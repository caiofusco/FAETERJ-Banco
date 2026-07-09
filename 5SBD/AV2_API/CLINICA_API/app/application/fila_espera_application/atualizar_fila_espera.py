from datetime import datetime

from app.application.fila_espera_application.buscar_fila_espera import (
    FilaEsperaNaoEncontradaError,
)
from app.domain.fila_espera_domain.entities.fila_espera import (
    FilaEspera,
    StatusFilaEspera,
)
from app.domain.fila_espera_domain.repositories.fila_espera_repository import (
    FilaEsperaRepository,
)


class AtualizarFilaEspera:
    def __init__(self, repositorio: FilaEsperaRepository):
        self.repositorio = repositorio

    def atualizar(
        self,
        registro_id: int,
        cliente_id: int,
        servico_id: int,
        data_solicitada: datetime,
        profissional_id: int | None,
        status: StatusFilaEspera,
    ) -> FilaEspera:
        registro = self.repositorio.buscar_por_id(registro_id)
        if registro is None:
            raise FilaEsperaNaoEncontradaError(
                "Registro da fila de espera não encontrado"
            )
        registro.atualizar(
            cliente_id=cliente_id,
            servico_id=servico_id,
            data_solicitada=data_solicitada,
            profissional_id=profissional_id,
            status=status,
        )
        return self.repositorio.atualizar(registro)
