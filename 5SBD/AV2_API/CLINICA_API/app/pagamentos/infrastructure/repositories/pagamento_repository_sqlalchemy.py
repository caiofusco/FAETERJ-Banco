from sqlalchemy import select
from sqlalchemy.orm import Session

from app.pagamentos.domain.entities.pagamento import (
    MetodoPagamento,
    Pagamento,
    StatusPagamento,
)
from app.pagamentos.domain.repositories.pagamento_repository import PagamentoRepository
from app.pagamentos.infrastructure.models.pagamento_model import PagamentoModel


class PagamentoRepositorySQLAlchemy(PagamentoRepository):
    def __init__(self, sessao: Session):
        self.sessao = sessao

    @staticmethod
    def transformar_em_entidade(model: PagamentoModel) -> Pagamento:
        return Pagamento(
            id=model.id,
            reserva_id=model.reserva_id,
            valor=model.valor,
            metodo=MetodoPagamento(model.metodo),
            status=StatusPagamento(model.status),
            data_pagamento=model.data_pagamento,
        )

    def salvar(self, pagamento: Pagamento) -> Pagamento:
        model = PagamentoModel(
            reserva_id=pagamento.reserva_id,
            valor=pagamento.valor,
            metodo=pagamento.metodo.value,
            status=pagamento.status.value,
            data_pagamento=pagamento.data_pagamento,
        )
        self.sessao.add(model)
        self.sessao.commit()
        self.sessao.refresh(model)
        return self.transformar_em_entidade(model)

    def listar(self) -> list[Pagamento]:
        comando = select(PagamentoModel).order_by(PagamentoModel.id)
        return [
            self.transformar_em_entidade(model)
            for model in self.sessao.scalars(comando).all()
        ]

    def buscar_por_id(self, pagamento_id: int) -> Pagamento | None:
        model = self.sessao.get(PagamentoModel, pagamento_id)
        return None if model is None else self.transformar_em_entidade(model)

    def atualizar(self, pagamento: Pagamento) -> Pagamento:
        model = self.sessao.get(PagamentoModel, pagamento.id)
        if model is None:
            raise ValueError("Pagamento não encontrado")
        model.reserva_id = pagamento.reserva_id
        model.valor = pagamento.valor
        model.metodo = pagamento.metodo.value
        model.status = pagamento.status.value
        model.data_pagamento = pagamento.data_pagamento
        self.sessao.commit()
        self.sessao.refresh(model)
        return self.transformar_em_entidade(model)

    def excluir(self, pagamento_id: int) -> bool:
        model = self.sessao.get(PagamentoModel, pagamento_id)
        if model is None:
            return False
        self.sessao.delete(model)
        self.sessao.commit()
        return True
