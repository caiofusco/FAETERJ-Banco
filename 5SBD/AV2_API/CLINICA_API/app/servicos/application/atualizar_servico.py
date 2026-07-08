from app.servicos.application.buscar_servico import ServicoNaoEncontradoError
from app.servicos.domain.entities.servico import Servico
from app.servicos.domain.repositories.servico_repository import ServicoRepository


class AtualizarServico:
    def __init__(self, repositorio: ServicoRepository):
        self.repositorio = repositorio

    def atualizar(
        self,
        servico_id: int,
        nome: str,
        descricao: str,
        especialidade: str,
        valor: float,
        duracao_minutos: int,
    ) -> Servico:
        servico = self.repositorio.buscar_por_id(servico_id)
        if servico is None:
            raise ServicoNaoEncontradoError("Serviço não encontrado")
        servico.atualizar(
            nome=nome,
            descricao=descricao,
            especialidade=especialidade,
            valor=valor,
            duracao_minutos=duracao_minutos,
        )
        return self.repositorio.atualizar(servico)
