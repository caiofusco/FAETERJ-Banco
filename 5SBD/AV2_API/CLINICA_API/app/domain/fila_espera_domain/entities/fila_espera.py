from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class StatusFilaEspera(str, Enum):
    AGUARDANDO = "AGUARDANDO"
    CHAMADO = "CHAMADO"
    ATENDIDO = "ATENDIDO"
    CANCELADO = "CANCELADO"


@dataclass
class FilaEspera:
    cliente_id: int
    servico_id: int
    data_solicitada: datetime
    profissional_id: int | None = None
    status: StatusFilaEspera = StatusFilaEspera.AGUARDANDO
    id: int | None = None

    def __post_init__(self) -> None:
        self._validar()

    def atualizar(
        self,
        cliente_id: int,
        servico_id: int,
        data_solicitada: datetime,
        profissional_id: int | None,
        status: StatusFilaEspera,
    ) -> None:
        self.cliente_id = cliente_id
        self.servico_id = servico_id
        self.data_solicitada = data_solicitada
        self.profissional_id = profissional_id
        self.status = status
        self._validar()

    def _validar(self) -> None:
        if self.cliente_id <= 0 or self.servico_id <= 0:
            raise ValueError("Cliente e serviço devem ter IDs válidos")
        if self.profissional_id is not None and self.profissional_id <= 0:
            raise ValueError("O ID do profissional deve ser maior que zero")
