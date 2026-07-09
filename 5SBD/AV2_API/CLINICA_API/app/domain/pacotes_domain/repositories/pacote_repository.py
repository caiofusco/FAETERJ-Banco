from abc import ABC, abstractmethod

from app.domain.pacotes_domain.entities.pacote import Pacote


class PacoteRepository(ABC):
    @abstractmethod
    def salvar(self, pacote: Pacote) -> Pacote:
        pass

    @abstractmethod
    def listar(self) -> list[Pacote]:
        pass

    @abstractmethod
    def buscar_por_id(self, pacote_id: int) -> Pacote | None:
        pass

    @abstractmethod
    def atualizar(self, pacote: Pacote) -> Pacote:
        pass

    @abstractmethod
    def excluir(self, pacote_id: int) -> bool:
        pass
