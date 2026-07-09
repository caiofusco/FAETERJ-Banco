from datetime import datetime

from app.domain.fila_espera_domain.entities.fila_espera import (
    FilaEspera,
    StatusFilaEspera,
)
from app.domain.fila_espera_domain.repositories.fila_espera_repository import (
    FilaEsperaRepository,
)


class CadastrarFilaEspera:
    def __init__(self, repositorio: FilaEsperaRepository):
        self.repositorio = repositorio

    def cadastrar(
        self,
        cliente_id: int,
        servico_id: int,
        data_solicitada: datetime,
        profissional_id: int | None = None,
        status: StatusFilaEspera = StatusFilaEspera.AGUARDANDO,
    ) -> FilaEspera:
        registro = FilaEspera(
            cliente_id=cliente_id,
            servico_id=servico_id,
            data_solicitada=data_solicitada,
            profissional_id=profissional_id,
            status=status,
        )
        return self.repositorio.salvar(registro)
