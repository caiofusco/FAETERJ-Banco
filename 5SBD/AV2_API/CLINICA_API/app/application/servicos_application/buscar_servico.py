from app.domain.servicos_domain.entities.servico import Servico
from app.domain.servicos_domain.repositories.servico_repository import ServicoRepository


class ServicoNaoEncontradoError(Exception):
    pass


class BuscarServico:
    def __init__(self, repositorio: ServicoRepository):
        self.repositorio = repositorio

    def buscar(self, servico_id: int) -> Servico:
        servico = self.repositorio.buscar_por_id(servico_id)
        if servico is None:
            raise ServicoNaoEncontradoError("Serviço não encontrado")
        return servico
