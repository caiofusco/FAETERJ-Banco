from pydantic import BaseModel, ConfigDict, Field


class ClienteEntrada(BaseModel):
    nome: str = Field(min_length=1, max_length=100)
    email: str = Field(min_length=3, max_length=150)
    telefone: str = Field(min_length=1, max_length=30)
    credito: float = Field(default=0, ge=0)


class ClienteAtualizacao(ClienteEntrada):
    pass


class ClienteSaida(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    email: str
    telefone: str
    credito: float
