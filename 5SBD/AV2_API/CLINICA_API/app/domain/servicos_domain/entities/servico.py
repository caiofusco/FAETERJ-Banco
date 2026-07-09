from dataclasses import dataclass


@dataclass
class Servico:
    nome: str
    descricao: str
    especialidade: str
    valor: float
    duracao_minutos: int
    id: int | None = None

    def __post_init__(self) -> None:
        self._validar(
            self.nome,
            self.descricao,
            self.especialidade,
            self.valor,
            self.duracao_minutos,
        )

    def atualizar(
        self,
        nome: str,
        descricao: str,
        especialidade: str,
        valor: float,
        duracao_minutos: int,
    ) -> None:
        self._validar(nome, descricao, especialidade, valor, duracao_minutos)
        self.nome = nome
        self.descricao = descricao
        self.especialidade = especialidade
        self.valor = valor
        self.duracao_minutos = duracao_minutos

    @staticmethod
    def _validar(
        nome: str,
        descricao: str,
        especialidade: str,
        valor: float,
        duracao_minutos: int,
    ) -> None:
        if not nome.strip():
            raise ValueError("O nome é obrigatório")
        if not descricao.strip():
            raise ValueError("A descrição é obrigatória")
        if not especialidade.strip():
            raise ValueError("A especialidade é obrigatória")
        if valor <= 0:
            raise ValueError("O valor deve ser maior que zero")
        if duracao_minutos <= 0:
            raise ValueError("A duração deve ser maior que zero")
