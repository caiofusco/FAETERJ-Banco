from collections.abc import Generator

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.database.infrastructure.database import SessionLocal
from app.fila_espera.application.atualizar_fila_espera import AtualizarFilaEspera
from app.fila_espera.application.buscar_fila_espera import (
    BuscarFilaEspera,
    FilaEsperaNaoEncontradaError,
)
from app.fila_espera.application.cadastrar_fila_espera import CadastrarFilaEspera
from app.fila_espera.application.excluir_fila_espera import ExcluirFilaEspera
from app.fila_espera.application.listar_fila_espera import ListarFilaEspera
from app.fila_espera.infrastructure.repositories.fila_espera_repository_sqlalchemy import (
    FilaEsperaRepositorySQLAlchemy,
)
from app.fila_espera.presentation.schemas.fila_espera_schema import (
    FilaEsperaAtualizacao,
    FilaEsperaEntrada,
    FilaEsperaSaida,
)


router = APIRouter(prefix="/fila-espera", tags=["Fila de espera"])


def obter_sessao() -> Generator[Session, None, None]:
    sessao = SessionLocal()
    try:
        yield sessao
    finally:
        sessao.close()


@router.post("", response_model=FilaEsperaSaida, status_code=status.HTTP_201_CREATED)
def cadastrar_registro(
    dados: FilaEsperaEntrada, sessao: Session = Depends(obter_sessao)
):
    try:
        repositorio = FilaEsperaRepositorySQLAlchemy(sessao)
        caso_de_uso = CadastrarFilaEspera(repositorio)

        return caso_de_uso.cadastrar(
            cliente_id=dados.cliente_id,
            servico_id=dados.servico_id,
            profissional_id=dados.profissional_id,
            data_solicitada=dados.data_solicitada,
            status=dados.status,
        )
    except ValueError as erro:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(erro)
        ) from erro


@router.get("", response_model=list[FilaEsperaSaida])
def listar_registros(sessao: Session = Depends(obter_sessao)):
    repositorio = FilaEsperaRepositorySQLAlchemy(sessao)
    caso_de_uso = ListarFilaEspera(repositorio)
    return caso_de_uso.listar()


@router.get("/{id}", response_model=FilaEsperaSaida)
def buscar_registro(id: int, sessao: Session = Depends(obter_sessao)):
    try:
        repositorio = FilaEsperaRepositorySQLAlchemy(sessao)
        caso_de_uso = BuscarFilaEspera(repositorio)
        return caso_de_uso.buscar(id)
    except FilaEsperaNaoEncontradaError as erro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(erro)
        ) from erro


@router.put("/{id}", response_model=FilaEsperaSaida)
def atualizar_registro(
    id: int, dados: FilaEsperaAtualizacao, sessao: Session = Depends(obter_sessao)
):
    try:
        repositorio = FilaEsperaRepositorySQLAlchemy(sessao)
        caso_de_uso = AtualizarFilaEspera(repositorio)

        return caso_de_uso.atualizar(
            registro_id=id,
            cliente_id=dados.cliente_id,
            servico_id=dados.servico_id,
            profissional_id=dados.profissional_id,
            data_solicitada=dados.data_solicitada,
            status=dados.status,
        )
    except FilaEsperaNaoEncontradaError as erro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(erro)
        ) from erro
    except ValueError as erro:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(erro)
        ) from erro


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_registro(id: int, sessao: Session = Depends(obter_sessao)):
    try:
        repositorio = FilaEsperaRepositorySQLAlchemy(sessao)
        caso_de_uso = ExcluirFilaEspera(repositorio)
        caso_de_uso.excluir(id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except FilaEsperaNaoEncontradaError as erro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(erro)
        ) from erro
