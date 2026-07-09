from dataclasses import dataclass, field


@dataclass
class Pacote:
    nome: str
    descricao: str
    valor: float
    servicos: list[int] = field(default_factory=list)
    id: int | None = None

    def __post_init__(self) -> None:
        self._validar(self.nome, self.descricao, self.valor, self.servicos)

    def atualizar(
        self, nome: str, descricao: str, valor: float, servicos: list[int]
    ) -> None:
        self._validar(nome, descricao, valor, servicos)
        self.nome = nome
        self.descricao = descricao
        self.valor = valor
        self.servicos = servicos

    @staticmethod
    def _validar(nome: str, descricao: str, valor: float, servicos: list[int]) -> None:
        if not nome.strip():
            raise ValueError("O nome é obrigatório")
        if not descricao.strip():
            raise ValueError("A descrição é obrigatória")
        if valor <= 0:
            raise ValueError("O valor deve ser maior que zero")
        if any(servico_id <= 0 for servico_id in servicos):
            raise ValueError("Os IDs dos serviços devem ser maiores que zero")
