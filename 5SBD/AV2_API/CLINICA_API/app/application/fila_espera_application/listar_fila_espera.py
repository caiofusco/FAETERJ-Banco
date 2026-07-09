from app.domain.fila_espera_domain.entities.fila_espera import FilaEspera
from app.domain.fila_espera_domain.repositories.fila_espera_repository import (
    FilaEsperaRepository,
)


class ListarFilaEspera:
    def __init__(self, repositorio: FilaEsperaRepository):
        self.repositorio = repositorio

    def listar(self) -> list[FilaEspera]:
        return self.repositorio.listar()
