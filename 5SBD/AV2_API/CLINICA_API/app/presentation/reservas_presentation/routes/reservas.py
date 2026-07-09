from collections.abc import Generator

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.infrastructure.database_infrastructure.database import SessionLocal
from app.application.reservas_application.atualizar_reserva import AtualizarReserva
from app.application.reservas_application.buscar_reserva import (
    BuscarReserva,
    ReservaNaoEncontradaError,
)
from app.application.reservas_application.cadastrar_reserva import CadastrarReserva
from app.application.reservas_application.excluir_reserva import ExcluirReserva
from app.application.reservas_application.listar_reservas import ListarReservas
from app.infrastructure.reservas_infrastructure.repositories.reserva_repository_sqlalchemy import (
    ReservaRepositorySQLAlchemy,
)
from app.presentation.reservas_presentation.schemas.reserva_schema import (
    ReservaAtualizacao,
    ReservaEntrada,
    ReservaSaida,
)


router = APIRouter(prefix="/reservas", tags=["Reservas"])


def obter_sessao() -> Generator[Session, None, None]:
    sessao = SessionLocal()
    try:
        yield sessao
    finally:
        sessao.close()


@router.post("", response_model=ReservaSaida, status_code=status.HTTP_201_CREATED)
def cadastrar_reserva(dados: ReservaEntrada, sessao: Session = Depends(obter_sessao)):
    try:
        repositorio = ReservaRepositorySQLAlchemy(sessao)
        caso_de_uso = CadastrarReserva(repositorio)

        return caso_de_uso.cadastrar(
            cliente_id=dados.cliente_id,
            profissional_id=dados.profissional_id,
            servico_id=dados.servico_id,
            pacote_id=dados.pacote_id,
            data_hora=dados.data_hora,
            status=dados.status,
            valor_total=dados.valor_total,
        )
    except ValueError as erro:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(erro)
        ) from erro


@router.get("", response_model=list[ReservaSaida])
def listar_reservas(sessao: Session = Depends(obter_sessao)):
    repositorio = ReservaRepositorySQLAlchemy(sessao)
    caso_de_uso = ListarReservas(repositorio)
    return caso_de_uso.listar()


@router.get("/{id}", response_model=ReservaSaida)
def buscar_reserva(id: int, sessao: Session = Depends(obter_sessao)):
    try:
        repositorio = ReservaRepositorySQLAlchemy(sessao)
        caso_de_uso = BuscarReserva(repositorio)
        return caso_de_uso.buscar(id)
    except ReservaNaoEncontradaError as erro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(erro)
        ) from erro


@router.put("/{id}", response_model=ReservaSaida)
def atualizar_reserva(
    id: int, dados: ReservaAtualizacao, sessao: Session = Depends(obter_sessao)
):
    try:
        repositorio = ReservaRepositorySQLAlchemy(sessao)
        caso_de_uso = AtualizarReserva(repositorio)

        return caso_de_uso.atualizar(
            reserva_id=id,
            cliente_id=dados.cliente_id,
            profissional_id=dados.profissional_id,
            servico_id=dados.servico_id,
            pacote_id=dados.pacote_id,
            data_hora=dados.data_hora,
            status=dados.status,
            valor_total=dados.valor_total,
        )
    except ReservaNaoEncontradaError as erro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(erro)
        ) from erro
    except ValueError as erro:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(erro)
        ) from erro


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_reserva(id: int, sessao: Session = Depends(obter_sessao)):
    try:
        repositorio = ReservaRepositorySQLAlchemy(sessao)
        caso_de_uso = ExcluirReserva(repositorio)
        caso_de_uso.excluir(id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except ReservaNaoEncontradaError as erro:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(erro)
        ) from erro
