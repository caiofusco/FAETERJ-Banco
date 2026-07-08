from collections.abc import Generator

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.database.infrastructure.database import SessionLocal
from app.profissionais.application.atualizar_profissional import AtualizarProfissional
from app.profissionais.application.buscar_profissional import (
    BuscarProfissional,
    ProfissionalNaoEncontradoError,
)
from app.profissionais.application.cadastrar_profissional import CadastrarProfissional
from app.profissionais.application.excluir_profissional import ExcluirProfissional
from app.profissionais.application.listar_profissionais import ListarProfissionais
from app.profissionais.infrastructure.repositories.profissional_repository_sqlalchemy import (
    ProfissionalRepositorySQLAlchemy,
)
from app.profissionais.presentation.schemas.profissional_schema import (
    ProfissionalAtualizacao,
    ProfissionalEntrada,
    ProfissionalSaida,
)


router = APIRouter(prefix="/profissionais", tags=["Profissionais"])


def obter_sessao() -> Generator[Session, None, None]:
    sessao = SessionLocal()
    try:
        yield sessao
    finally:
        sessao.close()


@router.post("", response_model=ProfissionalSaida, status_code=status.HTTP_201_CREATED)
def cadastrar_profissional(
    dados: ProfissionalEntrada, sessao: Session = Depends(obter_sessao)
):
    try:
        return CadastrarProfissional(
            ProfissionalRepositorySQLAlchemy(sessao)
        ).cadastrar(
            nome=dados.nome, especialidade=dados.especialidade, ativo=dados.ativo
        )
    except ValueError as erro:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(erro)
        ) from erro


@router.get("", response_model=list[ProfissionalSaida])
def listar_profissionais(sessao: Session = Depends(obter_sessao)):
    return ListarProfissionais(ProfissionalRepositorySQLAlchemy(sessao)).listar()


@router.get("/{id}", response_model=ProfissionalSaida)
def buscar_profissional(id: int, sessao: Session = Depends(obter_sessao)):
    try:
        return BuscarProfissional(ProfissionalRepositorySQLAlchemy(sessao)).buscar(id)
    except ProfissionalNaoEncontradoError as erro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(erro)
        ) from erro


@router.put("/{id}", response_model=ProfissionalSaida)
def atualizar_profissional(
    id: int, dados: ProfissionalAtualizacao, sessao: Session = Depends(obter_sessao)
):
    try:
        return AtualizarProfissional(
            ProfissionalRepositorySQLAlchemy(sessao)
        ).atualizar(
            profissional_id=id,
            nome=dados.nome,
            especialidade=dados.especialidade,
            ativo=dados.ativo,
        )
    except ProfissionalNaoEncontradoError as erro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(erro)
        ) from erro
    except ValueError as erro:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(erro)
        ) from erro


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_profissional(id: int, sessao: Session = Depends(obter_sessao)):
    try:
        ExcluirProfissional(ProfissionalRepositorySQLAlchemy(sessao)).excluir(id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except ProfissionalNaoEncontradoError as erro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(erro)
        ) from erro
