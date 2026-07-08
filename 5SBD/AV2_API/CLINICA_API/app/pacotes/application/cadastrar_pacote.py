from app.pacotes.domain.entities.pacote import Pacote
from app.pacotes.domain.repositories.pacote_repository import PacoteRepository


class CadastrarPacote:
    def __init__(self, repositorio: PacoteRepository):
        self.repositorio = repositorio

    def cadastrar(
        self, nome: str, descricao: str, valor: float, servicos: list[int]
    ) -> Pacote:
        pacote = Pacote(nome=nome, descricao=descricao, valor=valor, servicos=servicos)
        return self.repositorio.salvar(pacote)
