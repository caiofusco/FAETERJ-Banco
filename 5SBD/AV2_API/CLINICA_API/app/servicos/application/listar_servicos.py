from app.servicos.domain.entities.servico import Servico
from app.servicos.domain.repositories.servico_repository import ServicoRepository


class ListarServicos:
    def __init__(self, repositorio: ServicoRepository):
        self.repositorio = repositorio

    def listar(self) -> list[Servico]:
        return self.repositorio.listar()
