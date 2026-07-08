from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.reservas.domain.entities.reserva import StatusReserva


class ReservaEntrada(BaseModel):
    cliente_id: int = Field(gt=0)
    profissional_id: int = Field(gt=0)
    servico_id: int | None = Field(default=None, gt=0)
    pacote_id: int | None = Field(default=None, gt=0)
    data_hora: datetime
    status: StatusReserva = StatusReserva.AGENDADA
    valor_total: float = Field(ge=0)


class ReservaAtualizacao(ReservaEntrada):
    pass


class ReservaSaida(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    cliente_id: int
    profissional_id: int
    servico_id: int | None
    pacote_id: int | None
    data_hora: datetime
    status: StatusReserva
    valor_total: float
