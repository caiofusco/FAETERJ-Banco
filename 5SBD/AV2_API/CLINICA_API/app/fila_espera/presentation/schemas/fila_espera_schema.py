from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.fila_espera.domain.entities.fila_espera import StatusFilaEspera


class FilaEsperaEntrada(BaseModel):
    cliente_id: int = Field(gt=0)
    servico_id: int = Field(gt=0)
    profissional_id: int | None = Field(default=None, gt=0)
    data_solicitada: datetime
    status: StatusFilaEspera = StatusFilaEspera.AGUARDANDO


class FilaEsperaAtualizacao(FilaEsperaEntrada):
    pass


class FilaEsperaSaida(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    cliente_id: int
    servico_id: int
    profissional_id: int | None
    data_solicitada: datetime
    status: StatusFilaEspera
