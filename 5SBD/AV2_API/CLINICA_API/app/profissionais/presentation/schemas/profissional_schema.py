from pydantic import BaseModel, ConfigDict, Field


class ProfissionalEntrada(BaseModel):
    nome: str = Field(min_length=1, max_length=100)
    especialidade: str = Field(min_length=1, max_length=100)
    ativo: bool = True


class ProfissionalAtualizacao(ProfissionalEntrada):
    pass


class ProfissionalSaida(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    especialidade: str
    ativo: bool
