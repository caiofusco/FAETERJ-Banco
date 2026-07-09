from collections.abc import Generator

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.infrastructure.database_infrastructure.database import SessionLocal
from app.application.pacotes_application.atualizar_pacote import AtualizarPacote
from app.application.pacotes_application.buscar_pacote import (
    BuscarPacote,
    PacoteNaoEncontradoError,
)
from app.application.pacotes_application.cadastrar_pacote import CadastrarPacote
from app.application.pacotes_application.excluir_pacote import ExcluirPacote
from app.application.pacotes_application.listar_pacotes import ListarPacotes
from app.infrastructure.pacotes_infrastructure.repositories.pacote_repository_sqlalchemy import (
    PacoteRepositorySQLAlchemy,
)
from app.presentation.pacotes_presentation.schemas.pacote_schema import (
    PacoteAtualizacao,
    PacoteEntrada,
    PacoteSaida,
)


router = APIRouter(prefix="/pacotes", tags=["Pacotes"])


def obter_sessao() -> Generator[Session, None, None]:
    sessao = SessionLocal()
    try:
        yield sessao
    finally:
        sessao.close()


@router.post("", response_model=PacoteSaida, status_code=status.HTTP_201_CREATED)
def cadastrar_pacote(dados: PacoteEntrada, sessao: Session = Depends(obter_sessao)):
    try:
        return CadastrarPacote(PacoteRepositorySQLAlchemy(sessao)).cadastrar(
            nome=dados.nome,
            descricao=dados.descricao,
            valor=dados.valor,
            servicos=dados.servicos,
        )
    except ValueError as erro:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(erro)
        ) from erro


@router.get("", response_model=list[PacoteSaida])
def listar_pacotes(sessao: Session = Depends(obter_sessao)):
    return ListarPacotes(PacoteRepositorySQLAlchemy(sessao)).listar()


@router.get("/{id}", response_model=PacoteSaida)
def buscar_pacote(id: int, sessao: Session = Depends(obter_sessao)):
    try:
        return BuscarPacote(PacoteRepositorySQLAlchemy(sessao)).buscar(id)
    except PacoteNaoEncontradoError as erro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(erro)
        ) from erro


@router.put("/{id}", response_model=PacoteSaida)
def atualizar_pacote(
    id: int, dados: PacoteAtualizacao, sessao: Session = Depends(obter_sessao)
):
    try:
        return AtualizarPacote(PacoteRepositorySQLAlchemy(sessao)).atualizar(
            pacote_id=id,
            nome=dados.nome,
            descricao=dados.descricao,
            valor=dados.valor,
            servicos=dados.servicos,
        )
    except PacoteNaoEncontradoError as erro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(erro)
        ) from erro
    except ValueError as erro:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(erro)
        ) from erro


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_pacote(id: int, sessao: Session = Depends(obter_sessao)):
    try:
        ExcluirPacote(PacoteRepositorySQLAlchemy(sessao)).excluir(id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except PacoteNaoEncontradoError as erro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(erro)
        ) from erro
