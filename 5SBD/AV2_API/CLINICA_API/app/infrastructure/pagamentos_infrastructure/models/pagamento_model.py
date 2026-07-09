from datetime import datetime

from sqlalchemy import DateTime, Float, String
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database_infrastructure.database import Base


class PagamentoModel(Base):
    __tablename__ = "pagamentos"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    reserva_id: Mapped[int] = mapped_column(nullable=False)
    valor: Mapped[float] = mapped_column(Float, nullable=False)
    metodo: Mapped[str] = mapped_column(String(30), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False)
    data_pagamento: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
