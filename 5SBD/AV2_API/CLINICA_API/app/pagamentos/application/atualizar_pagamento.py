from datetime import datetime

from app.pagamentos.application.buscar_pagamento import PagamentoNaoEncontradoError
from app.pagamentos.domain.entities.pagamento import (
    MetodoPagamento,
    Pagamento,
    StatusPagamento,
)
from app.pagamentos.domain.repositories.pagamento_repository import PagamentoRepository


class AtualizarPagamento:
    def __init__(self, repositorio: PagamentoRepository):
        self.repositorio = repositorio

    def atualizar(
        self,
        pagamento_id: int,
        reserva_id: int,
        valor: float,
        metodo: MetodoPagamento,
        status: StatusPagamento,
        data_pagamento: datetime | None,
    ) -> Pagamento:
        pagamento = self.repositorio.buscar_por_id(pagamento_id)
        if pagamento is None:
            raise PagamentoNaoEncontradoError("Pagamento não encontrado")
        pagamento.atualizar(
            reserva_id=reserva_id,
            valor=valor,
            metodo=metodo,
            status=status,
            data_pagamento=data_pagamento,
        )
        return self.repositorio.atualizar(pagamento)
