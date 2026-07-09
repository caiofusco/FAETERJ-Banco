from sqlalchemy import Float, JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database_infrastructure.database import Base


class PacoteModel(Base):
    __tablename__ = "pacotes"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    descricao: Mapped[str] = mapped_column(String(500), nullable=False)
    valor: Mapped[float] = mapped_column(Float, nullable=False)
    servicos: Mapped[list[int]] = mapped_column(JSON, nullable=False, default=list)
