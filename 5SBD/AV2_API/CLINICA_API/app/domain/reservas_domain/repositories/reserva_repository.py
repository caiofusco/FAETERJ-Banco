from abc import ABC, abstractmethod

from app.domain.reservas_domain.entities.reserva import Reserva


class ReservaRepository(ABC):
    @abstractmethod
    def salvar(self, reserva: Reserva) -> Reserva:
        pass

    @abstractmethod
    def listar(self) -> list[Reserva]:
        pass

    @abstractmethod
    def buscar_por_id(self, reserva_id: int) -> Reserva | None:
        pass

    @abstractmethod
    def atualizar(self, reserva: Reserva) -> Reserva:
        pass

    @abstractmethod
    def excluir(self, reserva_id: int) -> bool:
        pass
