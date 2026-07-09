from app.application.pacotes_application.buscar_pacote import PacoteNaoEncontradoError
from app.domain.pacotes_domain.repositories.pacote_repository import PacoteRepository


class ExcluirPacote:
    def __init__(self, repositorio: PacoteRepository):
        self.repositorio = repositorio

    def excluir(self, pacote_id: int) -> None:
        if not self.repositorio.excluir(pacote_id):
            raise PacoteNaoEncontradoError("Pacote não encontrado")
