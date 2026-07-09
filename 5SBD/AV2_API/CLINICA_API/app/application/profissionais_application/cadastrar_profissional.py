from app.domain.profissionais_domain.entities.profissional import Profissional
from app.domain.profissionais_domain.repositories.profissional_repository import (
    ProfissionalRepository,
)


class CadastrarProfissional:
    def __init__(self, repositorio: ProfissionalRepository):
        self.repositorio = repositorio

    def cadastrar(
        self, nome: str, especialidade: str, ativo: bool = True
    ) -> Profissional:
        profissional = Profissional(nome=nome, especialidade=especialidade, ativo=ativo)
        return self.repositorio.salvar(profissional)
