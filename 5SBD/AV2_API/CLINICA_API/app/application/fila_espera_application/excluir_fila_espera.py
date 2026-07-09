from app.application.fila_espera_application.buscar_fila_espera import (
    FilaEsperaNaoEncontradaError,
)
from app.domain.fila_espera_domain.repositories.fila_espera_repository import (
    FilaEsperaRepository,
)


class ExcluirFilaEspera:
    def __init__(self, repositorio: FilaEsperaRepository):
        self.repositorio = repositorio

    def excluir(self, registro_id: int) -> None:
        if not self.repositorio.excluir(registro_id):
            raise FilaEsperaNaoEncontradaError(
                "Registro da fila de espera não encontrado"
            )
