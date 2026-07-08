from app.pagamentos.domain.entities.pagamento import Pagamento
from app.pagamentos.domain.repositories.pagamento_repository import PagamentoRepository


class ListarPagamentos:
    def __init__(self, repositorio: PagamentoRepository):
        self.repositorio = repositorio

    def listar(self) -> list[Pagamento]:
        return self.repositorio.listar()
