from app.servicos.domain.entities.servico import Servico
from app.servicos.domain.repositories.servico_repository import ServicoRepository


class CadastrarServico:
    def __init__(self, repositorio: ServicoRepository):
        self.repositorio = repositorio

    def cadastrar(
        self,
        nome: str,
        descricao: str,
        especialidade: str,
        valor: float,
        duracao_minutos: int,
    ) -> Servico:
        servico = Servico(
            nome=nome,
            descricao=descricao,
            especialidade=especialidade,
            valor=valor,
            duracao_minutos=duracao_minutos,
        )
        return self.repositorio.salvar(servico)
