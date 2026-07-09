from pydantic import BaseModel, Field


class LoginEntrada(BaseModel):
    usuario: str = Field(min_length=1)
    senha: str = Field(min_length=1)


class LoginSaida(BaseModel):
    access_token: str
    token_type: str = "bearer"
