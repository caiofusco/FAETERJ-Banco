from app.application.pacotes_application.buscar_pacote import PacoteNaoEncontradoError
from app.domain.pacotes_domain.entities.pacote import Pacote
from app.domain.pacotes_domain.repositories.pacote_repository import PacoteRepository


class AtualizarPacote:
    def __init__(self, repositorio: PacoteRepository):
        self.repositorio = repositorio

    def atualizar(
        self,
        pacote_id: int,
        nome: str,
        descricao: str,
        valor: float,
        servicos: list[int],
    ) -> Pacote:
        pacote = self.repositorio.buscar_por_id(pacote_id)
        if pacote is None:
            raise PacoteNaoEncontradoError("Pacote não encontrado")
        pacote.atualizar(nome=nome, descricao=descricao, valor=valor, servicos=servicos)
        return self.repositorio.atualizar(pacote)
