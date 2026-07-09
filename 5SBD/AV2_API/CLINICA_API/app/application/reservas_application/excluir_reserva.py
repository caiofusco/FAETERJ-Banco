from app.application.reservas_application.buscar_reserva import (
    ReservaNaoEncontradaError,
)
from app.domain.reservas_domain.repositories.reserva_repository import ReservaRepository


class ExcluirReserva:
    def __init__(self, repositorio: ReservaRepository):
        self.repositorio = repositorio

    def excluir(self, reserva_id: int) -> None:
        if not self.repositorio.excluir(reserva_id):
            raise ReservaNaoEncontradaError("Reserva não encontrada")
