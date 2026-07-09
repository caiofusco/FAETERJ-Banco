from app.application.clientes_application.buscar_cliente import (
    ClienteNaoEncontradoError,
)
from app.domain.clientes_domain.repositories.cliente_repository import ClienteRepository


class ExcluirCliente:
    def __init__(self, repositorio: ClienteRepository):
        self.repositorio = repositorio

    def excluir(self, cliente_id: int) -> None:
        if not self.repositorio.excluir(cliente_id):
            raise ClienteNaoEncontradoError("Cliente não encontrado")
