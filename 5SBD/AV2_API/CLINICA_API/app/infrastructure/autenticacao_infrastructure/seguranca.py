import os
from secrets import compare_digest

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer


seguranca = HTTPBearer()


def usuario_padrao() -> str:
    return os.getenv("USUARIO_API", "admin")


def senha_padrao() -> str:
    return os.getenv("SENHA_API", "123456")


def token_padrao() -> str:
    return os.getenv("TOKEN_API", "token-av2-sbd")


def conferir_login(usuario: str, senha: str) -> bool:
    usuario_correto = compare_digest(usuario, usuario_padrao())
    senha_correta = compare_digest(senha, senha_padrao())
    return usuario_correto and senha_correta


def verificar_token(credenciais: HTTPAuthorizationCredentials = Depends(seguranca)):
    token_recebido = credenciais.credentials

    if not compare_digest(token_recebido, token_padrao()):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalido ou nao informado",
        )
