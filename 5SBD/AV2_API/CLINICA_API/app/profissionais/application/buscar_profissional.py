from app.profissionais.domain.entities.profissional import Profissional
from app.profissionais.domain.repositories.profissional_repository import (
    ProfissionalRepository,
)


class ProfissionalNaoEncontradoError(Exception):
    pass


class BuscarProfissional:
    def __init__(self, repositorio: ProfissionalRepository):
        self.repositorio = repositorio

    def buscar(self, profissional_id: int) -> Profissional:
        profissional = self.repositorio.buscar_por_id(profissional_id)
        if profissional is None:
            raise ProfissionalNaoEncontradoError("Profissional não encontrado")
        return profissional
