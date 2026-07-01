from datetime import datetime, timedelta
from decimal import Decimal

from sqlalchemy import select

from app.core.security import hash_password
from app.domain.enums import ProfessionalTypeEnum, RoleEnum
from app.infrastructure.database import Base, SessionLocal, engine
from app.infrastructure.models import Package, PackageService, Professional, Service, User, WorkSchedule


USERS = [
    ("Administrador", "admin@beleza.com", RoleEnum.ADMINISTRADOR),
    ("Atendente", "atendente@beleza.com", RoleEnum.ATENDENTE),
    ("Gerente Financeiro", "financeiro@beleza.com", RoleEnum.GERENTE_FINANCEIRO),
    ("Cliente Demo", "cliente@beleza.com", RoleEnum.CLIENTE),
]


def run_seed() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        for name, email, role in USERS:
            exists = db.scalar(select(User).where(User.email == email))
            if not exists:
                db.add(User(name=name, email=email, role=role, password_hash=hash_password("123456"), is_active=True))
        db.commit()

        if not db.scalar(select(Service.id)):
            corte = Service(
                name="Corte Feminino",
                description="Corte de cabelo com profissional especializado.",
                specialty="cabelo",
                duration_minutes=60,
                price=Decimal("120.00"),
                highlighted=True,
            )
            limpeza = Service(
                name="Limpeza de Pele",
                description="Procedimento facial no centro de estética.",
                specialty="estetica_facial",
                duration_minutes=90,
                price=Decimal("180.00"),
                highlighted=True,
            )
            manicure = Service(
                name="Manicure",
                description="Cuidado completo das unhas.",
                specialty="unhas",
                duration_minutes=45,
                price=Decimal("55.00"),
            )
            db.add_all([corte, limpeza, manicure])
            db.flush()

            pacote = Package(name="Dia de Beleza", description="Corte + limpeza de pele.", price=Decimal("270.00"))
            db.add(pacote)
            db.flush()
            db.add_all([PackageService(package_id=pacote.id, service_id=corte.id), PackageService(package_id=pacote.id, service_id=limpeza.id)])

        if not db.scalar(select(Professional.id)):
            pros = [
                Professional(name="Ana Souza", email="ana@beleza.com", specialty="cabelo", professional_type=ProfessionalTypeEnum.CONTRATADO),
                Professional(name="Bruna Lima", email="bruna@beleza.com", specialty="estetica_facial", professional_type=ProfessionalTypeEnum.CONTRATADO),
                Professional(name="Carla Alves", email="carla@beleza.com", specialty="unhas", professional_type=ProfessionalTypeEnum.TERCEIRIZADO),
            ]
            db.add_all(pros)
            db.flush()
            tomorrow = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0) + timedelta(days=1)
            for pro in pros:
                db.add(WorkSchedule(professional_id=pro.id, starts_at=tomorrow, ends_at=tomorrow.replace(hour=18), approved=True))
        db.commit()
        print("Seed concluído. Usuários: admin@beleza.com, atendente@beleza.com, financeiro@beleza.com e cliente@beleza.com. Senha: 123456")
    finally:
        db.close()


if __name__ == "__main__":
    run_seed()
