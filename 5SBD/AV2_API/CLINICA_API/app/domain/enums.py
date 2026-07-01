from enum import Enum


class RoleEnum(str, Enum):
    ADMINISTRADOR = "administrador"
    GERENTE_FINANCEIRO = "gerente_financeiro"
    ATENDENTE = "atendente"
    PROFISSIONAL_CONTRATADO = "profissional_contratado"
    PROFISSIONAL_TERCEIRIZADO = "profissional_terceirizado"
    CLIENTE = "cliente"


class ProfessionalTypeEnum(str, Enum):
    CONTRATADO = "contratado"
    TERCEIRIZADO = "terceirizado"


class ReservationStatusEnum(str, Enum):
    AGENDADO = "agendado"
    CANCELADO = "cancelado"
    CONCLUIDO = "concluido"
    NAO_COMPARECEU = "nao_compareceu"


class PaymentMethodEnum(str, Enum):
    CARTAO_CREDITO = "cartao_credito"


class PaymentStatusEnum(str, Enum):
    APROVADO = "aprovado"
    CANCELADO = "cancelado"
    ESTORNADO = "estornado"


class WaitlistStatusEnum(str, Enum):
    AGUARDANDO = "aguardando"
    CHAMADO = "chamado"
    ATENDIDO = "atendido"
    CANCELADO = "cancelado"
