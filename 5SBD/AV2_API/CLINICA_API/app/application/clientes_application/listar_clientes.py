from app.domain.clientes_domain.entities.cliente import Cliente
from app.domain.clientes_domain.repositories.cliente_repository import ClienteRepository


class ListarClientes:
    def __init__(self, repositorio: ClienteRepository):
        self.repositorio = repositorio

    def listar(self) -> list[Cliente]:
        return self.repositorio.listar()
