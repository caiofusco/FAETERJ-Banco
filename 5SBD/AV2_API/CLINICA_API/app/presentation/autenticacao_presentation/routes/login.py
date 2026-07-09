from fastapi import APIRouter, HTTPException, status

from app.presentation.autenticacao_presentation.schemas.login_schema import (
    LoginEntrada,
    LoginSaida,
)
from app.infrastructure.autenticacao_infrastructure.seguranca import (
    conferir_login,
    token_padrao,
)


router = APIRouter(tags=["Login"])


@router.post("/login", response_model=LoginSaida)
def fazer_login(dados: LoginEntrada):
    if not conferir_login(dados.usuario, dados.senha):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario ou senha invalidos",
        )

    return LoginSaida(access_token=token_padrao())
