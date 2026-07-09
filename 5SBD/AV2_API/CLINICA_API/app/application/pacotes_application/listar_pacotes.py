from app.domain.pacotes_domain.entities.pacote import Pacote
from app.domain.pacotes_domain.repositories.pacote_repository import PacoteRepository


class ListarPacotes:
    def __init__(self, repositorio: PacoteRepository):
        self.repositorio = repositorio

    def listar(self) -> list[Pacote]:
        return self.repositorio.listar()
