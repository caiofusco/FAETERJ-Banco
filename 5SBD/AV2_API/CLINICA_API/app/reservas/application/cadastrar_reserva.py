from datetime import datetime

from app.reservas.domain.entities.reserva import Reserva, StatusReserva
from app.reservas.domain.repositories.reserva_repository import ReservaRepository


class CadastrarReserva:
    def __init__(self, repositorio: ReservaRepository):
        self.repositorio = repositorio

    def cadastrar(
        self,
        cliente_id: int,
        profissional_id: int,
        data_hora: datetime,
        status: StatusReserva,
        valor_total: float,
        servico_id: int | None = None,
        pacote_id: int | None = None,
    ) -> Reserva:
        reserva = Reserva(
            cliente_id=cliente_id,
            profissional_id=profissional_id,
            data_hora=data_hora,
            status=status,
            valor_total=valor_total,
            servico_id=servico_id,
            pacote_id=pacote_id,
        )
        return self.repositorio.salvar(reserva)
