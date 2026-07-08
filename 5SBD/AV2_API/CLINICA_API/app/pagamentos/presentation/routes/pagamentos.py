from collections.abc import Generator

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.database.infrastructure.database import SessionLocal
from app.pagamentos.application.atualizar_pagamento import AtualizarPagamento
from app.pagamentos.application.buscar_pagamento import (
    BuscarPagamento,
    PagamentoNaoEncontradoError,
)
from app.pagamentos.application.cadastrar_pagamento import CadastrarPagamento
from app.pagamentos.application.excluir_pagamento import ExcluirPagamento
from app.pagamentos.application.listar_pagamentos import ListarPagamentos
from app.pagamentos.infrastructure.repositories.pagamento_repository_sqlalchemy import (
    PagamentoRepositorySQLAlchemy,
)
from app.pagamentos.presentation.schemas.pagamento_schema import (
    PagamentoAtualizacao,
    PagamentoEntrada,
    PagamentoSaida,
)


router = APIRouter(prefix="/pagamentos", tags=["Pagamentos"])


def obter_sessao() -> Generator[Session, None, None]:
    sessao = SessionLocal()
    try:
        yield sessao
    finally:
        sessao.close()


@router.post("", response_model=PagamentoSaida, status_code=status.HTTP_201_CREATED)
def cadastrar_pagamento(
    dados: PagamentoEntrada, sessao: Session = Depends(obter_sessao)
):
    try:
        repositorio = PagamentoRepositorySQLAlchemy(sessao)
        caso_de_uso = CadastrarPagamento(repositorio)

        return caso_de_uso.cadastrar(
            reserva_id=dados.reserva_id,
            valor=dados.valor,
            metodo=dados.metodo,
            status=dados.status,
            data_pagamento=dados.data_pagamento,
        )
    except ValueError as erro:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(erro)
        ) from erro


@router.get("", response_model=list[PagamentoSaida])
def listar_pagamentos(sessao: Session = Depends(obter_sessao)):
    repositorio = PagamentoRepositorySQLAlchemy(sessao)
    caso_de_uso = ListarPagamentos(repositorio)
    return caso_de_uso.listar()


@router.get("/{id}", response_model=PagamentoSaida)
def buscar_pagamento(id: int, sessao: Session = Depends(obter_sessao)):
    try:
        repositorio = PagamentoRepositorySQLAlchemy(sessao)
        caso_de_uso = BuscarPagamento(repositorio)
        return caso_de_uso.buscar(id)
    except PagamentoNaoEncontradoError as erro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(erro)
        ) from erro


@router.put("/{id}", response_model=PagamentoSaida)
def atualizar_pagamento(
    id: int, dados: PagamentoAtualizacao, sessao: Session = Depends(obter_sessao)
):
    try:
        repositorio = PagamentoRepositorySQLAlchemy(sessao)
        caso_de_uso = AtualizarPagamento(repositorio)

        return caso_de_uso.atualizar(
            pagamento_id=id,
            reserva_id=dados.reserva_id,
            valor=dados.valor,
            metodo=dados.metodo,
            status=dados.status,
            data_pagamento=dados.data_pagamento,
        )
    except PagamentoNaoEncontradoError as erro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(erro)
        ) from erro
    except ValueError as erro:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(erro)
        ) from erro


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_pagamento(id: int, sessao: Session = Depends(obter_sessao)):
    try:
        repositorio = PagamentoRepositorySQLAlchemy(sessao)
        caso_de_uso = ExcluirPagamento(repositorio)
        caso_de_uso.excluir(id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except PagamentoNaoEncontradoError as erro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(erro)
        ) from erro
