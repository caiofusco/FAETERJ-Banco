from app.application.pagamentos_application.buscar_pagamento import (
    PagamentoNaoEncontradoError,
)
from app.domain.pagamentos_domain.repositories.pagamento_repository import (
    PagamentoRepository,
)


class ExcluirPagamento:
    def __init__(self, repositorio: PagamentoRepository):
        self.repositorio = repositorio

    def excluir(self, pagamento_id: int) -> None:
        if not self.repositorio.excluir(pagamento_id):
            raise PagamentoNaoEncontradoError("Pagamento não encontrado")
