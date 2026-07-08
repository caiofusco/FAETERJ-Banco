from app.profissionais.application.buscar_profissional import (
    ProfissionalNaoEncontradoError,
)
from app.profissionais.domain.entities.profissional import Profissional
from app.profissionais.domain.repositories.profissional_repository import (
    ProfissionalRepository,
)


class AtualizarProfissional:
    def __init__(self, repositorio: ProfissionalRepository):
        self.repositorio = repositorio

    def atualizar(
        self, profissional_id: int, nome: str, especialidade: str, ativo: bool
    ) -> Profissional:
        profissional = self.repositorio.buscar_por_id(profissional_id)
        if profissional is None:
            raise ProfissionalNaoEncontradoError("Profissional não encontrado")
        profissional.atualizar(nome=nome, especialidade=especialidade, ativo=ativo)
        return self.repositorio.atualizar(profissional)
