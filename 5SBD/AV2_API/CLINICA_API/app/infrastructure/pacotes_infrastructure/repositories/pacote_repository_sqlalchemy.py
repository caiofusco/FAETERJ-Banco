from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.pacotes_domain.entities.pacote import Pacote
from app.domain.pacotes_domain.repositories.pacote_repository import PacoteRepository
from app.infrastructure.pacotes_infrastructure.models.pacote_model import PacoteModel


class PacoteRepositorySQLAlchemy(PacoteRepository):
    def __init__(self, sessao: Session):
        self.sessao = sessao

    @staticmethod
    def transformar_em_entidade(model: PacoteModel) -> Pacote:
        return Pacote(
            id=model.id,
            nome=model.nome,
            descricao=model.descricao,
            valor=model.valor,
            servicos=model.servicos,
        )

    def salvar(self, pacote: Pacote) -> Pacote:
        model = PacoteModel(
            nome=pacote.nome,
            descricao=pacote.descricao,
            valor=pacote.valor,
            servicos=pacote.servicos,
        )
        self.sessao.add(model)
        self.sessao.commit()
        self.sessao.refresh(model)
        return self.transformar_em_entidade(model)

    def listar(self) -> list[Pacote]:
        comando = select(PacoteModel).order_by(PacoteModel.id)
        return [
            self.transformar_em_entidade(model)
            for model in self.sessao.scalars(comando).all()
        ]

    def buscar_por_id(self, pacote_id: int) -> Pacote | None:
        model = self.sessao.get(PacoteModel, pacote_id)
        return None if model is None else self.transformar_em_entidade(model)

    def atualizar(self, pacote: Pacote) -> Pacote:
        model = self.sessao.get(PacoteModel, pacote.id)
        if model is None:
            raise ValueError("Pacote não encontrado")
        model.nome = pacote.nome
        model.descricao = pacote.descricao
        model.valor = pacote.valor
        model.servicos = pacote.servicos
        self.sessao.commit()
        self.sessao.refresh(model)
        return self.transformar_em_entidade(model)

    def excluir(self, pacote_id: int) -> bool:
        model = self.sessao.get(PacoteModel, pacote_id)
        if model is None:
            return False
        self.sessao.delete(model)
        self.sessao.commit()
        return True
