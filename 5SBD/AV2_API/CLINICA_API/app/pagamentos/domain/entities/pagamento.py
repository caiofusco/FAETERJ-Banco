from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class MetodoPagamento(str, Enum):
    CARTAO_CREDITO = "CARTAO_CREDITO"


class StatusPagamento(str, Enum):
    PENDENTE = "PENDENTE"
    APROVADO = "APROVADO"
    RECUSADO = "RECUSADO"
    CANCELADO = "CANCELADO"


@dataclass
class Pagamento:
    reserva_id: int
    valor: float
    metodo: MetodoPagamento = MetodoPagamento.CARTAO_CREDITO
    status: StatusPagamento = StatusPagamento.PENDENTE
    data_pagamento: datetime | None = None
    id: int | None = None

    def __post_init__(self) -> None:
        self._validar()

    def atualizar(
        self,
        reserva_id: int,
        valor: float,
        metodo: MetodoPagamento,
        status: StatusPagamento,
        data_pagamento: datetime | None,
    ) -> None:
        self.reserva_id = reserva_id
        self.valor = valor
        self.metodo = metodo
        self.status = status
        self.data_pagamento = data_pagamento
        self._validar()

    def _validar(self) -> None:
        if self.reserva_id <= 0:
            raise ValueError("O ID da reserva deve ser maior que zero")
        if self.valor <= 0:
            raise ValueError("O valor deve ser maior que zero")
        if self.metodo != MetodoPagamento.CARTAO_CREDITO:
            raise ValueError("O método aceito é cartão de crédito")
