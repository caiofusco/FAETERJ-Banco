from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.clientes_domain.entities.cliente import Cliente
from app.domain.clientes_domain.repositories.cliente_repository import ClienteRepository
from app.infrastructure.clientes_infrastructure.models.cliente_model import ClienteModel


class ClienteRepositorySQLAlchemy(ClienteRepository):
    def __init__(self, sessao: Session):
        self.sessao = sessao

    @staticmethod
    def transformar_em_entidade(cliente_banco: ClienteModel) -> Cliente:
        return Cliente(
            id=cliente_banco.id,
            nome=cliente_banco.nome,
            email=cliente_banco.email,
            telefone=cliente_banco.telefone,
            credito=cliente_banco.credito,
        )

    def salvar(self, cliente: Cliente) -> Cliente:
        cliente_banco = ClienteModel(
            nome=cliente.nome,
            email=cliente.email,
            telefone=cliente.telefone,
            credito=cliente.credito,
        )
        self.sessao.add(cliente_banco)
        self.sessao.commit()
        self.sessao.refresh(cliente_banco)
        return self.transformar_em_entidade(cliente_banco)

    def listar(self) -> list[Cliente]:
        comando = select(ClienteModel).order_by(ClienteModel.id)
        return [
            self.transformar_em_entidade(item)
            for item in self.sessao.scalars(comando).all()
        ]

    def buscar_por_id(self, cliente_id: int) -> Cliente | None:
        cliente_banco = self.sessao.get(ClienteModel, cliente_id)
        return (
            None
            if cliente_banco is None
            else self.transformar_em_entidade(cliente_banco)
        )

    def atualizar(self, cliente: Cliente) -> Cliente:
        cliente_banco = self.sessao.get(ClienteModel, cliente.id)
        if cliente_banco is None:
            raise ValueError("Cliente não encontrado")
        cliente_banco.nome = cliente.nome
        cliente_banco.email = cliente.email
        cliente_banco.telefone = cliente.telefone
        cliente_banco.credito = cliente.credito
        self.sessao.commit()
        self.sessao.refresh(cliente_banco)
        return self.transformar_em_entidade(cliente_banco)

    def excluir(self, cliente_id: int) -> bool:
        cliente_banco = self.sessao.get(ClienteModel, cliente_id)
        if cliente_banco is None:
            return False
        self.sessao.delete(cliente_banco)
        self.sessao.commit()
        return True
