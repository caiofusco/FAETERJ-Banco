from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class StatusReserva(str, Enum):
    AGENDADA = "AGENDADA"
    CONCLUIDA = "CONCLUIDA"
    CANCELADA = "CANCELADA"
    NAO_COMPARECEU = "NAO_COMPARECEU"
    ATRASADA = "ATRASADA"


@dataclass
class Reserva:
    cliente_id: int
    profissional_id: int
    data_hora: datetime
    status: StatusReserva
    valor_total: float
    servico_id: int | None = None
    pacote_id: int | None = None
    id: int | None = None

    def __post_init__(self) -> None:
        self._validar()

    def atualizar(
        self,
        cliente_id: int,
        profissional_id: int,
        data_hora: datetime,
        status: StatusReserva,
        valor_total: float,
        servico_id: int | None,
        pacote_id: int | None,
    ) -> None:
        self.cliente_id = cliente_id
        self.profissional_id = profissional_id
        self.data_hora = data_hora
        self.status = status
        self.valor_total = valor_total
        self.servico_id = servico_id
        self.pacote_id = pacote_id
        self._validar()

    def _validar(self) -> None:
        if self.cliente_id <= 0 or self.profissional_id <= 0:
            raise ValueError("Cliente e profissional devem ter IDs válidos")
        if (self.servico_id is None) == (self.pacote_id is None):
            raise ValueError("Informe apenas servico_id ou pacote_id")
        if self.servico_id is not None and self.servico_id <= 0:
            raise ValueError("O ID do serviço deve ser maior que zero")
        if self.pacote_id is not None and self.pacote_id <= 0:
            raise ValueError("O ID do pacote deve ser maior que zero")
        if self.valor_total < 0:
            raise ValueError("O valor total não pode ser negativo")
