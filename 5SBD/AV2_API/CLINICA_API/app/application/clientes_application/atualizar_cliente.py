from app.application.clientes_application.buscar_cliente import (
    ClienteNaoEncontradoError,
)
from app.domain.clientes_domain.entities.cliente import Cliente
from app.domain.clientes_domain.repositories.cliente_repository import ClienteRepository


class AtualizarCliente:
    def __init__(self, repositorio: ClienteRepository):
        self.repositorio = repositorio

    def atualizar(
        self,
        cliente_id: int,
        nome: str,
        email: str,
        telefone: str,
        credito: float,
    ) -> Cliente:
        cliente = self.repositorio.buscar_por_id(cliente_id)
        if cliente is None:
            raise ClienteNaoEncontradoError("Cliente não encontrado")
        cliente.atualizar(nome=nome, email=email, telefone=telefone, credito=credito)
        return self.repositorio.atualizar(cliente)
