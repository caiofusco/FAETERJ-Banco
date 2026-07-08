from app.fila_espera.domain.entities.fila_espera import FilaEspera
from app.fila_espera.domain.repositories.fila_espera_repository import (
    FilaEsperaRepository,
)


class FilaEsperaNaoEncontradaError(Exception):
    pass


class BuscarFilaEspera:
    def __init__(self, repositorio: FilaEsperaRepository):
        self.repositorio = repositorio

    def buscar(self, registro_id: int) -> FilaEspera:
        registro = self.repositorio.buscar_por_id(registro_id)
        if registro is None:
            raise FilaEsperaNaoEncontradaError(
                "Registro da fila de espera não encontrado"
            )
        return registro
