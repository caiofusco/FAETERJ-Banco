from pydantic import BaseModel, ConfigDict, Field


class ServicoEntrada(BaseModel):
    nome: str = Field(min_length=1, max_length=100)
    descricao: str = Field(min_length=1, max_length=500)
    especialidade: str = Field(min_length=1, max_length=100)
    valor: float = Field(gt=0)
    duracao_minutos: int = Field(gt=0)


class ServicoAtualizacao(ServicoEntrada):
    pass


class ServicoSaida(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    descricao: str
    especialidade: str
    valor: float
    duracao_minutos: int
