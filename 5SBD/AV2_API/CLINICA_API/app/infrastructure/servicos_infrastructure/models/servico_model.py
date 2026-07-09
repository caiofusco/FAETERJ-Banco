from sqlalchemy import Float, String
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database_infrastructure.database import Base


class ServicoModel(Base):
    __tablename__ = "servicos"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    descricao: Mapped[str] = mapped_column(String(500), nullable=False)
    especialidade: Mapped[str] = mapped_column(String(100), nullable=False)
    valor: Mapped[float] = mapped_column(Float, nullable=False)
    duracao_minutos: Mapped[int] = mapped_column(nullable=False)
