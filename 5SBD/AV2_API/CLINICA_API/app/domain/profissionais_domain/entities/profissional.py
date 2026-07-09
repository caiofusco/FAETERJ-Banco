from dataclasses import dataclass


@dataclass
class Profissional:
    nome: str
    especialidade: str
    ativo: bool = True
    id: int | None = None

    def __post_init__(self) -> None:
        self._validar(self.nome, self.especialidade)

    def atualizar(self, nome: str, especialidade: str, ativo: bool) -> None:
        self._validar(nome, especialidade)
        self.nome = nome
        self.especialidade = especialidade
        self.ativo = ativo

    @staticmethod
    def _validar(nome: str, especialidade: str) -> None:
        if not nome.strip():
            raise ValueError("O nome é obrigatório")
        if not especialidade.strip():
            raise ValueError("A especialidade é obrigatória")
