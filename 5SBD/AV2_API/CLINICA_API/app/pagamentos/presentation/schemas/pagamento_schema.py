from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.pagamentos.domain.entities.pagamento import MetodoPagamento, StatusPagamento


class PagamentoEntrada(BaseModel):
    reserva_id: int = Field(gt=0)
    valor: float = Field(gt=0)
    metodo: MetodoPagamento = MetodoPagamento.CARTAO_CREDITO
    status: StatusPagamento = StatusPagamento.PENDENTE
    data_pagamento: datetime | None = None


class PagamentoAtualizacao(PagamentoEntrada):
    pass


class PagamentoSaida(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    reserva_id: int
    valor: float
    metodo: MetodoPagamento
    status: StatusPagamento
    data_pagamento: datetime | None
