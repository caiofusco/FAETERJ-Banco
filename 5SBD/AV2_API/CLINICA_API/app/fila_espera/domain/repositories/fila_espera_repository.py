from abc import ABC, abstractmethod

from app.fila_espera.domain.entities.fila_espera import FilaEspera


class FilaEsperaRepository(ABC):
    @abstractmethod
    def salvar(self, registro: FilaEspera) -> FilaEspera:
        pass

    @abstractmethod
    def listar(self) -> list[FilaEspera]:
        pass

    @abstractmethod
    def buscar_por_id(self, registro_id: int) -> FilaEspera | None:
        pass

    @abstractmethod
    def atualizar(self, registro: FilaEspera) -> FilaEspera:
        pass

    @abstractmethod
    def excluir(self, registro_id: int) -> bool:
        pass
