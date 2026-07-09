from abc import ABC, abstractmethod

from app.domain.clientes_domain.entities.cliente import Cliente


class ClienteRepository(ABC):
    @abstractmethod
    def salvar(self, cliente: Cliente) -> Cliente:
        pass

    @abstractmethod
    def listar(self) -> list[Cliente]:
        pass

    @abstractmethod
    def buscar_por_id(self, cliente_id: int) -> Cliente | None:
        pass

    @abstractmethod
    def atualizar(self, cliente: Cliente) -> Cliente:
        pass

    @abstractmethod
    def excluir(self, cliente_id: int) -> bool:
        pass
