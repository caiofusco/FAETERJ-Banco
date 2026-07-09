from app.application.servicos_application.buscar_servico import (
    ServicoNaoEncontradoError,
)
from app.domain.servicos_domain.repositories.servico_repository import ServicoRepository


class ExcluirServico:
    def __init__(self, repositorio: ServicoRepository):
        self.repositorio = repositorio

    def excluir(self, servico_id: int) -> None:
        if not self.repositorio.excluir(servico_id):
            raise ServicoNaoEncontradoError("Serviço não encontrado")
