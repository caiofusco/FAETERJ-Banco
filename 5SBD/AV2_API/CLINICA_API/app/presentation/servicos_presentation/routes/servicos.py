from collections.abc import Generator

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.infrastructure.database_infrastructure.database import SessionLocal
from app.application.servicos_application.atualizar_servico import AtualizarServico
from app.application.servicos_application.buscar_servico import (
    BuscarServico,
    ServicoNaoEncontradoError,
)
from app.application.servicos_application.cadastrar_servico import CadastrarServico
from app.application.servicos_application.excluir_servico import ExcluirServico
from app.application.servicos_application.listar_servicos import ListarServicos
from app.infrastructure.servicos_infrastructure.repositories.servico_repository_sqlalchemy import (
    ServicoRepositorySQLAlchemy,
)
from app.presentation.servicos_presentation.schemas.servico_schema import (
    ServicoAtualizacao,
    ServicoEntrada,
    ServicoSaida,
)


router = APIRouter(prefix="/servicos", tags=["Serviços"])


def obter_sessao() -> Generator[Session, None, None]:
    sessao = SessionLocal()
    try:
        yield sessao
    finally:
        sessao.close()


@router.post("", response_model=ServicoSaida, status_code=status.HTTP_201_CREATED)
def cadastrar_servico(dados: ServicoEntrada, sessao: Session = Depends(obter_sessao)):
    try:
        return CadastrarServico(ServicoRepositorySQLAlchemy(sessao)).cadastrar(
            nome=dados.nome,
            descricao=dados.descricao,
            especialidade=dados.especialidade,
            valor=dados.valor,
            duracao_minutos=dados.duracao_minutos,
        )
    except ValueError as erro:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(erro)
        ) from erro


@router.get("", response_model=list[ServicoSaida])
def listar_servicos(sessao: Session = Depends(obter_sessao)):
    return ListarServicos(ServicoRepositorySQLAlchemy(sessao)).listar()


@router.get("/{id}", response_model=ServicoSaida)
def buscar_servico(id: int, sessao: Session = Depends(obter_sessao)):
    try:
        return BuscarServico(ServicoRepositorySQLAlchemy(sessao)).buscar(id)
    except ServicoNaoEncontradoError as erro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(erro)
        ) from erro


@router.put("/{id}", response_model=ServicoSaida)
def atualizar_servico(
    id: int, dados: ServicoAtualizacao, sessao: Session = Depends(obter_sessao)
):
    try:
        return AtualizarServico(ServicoRepositorySQLAlchemy(sessao)).atualizar(
            servico_id=id,
            nome=dados.nome,
            descricao=dados.descricao,
            especialidade=dados.especialidade,
            valor=dados.valor,
            duracao_minutos=dados.duracao_minutos,
        )
    except ServicoNaoEncontradoError as erro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(erro)
        ) from erro
    except ValueError as erro:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(erro)
        ) from erro


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_servico(id: int, sessao: Session = Depends(obter_sessao)):
    try:
        ExcluirServico(ServicoRepositorySQLAlchemy(sessao)).excluir(id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except ServicoNaoEncontradoError as erro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(erro)
        ) from erro
