from sqlalchemy import Float, String
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database_infrastructure.database import Base


class ClienteModel(Base):
    __tablename__ = "clientes"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(150), nullable=False)
    telefone: Mapped[str] = mapped_column(String(30), nullable=False)
    credito: Mapped[float] = mapped_column(Float, nullable=False, default=0)
