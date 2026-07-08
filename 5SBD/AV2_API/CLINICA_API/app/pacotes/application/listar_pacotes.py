from app.pacotes.domain.entities.pacote import Pacote
from app.pacotes.domain.repositories.pacote_repository import PacoteRepository


class ListarPacotes:
    def __init__(self, repositorio: PacoteRepository):
        self.repositorio = repositorio

    def listar(self) -> list[Pacote]:
        return self.repositorio.listar()
