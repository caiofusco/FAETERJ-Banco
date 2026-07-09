from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.profissionais_domain.entities.profissional import Profissional
from app.domain.profissionais_domain.repositories.profissional_repository import (
    ProfissionalRepository,
)
from app.infrastructure.profissionais_infrastructure.models.profissional_model import (
    ProfissionalModel,
)


class ProfissionalRepositorySQLAlchemy(ProfissionalRepository):
    def __init__(self, sessao: Session):
        self.sessao = sessao

    @staticmethod
    def transformar_em_entidade(model: ProfissionalModel) -> Profissional:
        return Profissional(
            id=model.id,
            nome=model.nome,
            especialidade=model.especialidade,
            ativo=model.ativo,
        )

    def salvar(self, profissional: Profissional) -> Profissional:
        model = ProfissionalModel(
            nome=profissional.nome,
            especialidade=profissional.especialidade,
            ativo=profissional.ativo,
        )
        self.sessao.add(model)
        self.sessao.commit()
        self.sessao.refresh(model)
        return self.transformar_em_entidade(model)

    def listar(self) -> list[Profissional]:
        comando = select(ProfissionalModel).order_by(ProfissionalModel.id)
        return [
            self.transformar_em_entidade(model)
            for model in self.sessao.scalars(comando).all()
        ]

    def buscar_por_id(self, profissional_id: int) -> Profissional | None:
        model = self.sessao.get(ProfissionalModel, profissional_id)
        return None if model is None else self.transformar_em_entidade(model)

    def atualizar(self, profissional: Profissional) -> Profissional:
        model = self.sessao.get(ProfissionalModel, profissional.id)
        if model is None:
            raise ValueError("Profissional não encontrado")
        model.nome = profissional.nome
        model.especialidade = profissional.especialidade
        model.ativo = profissional.ativo
        self.sessao.commit()
        self.sessao.refresh(model)
        return self.transformar_em_entidade(model)

    def excluir(self, profissional_id: int) -> bool:
        model = self.sessao.get(ProfissionalModel, profissional_id)
        if model is None:
            return False
        self.sessao.delete(model)
        self.sessao.commit()
        return True
