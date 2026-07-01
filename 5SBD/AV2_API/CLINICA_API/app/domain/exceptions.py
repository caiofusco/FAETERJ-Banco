class DomainError(Exception):
    """Erro de regra de negócio da aplicação."""


class NotFoundError(DomainError):
    """Recurso não encontrado."""


class BusinessRuleError(DomainError):
    """Regra de negócio violada."""
