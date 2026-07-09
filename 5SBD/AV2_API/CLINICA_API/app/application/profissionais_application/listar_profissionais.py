from app.domain.profissionais_domain.entities.profissional import Profissional
from app.domain.profissionais_domain.repositories.profissional_repository import (
    ProfissionalRepository,
)


class ListarProfissionais:
    def __init__(self, repositorio: ProfissionalRepository):
        self.repositorio = repositorio

    def listar(self) -> list[Profissional]:
        return self.repositorio.listar()
