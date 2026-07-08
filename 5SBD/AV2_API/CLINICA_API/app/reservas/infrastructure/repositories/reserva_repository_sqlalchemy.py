from sqlalchemy import select
from sqlalchemy.orm import Session

from app.reservas.domain.entities.reserva import Reserva, StatusReserva
from app.reservas.domain.repositories.reserva_repository import ReservaRepository
from app.reservas.infrastructure.models.reserva_model import ReservaModel


class ReservaRepositorySQLAlchemy(ReservaRepository):
    def __init__(self, sessao: Session):
        self.sessao = sessao

    @staticmethod
    def transformar_em_entidade(model: ReservaModel) -> Reserva:
        return Reserva(
            id=model.id,
            cliente_id=model.cliente_id,
            profissional_id=model.profissional_id,
            servico_id=model.servico_id,
            pacote_id=model.pacote_id,
            data_hora=model.data_hora,
            status=StatusReserva(model.status),
            valor_total=model.valor_total,
        )

    def salvar(self, reserva: Reserva) -> Reserva:
        model = ReservaModel(
            cliente_id=reserva.cliente_id,
            profissional_id=reserva.profissional_id,
            servico_id=reserva.servico_id,
            pacote_id=reserva.pacote_id,
            data_hora=reserva.data_hora,
            status=reserva.status.value,
            valor_total=reserva.valor_total,
        )
        self.sessao.add(model)
        self.sessao.commit()
        self.sessao.refresh(model)
        return self.transformar_em_entidade(model)

    def listar(self) -> list[Reserva]:
        comando = select(ReservaModel).order_by(ReservaModel.id)
        return [
            self.transformar_em_entidade(model)
            for model in self.sessao.scalars(comando).all()
        ]

    def buscar_por_id(self, reserva_id: int) -> Reserva | None:
        model = self.sessao.get(ReservaModel, reserva_id)
        return None if model is None else self.transformar_em_entidade(model)

    def atualizar(self, reserva: Reserva) -> Reserva:
        model = self.sessao.get(ReservaModel, reserva.id)
        if model is None:
            raise ValueError("Reserva não encontrada")
        model.cliente_id = reserva.cliente_id
        model.profissional_id = reserva.profissional_id
        model.servico_id = reserva.servico_id
        model.pacote_id = reserva.pacote_id
        model.data_hora = reserva.data_hora
        model.status = reserva.status.value
        model.valor_total = reserva.valor_total
        self.sessao.commit()
        self.sessao.refresh(model)
        return self.transformar_em_entidade(model)

    def excluir(self, reserva_id: int) -> bool:
        model = self.sessao.get(ReservaModel, reserva_id)
        if model is None:
            return False
        self.sessao.delete(model)
        self.sessao.commit()
        return True
