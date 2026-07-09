from pydantic import BaseModel, ConfigDict, Field


class PacoteEntrada(BaseModel):
    nome: str = Field(min_length=1, max_length=100)
    descricao: str = Field(min_length=1, max_length=500)
    valor: float = Field(gt=0)
    servicos: list[int] = Field(default_factory=list)


class PacoteAtualizacao(PacoteEntrada):
    pass


class PacoteSaida(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    descricao: str
    valor: float
    servicos: list[int]
