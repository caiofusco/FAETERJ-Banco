from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.servicos_domain.entities.servico import Servico
from app.domain.servicos_domain.repositories.servico_repository import ServicoRepository
from app.infrastructure.servicos_infrastructure.models.servico_model import ServicoModel


class ServicoRepositorySQLAlchemy(ServicoRepository):
    def __init__(self, sessao: Session):
        self.sessao = sessao

    @staticmethod
    def transformar_em_entidade(model: ServicoModel) -> Servico:
        return Servico(
            id=model.id,
            nome=model.nome,
            descricao=model.descricao,
            especialidade=model.especialidade,
            valor=model.valor,
            duracao_minutos=model.duracao_minutos,
        )

    def salvar(self, servico: Servico) -> Servico:
        model = ServicoModel(
            nome=servico.nome,
            descricao=servico.descricao,
            especialidade=servico.especialidade,
            valor=servico.valor,
            duracao_minutos=servico.duracao_minutos,
        )
        self.sessao.add(model)
        self.sessao.commit()
        self.sessao.refresh(model)
        return self.transformar_em_entidade(model)

    def listar(self) -> list[Servico]:
        comando = select(ServicoModel).order_by(ServicoModel.id)
        return [
            self.transformar_em_entidade(model)
            for model in self.sessao.scalars(comando).all()
        ]

    def buscar_por_id(self, servico_id: int) -> Servico | None:
        model = self.sessao.get(ServicoModel, servico_id)
        return None if model is None else self.transformar_em_entidade(model)

    def atualizar(self, servico: Servico) -> Servico:
        model = self.sessao.get(ServicoModel, servico.id)
        if model is None:
            raise ValueError("Serviço não encontrado")
        model.nome = servico.nome
        model.descricao = servico.descricao
        model.especialidade = servico.especialidade
        model.valor = servico.valor
        model.duracao_minutos = servico.duracao_minutos
        self.sessao.commit()
        self.sessao.refresh(model)
        return self.transformar_em_entidade(model)

    def excluir(self, servico_id: int) -> bool:
        model = self.sessao.get(ServicoModel, servico_id)
        if model is None:
            return False
        self.sessao.delete(model)
        self.sessao.commit()
        return True
