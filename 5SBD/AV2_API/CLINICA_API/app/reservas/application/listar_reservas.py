from app.reservas.domain.entities.reserva import Reserva
from app.reservas.domain.repositories.reserva_repository import ReservaRepository


class ListarReservas:
    def __init__(self, repositorio: ReservaRepository):
        self.repositorio = repositorio

    def listar(self) -> list[Reserva]:
        return self.repositorio.listar()
