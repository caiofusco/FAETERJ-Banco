from app.fila_espera.domain.entities.fila_espera import FilaEspera
from app.fila_espera.domain.repositories.fila_espera_repository import (
    FilaEsperaRepository,
)


class ListarFilaEspera:
    def __init__(self, repositorio: FilaEsperaRepository):
        self.repositorio = repositorio

    def listar(self) -> list[FilaEspera]:
        return self.repositorio.listar()
