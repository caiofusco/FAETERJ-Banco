from datetime import datetime

from app.application.reservas_application.buscar_reserva import (
    ReservaNaoEncontradaError,
)
from app.domain.reservas_domain.entities.reserva import Reserva, StatusReserva
from app.domain.reservas_domain.repositories.reserva_repository import ReservaRepository


class AtualizarReserva:
    def __init__(self, repositorio: ReservaRepository):
        self.repositorio = repositorio

    def atualizar(
        self,
        reserva_id: int,
        cliente_id: int,
        profissional_id: int,
        data_hora: datetime,
        status: StatusReserva,
        valor_total: float,
        servico_id: int | None,
        pacote_id: int | None,
    ) -> Reserva:
        reserva = self.repositorio.buscar_por_id(reserva_id)
        if reserva is None:
            raise ReservaNaoEncontradaError("Reserva não encontrada")
        reserva.atualizar(
            cliente_id=cliente_id,
            profissional_id=profissional_id,
            data_hora=data_hora,
            status=status,
            valor_total=valor_total,
            servico_id=servico_id,
            pacote_id=pacote_id,
        )
        return self.repositorio.atualizar(reserva)
