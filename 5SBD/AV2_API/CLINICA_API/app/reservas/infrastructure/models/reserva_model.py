from datetime import datetime

from sqlalchemy import DateTime, Float, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.infrastructure.database import Base


class ReservaModel(Base):
    __tablename__ = "reservas"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    cliente_id: Mapped[int] = mapped_column(nullable=False)
    profissional_id: Mapped[int] = mapped_column(nullable=False)
    servico_id: Mapped[int | None] = mapped_column(nullable=True)
    pacote_id: Mapped[int | None] = mapped_column(nullable=True)
    data_hora: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False)
    valor_total: Mapped[float] = mapped_column(Float, nullable=False)
