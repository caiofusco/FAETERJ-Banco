from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database_infrastructure.database import Base


class FilaEsperaModel(Base):
    __tablename__ = "fila_espera"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    cliente_id: Mapped[int] = mapped_column(nullable=False)
    servico_id: Mapped[int] = mapped_column(nullable=False)
    profissional_id: Mapped[int | None] = mapped_column(nullable=True)
    data_solicitada: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False)
