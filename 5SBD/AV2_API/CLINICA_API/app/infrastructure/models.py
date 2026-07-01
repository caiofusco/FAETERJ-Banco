from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, Numeric, String, Text, UniqueConstraint
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.enums import (
    PaymentMethodEnum,
    PaymentStatusEnum,
    ProfessionalTypeEnum,
    ReservationStatusEnum,
    RoleEnum,
    WaitlistStatusEnum,
)
from app.infrastructure.database import Base


def enum_values(enum_cls):
    return [item.value for item in enum_cls]


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(180), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[RoleEnum] = mapped_column(
        SQLEnum(RoleEnum, values_callable=enum_values, native_enum=False),
        default=RoleEnum.CLIENTE,
        nullable=False,
    )
    phone: Mapped[str | None] = mapped_column(String(30), nullable=True)
    document: Mapped[str | None] = mapped_column(String(30), nullable=True)
    credit_balance: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=0, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)

    reservations: Mapped[list["Reservation"]] = relationship(back_populates="client")
    professional_profile: Mapped["Professional | None"] = relationship(back_populates="user", uselist=False)


class Professional(Base):
    __tablename__ = "professionals"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str | None] = mapped_column(String(180), unique=True, nullable=True)
    specialty: Mapped[str] = mapped_column(String(80), index=True, nullable=False)
    professional_type: Mapped[ProfessionalTypeEnum] = mapped_column(
        SQLEnum(ProfessionalTypeEnum, values_callable=enum_values, native_enum=False),
        default=ProfessionalTypeEnum.CONTRATADO,
        nullable=False,
    )
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), unique=True, nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)

    user: Mapped[User | None] = relationship(back_populates="professional_profile")
    schedules: Mapped[list["WorkSchedule"]] = relationship(back_populates="professional", cascade="all, delete-orphan")
    reservations: Mapped[list["Reservation"]] = relationship(back_populates="professional")


class Service(Base):
    __tablename__ = "services"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    specialty: Mapped[str] = mapped_column(String(80), index=True, nullable=False)
    duration_minutes: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    highlighted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)

    reservations: Mapped[list["Reservation"]] = relationship(back_populates="service")
    package_items: Mapped[list["PackageService"]] = relationship(back_populates="service")


class Package(Base):
    __tablename__ = "packages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)

    items: Mapped[list["PackageService"]] = relationship(back_populates="package", cascade="all, delete-orphan")


class PackageService(Base):
    __tablename__ = "package_services"
    __table_args__ = (UniqueConstraint("package_id", "service_id", name="uq_package_service"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    package_id: Mapped[int] = mapped_column(ForeignKey("packages.id"), nullable=False)
    service_id: Mapped[int] = mapped_column(ForeignKey("services.id"), nullable=False)

    package: Mapped[Package] = relationship(back_populates="items")
    service: Mapped[Service] = relationship(back_populates="package_items")


class WorkSchedule(Base):
    __tablename__ = "work_schedules"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    professional_id: Mapped[int] = mapped_column(ForeignKey("professionals.id"), nullable=False, index=True)
    starts_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    ends_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    approved: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    notes: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)

    professional: Mapped[Professional] = relationship(back_populates="schedules")


class Reservation(Base):
    __tablename__ = "reservations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    service_id: Mapped[int] = mapped_column(ForeignKey("services.id"), nullable=False, index=True)
    professional_id: Mapped[int] = mapped_column(ForeignKey("professionals.id"), nullable=False, index=True)
    starts_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    ends_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    status: Mapped[ReservationStatusEnum] = mapped_column(
        SQLEnum(ReservationStatusEnum, values_callable=enum_values, native_enum=False),
        default=ReservationStatusEnum.AGENDADO,
        nullable=False,
    )
    total_price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    credit_generated: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)

    client: Mapped[User] = relationship(back_populates="reservations")
    service: Mapped[Service] = relationship(back_populates="reservations")
    professional: Mapped[Professional] = relationship(back_populates="reservations")
    payment: Mapped["Payment | None"] = relationship(back_populates="reservation", uselist=False, cascade="all, delete-orphan")


class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    reservation_id: Mapped[int] = mapped_column(ForeignKey("reservations.id"), unique=True, nullable=False)
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    method: Mapped[PaymentMethodEnum] = mapped_column(
        SQLEnum(PaymentMethodEnum, values_callable=enum_values, native_enum=False),
        default=PaymentMethodEnum.CARTAO_CREDITO,
        nullable=False,
    )
    status: Mapped[PaymentStatusEnum] = mapped_column(
        SQLEnum(PaymentStatusEnum, values_callable=enum_values, native_enum=False),
        default=PaymentStatusEnum.APROVADO,
        nullable=False,
    )
    card_last4: Mapped[str] = mapped_column(String(4), nullable=False)
    transaction_reference: Mapped[str] = mapped_column(String(80), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)

    reservation: Mapped[Reservation] = relationship(back_populates="payment")


class WaitlistEntry(Base):
    __tablename__ = "waitlist_entries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    service_id: Mapped[int] = mapped_column(ForeignKey("services.id"), nullable=False, index=True)
    professional_id: Mapped[int | None] = mapped_column(ForeignKey("professionals.id"), nullable=True, index=True)
    preferred_start: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    preferred_end: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    status: Mapped[WaitlistStatusEnum] = mapped_column(
        SQLEnum(WaitlistStatusEnum, values_callable=enum_values, native_enum=False),
        default=WaitlistStatusEnum.AGUARDANDO,
        nullable=False,
    )
    notes: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utc_now, nullable=False)
