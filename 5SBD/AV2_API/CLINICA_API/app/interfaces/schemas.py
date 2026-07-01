from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from app.domain.enums import (
    PaymentMethodEnum,
    PaymentStatusEnum,
    ProfessionalTypeEnum,
    ReservationStatusEnum,
    RoleEnum,
    WaitlistStatusEnum,
)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)


class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(min_length=6, max_length=120)
    phone: str | None = None
    document: str | None = None
    role: RoleEnum = RoleEnum.CLIENTE


class ClientCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(min_length=6, max_length=120)
    phone: str | None = None
    document: str | None = None


class UserUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=120)
    phone: str | None = None
    document: str | None = None
    is_active: bool | None = None


class UserRead(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: RoleEnum
    phone: str | None = None
    document: str | None = None
    credit_balance: Decimal
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ServiceCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    description: str | None = None
    specialty: str = Field(min_length=2, max_length=80)
    duration_minutes: int = Field(gt=0, le=480)
    price: Decimal = Field(gt=0)
    highlighted: bool = False
    active: bool = True


class ServiceUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=120)
    description: str | None = None
    specialty: str | None = Field(default=None, min_length=2, max_length=80)
    duration_minutes: int | None = Field(default=None, gt=0, le=480)
    price: Decimal | None = Field(default=None, gt=0)
    highlighted: bool | None = None
    active: bool | None = None


class ServiceRead(BaseModel):
    id: int
    name: str
    description: str | None
    specialty: str
    duration_minutes: int
    price: Decimal
    highlighted: bool
    active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PackageCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    description: str | None = None
    price: Decimal = Field(gt=0)
    service_ids: list[int] = Field(default_factory=list)
    active: bool = True


class PackageUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=120)
    description: str | None = None
    price: Decimal | None = Field(default=None, gt=0)
    service_ids: list[int] | None = None
    active: bool | None = None


class PackageRead(BaseModel):
    id: int
    name: str
    description: str | None
    price: Decimal
    active: bool
    service_ids: list[int]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ProfessionalCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr | None = None
    specialty: str = Field(min_length=2, max_length=80)
    professional_type: ProfessionalTypeEnum = ProfessionalTypeEnum.CONTRATADO
    user_id: int | None = None
    active: bool = True


class ProfessionalUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=120)
    email: EmailStr | None = None
    specialty: str | None = Field(default=None, min_length=2, max_length=80)
    professional_type: ProfessionalTypeEnum | None = None
    user_id: int | None = None
    active: bool | None = None


class ProfessionalRead(BaseModel):
    id: int
    name: str
    email: EmailStr | None
    specialty: str
    professional_type: ProfessionalTypeEnum
    user_id: int | None
    active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ScheduleCreate(BaseModel):
    professional_id: int
    starts_at: datetime
    ends_at: datetime
    approved: bool = True
    notes: str | None = None

    @field_validator("ends_at")
    @classmethod
    def ends_must_be_after_start(cls, value: datetime, info):
        starts_at = info.data.get("starts_at")
        if starts_at and value <= starts_at:
            raise ValueError("ends_at deve ser maior que starts_at")
        return value


class ScheduleUpdate(BaseModel):
    starts_at: datetime | None = None
    ends_at: datetime | None = None
    approved: bool | None = None
    notes: str | None = None


class ScheduleRead(BaseModel):
    id: int
    professional_id: int
    starts_at: datetime
    ends_at: datetime
    approved: bool
    notes: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AvailabilityQuery(BaseModel):
    service_id: int
    day: date
    professional_id: int | None = None


class AvailableSlot(BaseModel):
    professional_id: int
    professional_name: str
    specialty: str
    starts_at: datetime
    ends_at: datetime


class ReservationCreate(BaseModel):
    service_id: int
    starts_at: datetime
    professional_id: int | None = None
    client_id: int | None = None
    card_last4: str = Field(min_length=4, max_length=4, pattern="^[0-9]{4}$")


class ReservationUpdate(BaseModel):
    starts_at: datetime | None = None
    professional_id: int | None = None
    status: ReservationStatusEnum | None = None


class PaymentRead(BaseModel):
    id: int
    reservation_id: int
    amount: Decimal
    method: PaymentMethodEnum
    status: PaymentStatusEnum
    card_last4: str
    transaction_reference: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ReservationRead(BaseModel):
    id: int
    client_id: int
    service_id: int
    professional_id: int
    starts_at: datetime
    ends_at: datetime
    status: ReservationStatusEnum
    total_price: Decimal
    credit_generated: Decimal
    created_at: datetime
    payment: PaymentRead | None = None

    model_config = ConfigDict(from_attributes=True)


class WaitlistCreate(BaseModel):
    service_id: int
    preferred_start: datetime
    preferred_end: datetime
    professional_id: int | None = None
    client_id: int | None = None
    notes: str | None = None

    @field_validator("preferred_end")
    @classmethod
    def preferred_end_must_be_after_start(cls, value: datetime, info):
        preferred_start = info.data.get("preferred_start")
        if preferred_start and value <= preferred_start:
            raise ValueError("preferred_end deve ser maior que preferred_start")
        return value


class WaitlistUpdate(BaseModel):
    status: WaitlistStatusEnum | None = None
    notes: str | None = None


class WaitlistRead(BaseModel):
    id: int
    client_id: int
    service_id: int
    professional_id: int | None
    preferred_start: datetime
    preferred_end: datetime
    status: WaitlistStatusEnum
    notes: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
