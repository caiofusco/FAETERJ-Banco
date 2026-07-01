# Clínica de Estética API

API REST funcional para um sistema de reserva de serviços de salão de beleza e centro de estética.

O projeto foi criado para atender ao pedido da AV2: implementar a API do sistema, sem criar especificação de casos de uso e sem criar diagrama de classes.

## Tecnologias usadas

- Python 3.12+
- FastAPI
- DDD simplificado, com separação por camadas
- SQLAlchemy ORM
- JWT para autenticação
- SQLite por padrão, podendo trocar para PostgreSQL/MySQL/SQL Server pela variável `DATABASE_URL`
- Pydantic para validação dos dados
- Docker opcional

## Funcionalidades implementadas

- Autenticação com JWT
- Cadastro e login de cliente
- CRUD de clientes
- CRUD de usuários administrativos
- CRUD de serviços
- CRUD de pacotes pré-estabelecidos
- CRUD de profissionais
- CRUD de horários de trabalho
- Aprovação de horário informado por profissional terceirizado
- Consulta de horários disponíveis por serviço, especialidade, data e profissional
- Reserva de serviço com pagamento simulado por cartão de crédito
- Cancelamento e remarcação de reserva
- Regra de não comparecimento: cliente perde metade do valor e recebe crédito da outra metade
- Lista de espera para cliente sem reserva ou sem horário disponível
- Consulta e atualização de pagamentos pela gerência financeira

## Estrutura DDD simplificada

```txt
app/
  core/              Configurações e segurança
  domain/            Enums e exceções de domínio
  application/       Regras de negócio e serviços de aplicação
  infrastructure/    Banco de dados, ORM e repositórios
  interfaces/        Rotas FastAPI, schemas e dependências HTTP
```

## Como executar localmente

### 1. Criar ambiente virtual

```bash
python -m venv .venv
```

Windows PowerShell:

```bash
.venv\Scripts\Activate.ps1
```

Linux/macOS:

```bash
source .venv/bin/activate
```

### 2. Instalar dependências

```bash
pip install -r requirements.txt
```

### 3. Criar o arquivo `.env`

```bash
cp .env.example .env
```

No Windows, você pode simplesmente copiar o arquivo `.env.example` e renomear a cópia para `.env`.

### 4. Criar dados de exemplo

```bash
python -m app.seed
```

Usuários criados pelo seed:

| Perfil | E-mail | Senha |
|---|---|---|
| Administrador | admin@beleza.com | 123456 |
| Atendente | atendente@beleza.com | 123456 |
| Gerente Financeiro | financeiro@beleza.com | 123456 |
| Cliente | cliente@beleza.com | 123456 |

### 5. Subir a API

```bash
uvicorn app.main:app --reload
```

Acesse:

- API: `http://127.0.0.1:8000`
- Swagger: `http://127.0.0.1:8000/docs`
- Redoc: `http://127.0.0.1:8000/redoc`

## Como executar com Docker

```bash
cp .env.example .env
docker compose up --build
```

Depois acesse `http://127.0.0.1:8000/docs`.

## Fluxo de teste rápido

### Login

```bash
curl -X POST http://127.0.0.1:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"cliente@beleza.com","password":"123456"}'
```

Copie o `access_token` retornado.

### Consultar serviços

```bash
curl http://127.0.0.1:8000/api/v1/services
```

### Consultar horários disponíveis

Troque a data abaixo para a data do horário criado pelo seed, geralmente amanhã:

```bash
curl "http://127.0.0.1:8000/api/v1/availability?service_id=1&day=2026-07-02"
```

### Criar reserva com cartão de crédito simulado

```bash
curl -X POST http://127.0.0.1:8000/api/v1/reservations \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer SEU_TOKEN" \
  -d '{
    "service_id": 1,
    "starts_at": "2026-07-02T09:00:00",
    "card_last4": "1234"
  }'
```

## Observações importantes

1. O pagamento é simulado: a API grava a transação como aprovada e gera uma referência fictícia.
2. Por padrão, o banco é SQLite para facilitar a execução local.
3. Para produção, troque `SECRET_KEY`, use HTTPS, configure um banco externo e integre um gateway de pagamento real.
4. O projeto foi mantido simples para fins acadêmicos, mas com separação suficiente para demonstrar DDD, ORM e JWT.
