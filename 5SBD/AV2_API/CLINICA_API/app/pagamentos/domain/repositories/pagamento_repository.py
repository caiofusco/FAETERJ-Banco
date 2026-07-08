from abc import ABC, abstractmethod

from app.pagamentos.domain.entities.pagamento import Pagamento


class PagamentoRepository(ABC):
    @abstractmethod
    def salvar(self, pagamento: Pagamento) -> Pagamento:
        pass

    @abstractmethod
    def listar(self) -> list[Pagamento]:
        pass

    @abstractmethod
    def buscar_por_id(self, pagamento_id: int) -> Pagamento | None:
        pass

    @abstractmethod
    def atualizar(self, pagamento: Pagamento) -> Pagamento:
        pass

    @abstractmethod
    def excluir(self, pagamento_id: int) -> bool:
        pass
