from datetime import date, datetime, time, timedelta
from decimal import Decimal
from uuid import uuid4

from sqlalchemy import and_, select
from sqlalchemy.orm import Session, joinedload

from app.core.security import create_access_token, hash_password, verify_password
from app.domain.enums import PaymentMethodEnum, PaymentStatusEnum, ReservationStatusEnum, RoleEnum
from app.domain.exceptions import BusinessRuleError, NotFoundError
from app.infrastructure.models import (
    Package,
    PackageService,
    Payment,
    Professional,
    Reservation,
    Service,
    User,
    WaitlistEntry,
    WorkSchedule,
)
from app.interfaces.schemas import PackageCreate, PackageUpdate, ReservationCreate, ReservationUpdate


class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def register_user(self, *, name: str, email: str, password: str, role: RoleEnum, phone: str | None = None, document: str | None = None) -> User:
        existing = self.db.scalar(select(User).where(User.email == email))
        if existing:
            raise BusinessRuleError("Já existe um usuário cadastrado com este e-mail.")
        user = User(
            name=name,
            email=email,
            password_hash=hash_password(password),
            role=role,
            phone=phone,
            document=document,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def authenticate(self, email: str, password: str) -> tuple[User, str]:
        user = self.db.scalar(select(User).where(User.email == email, User.is_active.is_(True)))
        if not user or not verify_password(password, user.password_hash):
            raise BusinessRuleError("E-mail ou senha inválidos.")
        token = create_access_token(subject=str(user.id), claims={"role": user.role.value})
        return user, token


class PackageServiceApp:
    def __init__(self, db: Session):
        self.db = db

    def create_package(self, data: PackageCreate) -> Package:
        service_ids = data.service_ids
        self._validate_services(service_ids)
        payload = data.model_dump(exclude={"service_ids"})
        package = Package(**payload)
        self.db.add(package)
        self.db.flush()
        package.items = [PackageService(service_id=service_id) for service_id in service_ids]
        self.db.commit()
        self.db.refresh(package)
        return package

    def update_package(self, package: Package, data: PackageUpdate) -> Package:
        payload = data.model_dump(exclude_unset=True)
        service_ids = payload.pop("service_ids", None)
        for field, value in payload.items():
            setattr(package, field, value)
        if service_ids is not None:
            self._validate_services(service_ids)
            package.items.clear()
            self.db.flush()
            package.items = [PackageService(service_id=service_id) for service_id in service_ids]
        self.db.commit()
        self.db.refresh(package)
        return package

    def _validate_services(self, service_ids: list[int]) -> None:
        if not service_ids:
            return
        found = set(self.db.scalars(select(Service.id).where(Service.id.in_(service_ids), Service.active.is_(True))).all())
        missing = set(service_ids) - found
        if missing:
            raise NotFoundError(f"Serviço(s) inexistente(s) ou inativo(s): {sorted(missing)}")


def package_to_read(package: Package) -> dict:
    return {
        "id": package.id,
        "name": package.name,
        "description": package.description,
        "price": package.price,
        "active": package.active,
        "service_ids": [item.service_id for item in package.items],
        "created_at": package.created_at,
    }


class AvailabilityService:
    SLOT_STEP_MINUTES = 15

    def __init__(self, db: Session):
        self.db = db

    def get_available_slots(self, *, service_id: int, day: date, professional_id: int | None = None) -> list[dict]:
        service = self.db.get(Service, service_id)
        if not service or not service.active:
            raise NotFoundError("Serviço não encontrado ou inativo.")

        professionals_stmt = select(Professional).where(
            Professional.active.is_(True),
            Professional.specialty == service.specialty,
        )
        if professional_id:
            professionals_stmt = professionals_stmt.where(Professional.id == professional_id)
        professionals = self.db.scalars(professionals_stmt).all()

        day_start = datetime.combine(day, time.min)
        day_end = datetime.combine(day, time.max)
        result: list[dict] = []

        for professional in professionals:
            schedules = self.db.scalars(
                select(WorkSchedule).where(
                    WorkSchedule.professional_id == professional.id,
                    WorkSchedule.approved.is_(True),
                    WorkSchedule.starts_at <= day_end,
                    WorkSchedule.ends_at >= day_start,
                )
            ).all()
            reservations = self.db.scalars(
                select(Reservation).where(
                    Reservation.professional_id == professional.id,
                    Reservation.status == ReservationStatusEnum.AGENDADO,
                    Reservation.starts_at < day_end,
                    Reservation.ends_at > day_start,
                )
            ).all()

            for schedule in schedules:
                cursor = max(schedule.starts_at, day_start)
                max_start = min(schedule.ends_at, day_end) - timedelta(minutes=service.duration_minutes)
                while cursor <= max_start:
                    slot_end = cursor + timedelta(minutes=service.duration_minutes)
                    if not self._overlaps_any(cursor, slot_end, reservations):
                        result.append(
                            {
                                "professional_id": professional.id,
                                "professional_name": professional.name,
                                "specialty": professional.specialty,
                                "starts_at": cursor,
                                "ends_at": slot_end,
                            }
                        )
                    cursor += timedelta(minutes=self.SLOT_STEP_MINUTES)
        return sorted(result, key=lambda item: (item["starts_at"], item["professional_id"]))

    def ensure_slot_is_available(self, *, service: Service, professional: Professional, starts_at: datetime) -> None:
        ends_at = starts_at + timedelta(minutes=service.duration_minutes)
        if professional.specialty != service.specialty:
            raise BusinessRuleError("O profissional escolhido não atende a especialidade do serviço.")

        schedule_exists = self.db.scalar(
            select(WorkSchedule.id).where(
                WorkSchedule.professional_id == professional.id,
                WorkSchedule.approved.is_(True),
                WorkSchedule.starts_at <= starts_at,
                WorkSchedule.ends_at >= ends_at,
            )
        )
        if not schedule_exists:
            raise BusinessRuleError("Não há horário aprovado para este profissional neste período.")

        conflict = self.db.scalar(
            select(Reservation.id).where(
                Reservation.professional_id == professional.id,
                Reservation.status == ReservationStatusEnum.AGENDADO,
                Reservation.starts_at < ends_at,
                Reservation.ends_at > starts_at,
            )
        )
        if conflict:
            raise BusinessRuleError("Horário indisponível para o profissional selecionado.")

    @staticmethod
    def _overlaps_any(starts_at: datetime, ends_at: datetime, reservations: list[Reservation]) -> bool:
        return any(res.starts_at < ends_at and res.ends_at > starts_at for res in reservations)


class ReservationService:
    def __init__(self, db: Session):
        self.db = db
        self.availability = AvailabilityService(db)

    def create_reservation(self, data: ReservationCreate, current_user: User) -> Reservation:
        service = self.db.get(Service, data.service_id)
        if not service or not service.active:
            raise NotFoundError("Serviço não encontrado ou inativo.")

        client_id = self._resolve_client_id(data.client_id, current_user)
        client = self.db.get(User, client_id)
        if not client or client.role != RoleEnum.CLIENTE or not client.is_active:
            raise BusinessRuleError("Cliente inválido ou inativo.")

        professional = self._resolve_professional(service, data.professional_id, data.starts_at)
        ends_at = data.starts_at + timedelta(minutes=service.duration_minutes)
        self.availability.ensure_slot_is_available(service=service, professional=professional, starts_at=data.starts_at)

        reservation = Reservation(
            client_id=client_id,
            service_id=service.id,
            professional_id=professional.id,
            starts_at=data.starts_at,
            ends_at=ends_at,
            total_price=service.price,
            status=ReservationStatusEnum.AGENDADO,
        )
        self.db.add(reservation)
        self.db.flush()
        payment = Payment(
            reservation_id=reservation.id,
            amount=service.price,
            method=PaymentMethodEnum.CARTAO_CREDITO,
            status=PaymentStatusEnum.APROVADO,
            card_last4=data.card_last4,
            transaction_reference=f"SIM-{uuid4().hex[:12].upper()}",
        )
        self.db.add(payment)
        self.db.commit()
        self.db.refresh(reservation)
        return reservation

    def update_reservation(self, reservation: Reservation, data: ReservationUpdate) -> Reservation:
        payload = data.model_dump(exclude_unset=True)
        new_professional_id = payload.get("professional_id", reservation.professional_id)
        new_starts_at = payload.get("starts_at", reservation.starts_at)

        if "professional_id" in payload or "starts_at" in payload:
            service = self.db.get(Service, reservation.service_id)
            professional = self.db.get(Professional, new_professional_id)
            if not service or not professional:
                raise NotFoundError("Serviço ou profissional não encontrado.")

            old_status = reservation.status
            reservation.status = ReservationStatusEnum.CANCELADO
            self.db.flush()
            try:
                self.availability.ensure_slot_is_available(service=service, professional=professional, starts_at=new_starts_at)
            finally:
                reservation.status = old_status
            reservation.professional_id = professional.id
            reservation.starts_at = new_starts_at
            reservation.ends_at = new_starts_at + timedelta(minutes=service.duration_minutes)

        if "status" in payload and payload["status"] is not None:
            reservation.status = payload["status"]

        self.db.commit()
        self.db.refresh(reservation)
        return reservation

    def cancel_reservation(self, reservation: Reservation) -> Reservation:
        reservation.status = ReservationStatusEnum.CANCELADO
        if reservation.payment:
            reservation.payment.status = PaymentStatusEnum.CANCELADO
        self.db.commit()
        self.db.refresh(reservation)
        return reservation

    def mark_no_show(self, reservation: Reservation) -> Reservation:
        if reservation.status != ReservationStatusEnum.AGENDADO:
            raise BusinessRuleError("Apenas reservas agendadas podem ser marcadas como não comparecimento.")
        credit = Decimal(reservation.total_price) / Decimal("2")
        reservation.status = ReservationStatusEnum.NAO_COMPARECEU
        reservation.credit_generated = credit
        reservation.client.credit_balance = Decimal(reservation.client.credit_balance) + credit
        self.db.commit()
        self.db.refresh(reservation)
        return reservation

    def _resolve_client_id(self, client_id: int | None, current_user: User) -> int:
        if current_user.role == RoleEnum.CLIENTE:
            return current_user.id
        if current_user.role in {RoleEnum.ADMINISTRADOR, RoleEnum.ATENDENTE} and client_id:
            return client_id
        if current_user.role in {RoleEnum.ADMINISTRADOR, RoleEnum.ATENDENTE} and not client_id:
            raise BusinessRuleError("Informe client_id para criar reserva como atendente/administrador.")
        raise BusinessRuleError("Seu perfil não tem permissão para criar reserva.")

    def _resolve_professional(self, service: Service, professional_id: int | None, starts_at: datetime) -> Professional:
        if professional_id:
            professional = self.db.get(Professional, professional_id)
            if not professional or not professional.active:
                raise NotFoundError("Profissional não encontrado ou inativo.")
            return professional

        candidates = self.db.scalars(
            select(Professional).where(
                Professional.active.is_(True),
                Professional.specialty == service.specialty,
            )
        ).all()
        for candidate in candidates:
            try:
                self.availability.ensure_slot_is_available(service=service, professional=candidate, starts_at=starts_at)
                return candidate
            except BusinessRuleError:
                continue
        raise BusinessRuleError("Nenhum profissional disponível para o horário solicitado.")


def get_reservation_or_404(db: Session, reservation_id: int) -> Reservation:
    reservation = db.scalar(
        select(Reservation)
        .where(Reservation.id == reservation_id)
        .options(joinedload(Reservation.payment), joinedload(Reservation.client))
    )
    if not reservation:
        raise NotFoundError("Reserva não encontrada.")
    return reservation


def get_waitlist_entry_or_404(db: Session, entry_id: int) -> WaitlistEntry:
    entry = db.get(WaitlistEntry, entry_id)
    if not entry:
        raise NotFoundError("Entrada da lista de espera não encontrada.")
    return entry
