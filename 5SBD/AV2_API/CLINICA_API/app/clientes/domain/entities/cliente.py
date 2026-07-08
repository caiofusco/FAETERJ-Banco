from dataclasses import dataclass


@dataclass
class Cliente:
    nome: str
    email: str
    telefone: str
    credito: float = 0
    id: int | None = None

    def __post_init__(self) -> None:
        self._validar(self.nome, self.email, self.telefone, self.credito)

    def atualizar(self, nome: str, email: str, telefone: str, credito: float) -> None:
        self._validar(nome, email, telefone, credito)
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self.credito = credito

    @staticmethod
    def _validar(nome: str, email: str, telefone: str, credito: float) -> None:
        if not nome.strip():
            raise ValueError("O nome é obrigatório")
        if "@" not in email or not email.strip():
            raise ValueError("O e-mail é inválido")
        if not telefone.strip():
            raise ValueError("O telefone é obrigatório")
        if credito < 0:
            raise ValueError("O crédito não pode ser negativo")
