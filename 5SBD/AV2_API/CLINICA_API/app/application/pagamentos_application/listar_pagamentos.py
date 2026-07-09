from app.domain.pagamentos_domain.entities.pagamento import Pagamento
from app.domain.pagamentos_domain.repositories.pagamento_repository import (
    PagamentoRepository,
)


class ListarPagamentos:
    def __init__(self, repositorio: PagamentoRepository):
        self.repositorio = repositorio

    def listar(self) -> list[Pagamento]:
        return self.repositorio.listar()
