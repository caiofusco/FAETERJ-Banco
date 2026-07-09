from app.domain.reservas_domain.entities.reserva import Reserva
from app.domain.reservas_domain.repositories.reserva_repository import ReservaRepository


class ReservaNaoEncontradaError(Exception):
    pass


class BuscarReserva:
    def __init__(self, repositorio: ReservaRepository):
        self.repositorio = repositorio

    def buscar(self, reserva_id: int) -> Reserva:
        reserva = self.repositorio.buscar_por_id(reserva_id)
        if reserva is None:
            raise ReservaNaoEncontradaError("Reserva não encontrada")
        return reserva
