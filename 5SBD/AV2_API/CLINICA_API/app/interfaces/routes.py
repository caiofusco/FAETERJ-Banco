from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.application.services import (
    AuthService,
    AvailabilityService,
    PackageServiceApp,
    ReservationService,
    get_reservation_or_404,
    get_waitlist_entry_or_404,
    package_to_read,
)
from app.core.security import hash_password
from app.domain.enums import PaymentStatusEnum, RoleEnum, WaitlistStatusEnum
from app.infrastructure.database import get_db
from app.infrastructure.models import (
    Package,
    Payment,
    Professional,
    Reservation,
    Service,
    User,
    WaitlistEntry,
    WorkSchedule,
)
from app.interfaces.dependencies import get_current_user, require_roles
from app.interfaces.schemas import (
    AvailableSlot,
    ClientCreate,
    LoginRequest,
    PackageCreate,
    PackageRead,
    PackageUpdate,
    PaymentRead,
    ProfessionalCreate,
    ProfessionalRead,
    ProfessionalUpdate,
    ReservationCreate,
    ReservationRead,
    ReservationUpdate,
    ScheduleCreate,
    ScheduleRead,
    ScheduleUpdate,
    ServiceCreate,
    ServiceRead,
    ServiceUpdate,
    Token,
    UserCreate,
    UserRead,
    UserUpdate,
    WaitlistCreate,
    WaitlistRead,
    WaitlistUpdate,
)

router = APIRouter()


# -------------------------
# Autenticação
# -------------------------
@router.post("/auth/register", response_model=UserRead, status_code=status.HTTP_201_CREATED, tags=["Auth"])
def register_client(data: ClientCreate, db: Session = Depends(get_db)):
    return AuthService(db).register_user(role=RoleEnum.CLIENTE, **data.model_dump())


@router.post("/auth/login", response_model=Token, tags=["Auth"])
def login(data: LoginRequest, db: Session = Depends(get_db)):
    _, token = AuthService(db).authenticate(email=data.email, password=data.password)
    return Token(access_token=token)


@router.get("/auth/me", response_model=UserRead, tags=["Auth"])
def me(current_user: User = Depends(get_current_user)):
    return current_user


# -------------------------
# Usuários e clientes
# -------------------------
@router.post(
    "/users",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    tags=["Usuários"],
    dependencies=[Depends(require_roles(RoleEnum.ADMINISTRADOR))],
)
def create_user(data: UserCreate, db: Session = Depends(get_db)):
    return AuthService(db).register_user(**data.model_dump())


@router.get(
    "/clients",
    response_model=list[UserRead],
    tags=["Clientes"],
    dependencies=[Depends(require_roles(RoleEnum.ADMINISTRADOR, RoleEnum.ATENDENTE))],
)
def list_clients(offset: int = 0, limit: int = Query(100, le=200), db: Session = Depends(get_db)):
    return db.scalars(select(User).where(User.role == RoleEnum.CLIENTE).offset(offset).limit(limit)).all()


@router.post(
    "/clients",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    tags=["Clientes"],
    dependencies=[Depends(require_roles(RoleEnum.ADMINISTRADOR, RoleEnum.ATENDENTE))],
)
def create_client(data: ClientCreate, db: Session = Depends(get_db)):
    return AuthService(db).register_user(role=RoleEnum.CLIENTE, **data.model_dump())


@router.get("/clients/{client_id}", response_model=UserRead, tags=["Clientes"])
def get_client(client_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    client = _get_client_or_404(db, client_id)
    if current_user.role == RoleEnum.CLIENTE and current_user.id != client.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permissão insuficiente")
    return client


@router.put("/clients/{client_id}", response_model=UserRead, tags=["Clientes"])
def update_client(client_id: int, data: UserUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    client = _get_client_or_404(db, client_id)
    can_update = current_user.id == client.id or current_user.role in {RoleEnum.ADMINISTRADOR, RoleEnum.ATENDENTE}
    if not can_update:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permissão insuficiente")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(client, field, value)
    db.commit()
    db.refresh(client)
    return client


@router.delete(
    "/clients/{client_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Clientes"],
    dependencies=[Depends(require_roles(RoleEnum.ADMINISTRADOR, RoleEnum.ATENDENTE))],
)
def delete_client(client_id: int, db: Session = Depends(get_db)):
    client = _get_client_or_404(db, client_id)
    client.is_active = False
    db.commit()
    return None


# -------------------------
# Serviços
# -------------------------
@router.get("/services", response_model=list[ServiceRead], tags=["Serviços"])
def list_services(
    specialty: str | None = None,
    professional_id: int | None = None,
    highlighted: bool | None = None,
    active: bool | None = True,
    offset: int = 0,
    limit: int = Query(100, le=200),
    db: Session = Depends(get_db),
):
    stmt = select(Service).offset(offset).limit(limit)
    if active is not None:
        stmt = stmt.where(Service.active.is_(active))
    if specialty:
        stmt = stmt.where(Service.specialty == specialty)
    if professional_id:
        professional = db.get(Professional, professional_id)
        if not professional:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profissional não encontrado")
        stmt = stmt.where(Service.specialty == professional.specialty)
    if highlighted is not None:
        stmt = stmt.where(Service.highlighted.is_(highlighted))
    return db.scalars(stmt).all()


@router.post(
    "/services",
    response_model=ServiceRead,
    status_code=status.HTTP_201_CREATED,
    tags=["Serviços"],
    dependencies=[Depends(require_roles(RoleEnum.ADMINISTRADOR))],
)
def create_service(data: ServiceCreate, db: Session = Depends(get_db)):
    service = Service(**data.model_dump())
    db.add(service)
    db.commit()
    db.refresh(service)
    return service


@router.get("/services/{service_id}", response_model=ServiceRead, tags=["Serviços"])
def get_service(service_id: int, db: Session = Depends(get_db)):
    return _get_or_404(db, Service, service_id, "Serviço não encontrado")


@router.put(
    "/services/{service_id}",
    response_model=ServiceRead,
    tags=["Serviços"],
    dependencies=[Depends(require_roles(RoleEnum.ADMINISTRADOR))],
)
def update_service(service_id: int, data: ServiceUpdate, db: Session = Depends(get_db)):
    service = _get_or_404(db, Service, service_id, "Serviço não encontrado")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(service, field, value)
    db.commit()
    db.refresh(service)
    return service


@router.delete(
    "/services/{service_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Serviços"],
    dependencies=[Depends(require_roles(RoleEnum.ADMINISTRADOR))],
)
def delete_service(service_id: int, db: Session = Depends(get_db)):
    service = _get_or_404(db, Service, service_id, "Serviço não encontrado")
    service.active = False
    db.commit()
    return None


# -------------------------
# Pacotes
# -------------------------
@router.get("/packages", response_model=list[PackageRead], tags=["Pacotes"])
def list_packages(active: bool | None = True, db: Session = Depends(get_db)):
    stmt = select(Package).options(joinedload(Package.items))
    if active is not None:
        stmt = stmt.where(Package.active.is_(active))
    packages = db.scalars(stmt).unique().all()
    return [package_to_read(package) for package in packages]


@router.post(
    "/packages",
    response_model=PackageRead,
    status_code=status.HTTP_201_CREATED,
    tags=["Pacotes"],
    dependencies=[Depends(require_roles(RoleEnum.ADMINISTRADOR))],
)
def create_package(data: PackageCreate, db: Session = Depends(get_db)):
    package = PackageServiceApp(db).create_package(data)
    return package_to_read(package)


@router.get("/packages/{package_id}", response_model=PackageRead, tags=["Pacotes"])
def get_package(package_id: int, db: Session = Depends(get_db)):
    package = db.scalar(select(Package).where(Package.id == package_id).options(joinedload(Package.items)))
    if not package:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pacote não encontrado")
    return package_to_read(package)


@router.put(
    "/packages/{package_id}",
    response_model=PackageRead,
    tags=["Pacotes"],
    dependencies=[Depends(require_roles(RoleEnum.ADMINISTRADOR))],
)
def update_package(package_id: int, data: PackageUpdate, db: Session = Depends(get_db)):
    package = db.scalar(select(Package).where(Package.id == package_id).options(joinedload(Package.items)))
    if not package:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pacote não encontrado")
    package = PackageServiceApp(db).update_package(package, data)
    return package_to_read(package)


@router.delete(
    "/packages/{package_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Pacotes"],
    dependencies=[Depends(require_roles(RoleEnum.ADMINISTRADOR))],
)
def delete_package(package_id: int, db: Session = Depends(get_db)):
    package = _get_or_404(db, Package, package_id, "Pacote não encontrado")
    package.active = False
    db.commit()
    return None


# -------------------------
# Profissionais
# -------------------------
@router.get("/professionals", response_model=list[ProfessionalRead], tags=["Profissionais"])
def list_professionals(
    specialty: str | None = None,
    active: bool | None = True,
    offset: int = 0,
    limit: int = Query(100, le=200),
    db: Session = Depends(get_db),
):
    stmt = select(Professional).offset(offset).limit(limit)
    if active is not None:
        stmt = stmt.where(Professional.active.is_(active))
    if specialty:
        stmt = stmt.where(Professional.specialty == specialty)
    return db.scalars(stmt).all()


@router.post(
    "/professionals",
    response_model=ProfessionalRead,
    status_code=status.HTTP_201_CREATED,
    tags=["Profissionais"],
    dependencies=[Depends(require_roles(RoleEnum.ADMINISTRADOR))],
)
def create_professional(data: ProfessionalCreate, db: Session = Depends(get_db)):
    professional = Professional(**data.model_dump())
    db.add(professional)
    db.commit()
    db.refresh(professional)
    return professional


@router.get("/professionals/{professional_id}", response_model=ProfessionalRead, tags=["Profissionais"])
def get_professional(professional_id: int, db: Session = Depends(get_db)):
    return _get_or_404(db, Professional, professional_id, "Profissional não encontrado")


@router.put(
    "/professionals/{professional_id}",
    response_model=ProfessionalRead,
    tags=["Profissionais"],
    dependencies=[Depends(require_roles(RoleEnum.ADMINISTRADOR))],
)
def update_professional(professional_id: int, data: ProfessionalUpdate, db: Session = Depends(get_db)):
    professional = _get_or_404(db, Professional, professional_id, "Profissional não encontrado")
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(professional, field, value)
    db.commit()
    db.refresh(professional)
    return professional


@router.delete(
    "/professionals/{professional_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Profissionais"],
    dependencies=[Depends(require_roles(RoleEnum.ADMINISTRADOR))],
)
def delete_professional(professional_id: int, db: Session = Depends(get_db)):
    professional = _get_or_404(db, Professional, professional_id, "Profissional não encontrado")
    professional.active = False
    db.commit()
    return None


# -------------------------
# Horários de trabalho e disponibilidade
# -------------------------
@router.get("/schedules", response_model=list[ScheduleRead], tags=["Horários"])
def list_schedules(
    professional_id: int | None = None,
    approved: bool | None = None,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles(RoleEnum.ADMINISTRADOR, RoleEnum.ATENDENTE, RoleEnum.PROFISSIONAL_TERCEIRIZADO, RoleEnum.PROFISSIONAL_CONTRATADO)),
):
    stmt = select(WorkSchedule)
    if professional_id:
        stmt = stmt.where(WorkSchedule.professional_id == professional_id)
    if approved is not None:
        stmt = stmt.where(WorkSchedule.approved.is_(approved))
    return db.scalars(stmt).all()


@router.post("/schedules", response_model=ScheduleRead, status_code=status.HTTP_201_CREATED, tags=["Horários"])
def create_schedule(
    data: ScheduleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(RoleEnum.ADMINISTRADOR, RoleEnum.PROFISSIONAL_TERCEIRIZADO)),
):
    _get_or_404(db, Professional, data.professional_id, "Profissional não encontrado")
    payload = data.model_dump()
    if current_user.role == RoleEnum.PROFISSIONAL_TERCEIRIZADO:
        payload["approved"] = False
    schedule = WorkSchedule(**payload)
    db.add(schedule)
    db.commit()
    db.refresh(schedule)
    return schedule


@router.put("/schedules/{schedule_id}", response_model=ScheduleRead, tags=["Horários"])
def update_schedule(
    schedule_id: int,
    data: ScheduleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(RoleEnum.ADMINISTRADOR, RoleEnum.PROFISSIONAL_TERCEIRIZADO)),
):
    schedule = _get_or_404(db, WorkSchedule, schedule_id, "Horário não encontrado")
    payload = data.model_dump(exclude_unset=True)
    if current_user.role != RoleEnum.ADMINISTRADOR:
        payload.pop("approved", None)
    for field, value in payload.items():
        setattr(schedule, field, value)
    db.commit()
    db.refresh(schedule)
    return schedule


@router.post(
    "/schedules/{schedule_id}/approve",
    response_model=ScheduleRead,
    tags=["Horários"],
    dependencies=[Depends(require_roles(RoleEnum.ADMINISTRADOR))],
)
def approve_schedule(schedule_id: int, db: Session = Depends(get_db)):
    schedule = _get_or_404(db, WorkSchedule, schedule_id, "Horário não encontrado")
    schedule.approved = True
    db.commit()
    db.refresh(schedule)
    return schedule


@router.delete(
    "/schedules/{schedule_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Horários"],
    dependencies=[Depends(require_roles(RoleEnum.ADMINISTRADOR))],
)
def delete_schedule(schedule_id: int, db: Session = Depends(get_db)):
    schedule = _get_or_404(db, WorkSchedule, schedule_id, "Horário não encontrado")
    db.delete(schedule)
    db.commit()
    return None


@router.get("/availability", response_model=list[AvailableSlot], tags=["Disponibilidade"])
def get_availability(service_id: int, day: date, professional_id: int | None = None, db: Session = Depends(get_db)):
    return AvailabilityService(db).get_available_slots(service_id=service_id, day=day, professional_id=professional_id)


# -------------------------
# Reservas e pagamento por cartão
# -------------------------
@router.get("/reservations", response_model=list[ReservationRead], tags=["Reservas"])
def list_reservations(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    stmt = select(Reservation).options(joinedload(Reservation.payment))
    if current_user.role == RoleEnum.CLIENTE:
        stmt = stmt.where(Reservation.client_id == current_user.id)
    elif current_user.role in {RoleEnum.PROFISSIONAL_CONTRATADO, RoleEnum.PROFISSIONAL_TERCEIRIZADO} and current_user.professional_profile:
        stmt = stmt.where(Reservation.professional_id == current_user.professional_profile.id)
    elif current_user.role not in {RoleEnum.ADMINISTRADOR, RoleEnum.ATENDENTE, RoleEnum.GERENTE_FINANCEIRO}:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permissão insuficiente")
    return db.scalars(stmt).all()


@router.post("/reservations", response_model=ReservationRead, status_code=status.HTTP_201_CREATED, tags=["Reservas"])
def create_reservation(data: ReservationCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return ReservationService(db).create_reservation(data, current_user)


@router.get("/reservations/{reservation_id}", response_model=ReservationRead, tags=["Reservas"])
def get_reservation(reservation_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    reservation = get_reservation_or_404(db, reservation_id)
    _ensure_can_view_reservation(current_user, reservation)
    return reservation


@router.put("/reservations/{reservation_id}", response_model=ReservationRead, tags=["Reservas"])
def update_reservation(
    reservation_id: int,
    data: ReservationUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    reservation = get_reservation_or_404(db, reservation_id)
    _ensure_can_change_reservation(current_user, reservation)
    return ReservationService(db).update_reservation(reservation, data)


@router.delete("/reservations/{reservation_id}", response_model=ReservationRead, tags=["Reservas"])
def cancel_reservation(reservation_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    reservation = get_reservation_or_404(db, reservation_id)
    _ensure_can_change_reservation(current_user, reservation)
    return ReservationService(db).cancel_reservation(reservation)


@router.post(
    "/reservations/{reservation_id}/no-show",
    response_model=ReservationRead,
    tags=["Reservas"],
    dependencies=[Depends(require_roles(RoleEnum.ADMINISTRADOR, RoleEnum.ATENDENTE))],
)
def mark_no_show(reservation_id: int, db: Session = Depends(get_db)):
    reservation = get_reservation_or_404(db, reservation_id)
    return ReservationService(db).mark_no_show(reservation)


# -------------------------
# Pagamentos
# -------------------------
@router.get("/payments", response_model=list[PaymentRead], tags=["Pagamentos"])
def list_payments(
    db: Session = Depends(get_db),
    _: User = Depends(require_roles(RoleEnum.ADMINISTRADOR, RoleEnum.GERENTE_FINANCEIRO)),
):
    return db.scalars(select(Payment)).all()


@router.get("/payments/{payment_id}", response_model=PaymentRead, tags=["Pagamentos"])
def get_payment(
    payment_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles(RoleEnum.ADMINISTRADOR, RoleEnum.GERENTE_FINANCEIRO)),
):
    return _get_or_404(db, Payment, payment_id, "Pagamento não encontrado")


@router.put("/payments/{payment_id}/status", response_model=PaymentRead, tags=["Pagamentos"])
def update_payment_status(
    payment_id: int,
    new_status: PaymentStatusEnum,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles(RoleEnum.ADMINISTRADOR, RoleEnum.GERENTE_FINANCEIRO)),
):
    payment = _get_or_404(db, Payment, payment_id, "Pagamento não encontrado")
    payment.status = new_status
    db.commit()
    db.refresh(payment)
    return payment


# -------------------------
# Lista de espera
# -------------------------
@router.get("/waitlist", response_model=list[WaitlistRead], tags=["Lista de espera"])
def list_waitlist(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    stmt = select(WaitlistEntry)
    if current_user.role == RoleEnum.CLIENTE:
        stmt = stmt.where(WaitlistEntry.client_id == current_user.id)
    elif current_user.role not in {RoleEnum.ADMINISTRADOR, RoleEnum.ATENDENTE}:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permissão insuficiente")
    return db.scalars(stmt).all()


@router.post("/waitlist", response_model=WaitlistRead, status_code=status.HTTP_201_CREATED, tags=["Lista de espera"])
def create_waitlist_entry(data: WaitlistCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    client_id = current_user.id if current_user.role == RoleEnum.CLIENTE else data.client_id
    if not client_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Informe client_id")
    client = _get_client_or_404(db, client_id)
    service = _get_or_404(db, Service, data.service_id, "Serviço não encontrado")
    if data.professional_id:
        professional = _get_or_404(db, Professional, data.professional_id, "Profissional não encontrado")
        if professional.specialty != service.specialty:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Profissional não atende a especialidade do serviço")
    entry = WaitlistEntry(
        client_id=client.id,
        service_id=service.id,
        professional_id=data.professional_id,
        preferred_start=data.preferred_start,
        preferred_end=data.preferred_end,
        status=WaitlistStatusEnum.AGUARDANDO,
        notes=data.notes,
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


@router.put("/waitlist/{entry_id}", response_model=WaitlistRead, tags=["Lista de espera"])
def update_waitlist_entry(
    entry_id: int,
    data: WaitlistUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles(RoleEnum.ADMINISTRADOR, RoleEnum.ATENDENTE)),
):
    entry = get_waitlist_entry_or_404(db, entry_id)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(entry, field, value)
    db.commit()
    db.refresh(entry)
    return entry


@router.delete("/waitlist/{entry_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Lista de espera"])
def delete_waitlist_entry(
    entry_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles(RoleEnum.ADMINISTRADOR, RoleEnum.ATENDENTE)),
):
    entry = get_waitlist_entry_or_404(db, entry_id)
    db.delete(entry)
    db.commit()
    return None


# -------------------------
# Helpers
# -------------------------
def _get_or_404(db: Session, model: type, obj_id: int, detail: str):
    obj = db.get(model, obj_id)
    if not obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
    return obj


def _get_client_or_404(db: Session, client_id: int) -> User:
    client = db.get(User, client_id)
    if not client or client.role != RoleEnum.CLIENTE:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente não encontrado")
    return client


def _ensure_can_view_reservation(current_user: User, reservation: Reservation) -> None:
    if current_user.role == RoleEnum.CLIENTE and reservation.client_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permissão insuficiente")
    if current_user.role in {RoleEnum.PROFISSIONAL_CONTRATADO, RoleEnum.PROFISSIONAL_TERCEIRIZADO}:
        if not current_user.professional_profile or current_user.professional_profile.id != reservation.professional_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permissão insuficiente")


def _ensure_can_change_reservation(current_user: User, reservation: Reservation) -> None:
    if current_user.role in {RoleEnum.ADMINISTRADOR, RoleEnum.ATENDENTE}:
        return
    if current_user.role == RoleEnum.CLIENTE and reservation.client_id == current_user.id:
        return
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Permissão insuficiente")
