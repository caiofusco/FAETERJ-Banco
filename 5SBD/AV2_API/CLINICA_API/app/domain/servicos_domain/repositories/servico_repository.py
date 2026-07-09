from abc import ABC, abstractmethod

from app.domain.servicos_domain.entities.servico import Servico


class ServicoRepository(ABC):
    @abstractmethod
    def salvar(self, servico: Servico) -> Servico:
        pass

    @abstractmethod
    def listar(self) -> list[Servico]:
        pass

    @abstractmethod
    def buscar_por_id(self, servico_id: int) -> Servico | None:
        pass

    @abstractmethod
    def atualizar(self, servico: Servico) -> Servico:
        pass

    @abstractmethod
    def excluir(self, servico_id: int) -> bool:
        pass
