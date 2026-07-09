from app.domain.clientes_domain.entities.cliente import Cliente
from app.domain.clientes_domain.repositories.cliente_repository import ClienteRepository


class CadastrarCliente:
    def __init__(self, repositorio: ClienteRepository):
        self.repositorio = repositorio

    def cadastrar(
        self, nome: str, email: str, telefone: str, credito: float = 0
    ) -> Cliente:
        cliente = Cliente(nome=nome, email=email, telefone=telefone, credito=credito)
        return self.repositorio.salvar(cliente)
