from datetime import datetime

from app.pagamentos.domain.entities.pagamento import (
    MetodoPagamento,
    Pagamento,
    StatusPagamento,
)
from app.pagamentos.domain.repositories.pagamento_repository import PagamentoRepository


class CadastrarPagamento:
    def __init__(self, repositorio: PagamentoRepository):
        self.repositorio = repositorio

    def cadastrar(
        self,
        reserva_id: int,
        valor: float,
        metodo: MetodoPagamento = MetodoPagamento.CARTAO_CREDITO,
        status: StatusPagamento = StatusPagamento.PENDENTE,
        data_pagamento: datetime | None = None,
    ) -> Pagamento:
        pagamento = Pagamento(
            reserva_id=reserva_id,
            valor=valor,
            metodo=metodo,
            status=status,
            data_pagamento=data_pagamento,
        )
        return self.repositorio.salvar(pagamento)
