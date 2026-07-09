from abc import ABC, abstractmethod

from app.domain.profissionais_domain.entities.profissional import Profissional


class ProfissionalRepository(ABC):
    @abstractmethod
    def salvar(self, profissional: Profissional) -> Profissional:
        pass

    @abstractmethod
    def listar(self) -> list[Profissional]:
        pass

    @abstractmethod
    def buscar_por_id(self, profissional_id: int) -> Profissional | None:
        pass

    @abstractmethod
    def atualizar(self, profissional: Profissional) -> Profissional:
        pass

    @abstractmethod
    def excluir(self, profissional_id: int) -> bool:
        pass
