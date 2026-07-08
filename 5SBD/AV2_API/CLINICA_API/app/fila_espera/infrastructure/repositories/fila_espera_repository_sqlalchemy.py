from sqlalchemy import select
from sqlalchemy.orm import Session

from app.fila_espera.domain.entities.fila_espera import FilaEspera, StatusFilaEspera
from app.fila_espera.domain.repositories.fila_espera_repository import (
    FilaEsperaRepository,
)
from app.fila_espera.infrastructure.models.fila_espera_model import FilaEsperaModel


class FilaEsperaRepositorySQLAlchemy(FilaEsperaRepository):
    def __init__(self, sessao: Session):
        self.sessao = sessao

    @staticmethod
    def transformar_em_entidade(model: FilaEsperaModel) -> FilaEspera:
        return FilaEspera(
            id=model.id,
            cliente_id=model.cliente_id,
            servico_id=model.servico_id,
            profissional_id=model.profissional_id,
            data_solicitada=model.data_solicitada,
            status=StatusFilaEspera(model.status),
        )

    def salvar(self, registro: FilaEspera) -> FilaEspera:
        model = FilaEsperaModel(
            cliente_id=registro.cliente_id,
            servico_id=registro.servico_id,
            profissional_id=registro.profissional_id,
            data_solicitada=registro.data_solicitada,
            status=registro.status.value,
        )
        self.sessao.add(model)
        self.sessao.commit()
        self.sessao.refresh(model)
        return self.transformar_em_entidade(model)

    def listar(self) -> list[FilaEspera]:
        comando = select(FilaEsperaModel).order_by(FilaEsperaModel.id)
        return [
            self.transformar_em_entidade(model)
            for model in self.sessao.scalars(comando).all()
        ]

    def buscar_por_id(self, registro_id: int) -> FilaEspera | None:
        model = self.sessao.get(FilaEsperaModel, registro_id)
        return None if model is None else self.transformar_em_entidade(model)

    def atualizar(self, registro: FilaEspera) -> FilaEspera:
        model = self.sessao.get(FilaEsperaModel, registro.id)
        if model is None:
            raise ValueError("Registro da fila de espera não encontrado")
        model.cliente_id = registro.cliente_id
        model.servico_id = registro.servico_id
        model.profissional_id = registro.profissional_id
        model.data_solicitada = registro.data_solicitada
        model.status = registro.status.value
        self.sessao.commit()
        self.sessao.refresh(model)
        return self.transformar_em_entidade(model)

    def excluir(self, registro_id: int) -> bool:
        model = self.sessao.get(FilaEsperaModel, registro_id)
        if model is None:
            return False
        self.sessao.delete(model)
        self.sessao.commit()
        return True
