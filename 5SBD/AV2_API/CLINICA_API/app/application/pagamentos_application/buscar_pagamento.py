from app.domain.pagamentos_domain.entities.pagamento import Pagamento
from app.domain.pagamentos_domain.repositories.pagamento_repository import (
    PagamentoRepository,
)


class PagamentoNaoEncontradoError(Exception):
    pass


class BuscarPagamento:
    def __init__(self, repositorio: PagamentoRepository):
        self.repositorio = repositorio

    def buscar(self, pagamento_id: int) -> Pagamento:
        pagamento = self.repositorio.buscar_por_id(pagamento_id)
        if pagamento is None:
            raise PagamentoNaoEncontradoError("Pagamento não encontrado")
        return pagamento
