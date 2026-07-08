from collections.abc import Generator

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.clientes.application.atualizar_cliente import AtualizarCliente
from app.clientes.application.buscar_cliente import (
    BuscarCliente,
    ClienteNaoEncontradoError,
)
from app.clientes.application.cadastrar_cliente import CadastrarCliente
from app.clientes.application.excluir_cliente import ExcluirCliente
from app.clientes.application.listar_clientes import ListarClientes
from app.clientes.infrastructure.repositories.cliente_repository_sqlalchemy import (
    ClienteRepositorySQLAlchemy,
)
from app.clientes.presentation.schemas.cliente_schema import (
    ClienteAtualizacao,
    ClienteEntrada,
    ClienteSaida,
)
from app.database.infrastructure.database import SessionLocal


router = APIRouter(prefix="/clientes", tags=["Clientes"])


def obter_sessao() -> Generator[Session, None, None]:
    sessao = SessionLocal()
    try:
        yield sessao
    finally:
        sessao.close()


@router.post("", response_model=ClienteSaida, status_code=status.HTTP_201_CREATED)
def cadastrar_cliente(dados: ClienteEntrada, sessao: Session = Depends(obter_sessao)):
    try:
        return CadastrarCliente(ClienteRepositorySQLAlchemy(sessao)).cadastrar(
            nome=dados.nome,
            email=dados.email,
            telefone=dados.telefone,
            credito=dados.credito,
        )
    except ValueError as erro:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(erro)
        ) from erro


@router.get("", response_model=list[ClienteSaida])
def listar_clientes(sessao: Session = Depends(obter_sessao)):
    return ListarClientes(ClienteRepositorySQLAlchemy(sessao)).listar()


@router.get("/{id}", response_model=ClienteSaida)
def buscar_cliente(id: int, sessao: Session = Depends(obter_sessao)):
    try:
        return BuscarCliente(ClienteRepositorySQLAlchemy(sessao)).buscar(id)
    except ClienteNaoEncontradoError as erro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(erro)
        ) from erro


@router.put("/{id}", response_model=ClienteSaida)
def atualizar_cliente(
    id: int, dados: ClienteAtualizacao, sessao: Session = Depends(obter_sessao)
):
    try:
        return AtualizarCliente(ClienteRepositorySQLAlchemy(sessao)).atualizar(
            cliente_id=id,
            nome=dados.nome,
            email=dados.email,
            telefone=dados.telefone,
            credito=dados.credito,
        )
    except ClienteNaoEncontradoError as erro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(erro)
        ) from erro
    except ValueError as erro:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(erro)
        ) from erro


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_cliente(id: int, sessao: Session = Depends(obter_sessao)):
    try:
        ExcluirCliente(ClienteRepositorySQLAlchemy(sessao)).excluir(id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except ClienteNaoEncontradoError as erro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(erro)
        ) from erro
