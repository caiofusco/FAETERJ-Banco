from app.clientes.domain.entities.cliente import Cliente
from app.clientes.domain.repositories.cliente_repository import ClienteRepository


class ClienteNaoEncontradoError(Exception):
    pass


class BuscarCliente:
    def __init__(self, repositorio: ClienteRepository):
        self.repositorio = repositorio

    def buscar(self, cliente_id: int) -> Cliente:
        cliente = self.repositorio.buscar_por_id(cliente_id)
        if cliente is None:
            raise ClienteNaoEncontradoError("Cliente não encontrado")
        return cliente
