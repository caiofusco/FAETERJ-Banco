from app.pacotes.domain.entities.pacote import Pacote
from app.pacotes.domain.repositories.pacote_repository import PacoteRepository


class PacoteNaoEncontradoError(Exception):
    pass


class BuscarPacote:
    def __init__(self, repositorio: PacoteRepository):
        self.repositorio = repositorio

    def buscar(self, pacote_id: int) -> Pacote:
        pacote = self.repositorio.buscar_por_id(pacote_id)
        if pacote is None:
            raise PacoteNaoEncontradoError("Pacote não encontrado")
        return pacote
