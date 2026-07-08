from app.profissionais.application.buscar_profissional import (
    ProfissionalNaoEncontradoError,
)
from app.profissionais.domain.repositories.profissional_repository import (
    ProfissionalRepository,
)


class ExcluirProfissional:
    def __init__(self, repositorio: ProfissionalRepository):
        self.repositorio = repositorio

    def excluir(self, profissional_id: int) -> None:
        if not self.repositorio.excluir(profissional_id):
            raise ProfissionalNaoEncontradoError("Profissional não encontrado")
