from fastapi import FastAPI
from fastapi import Depends
from app.presentation.autenticacao_presentation.routes.login import (
    router as login_router,
)
from app.infrastructure.autenticacao_infrastructure.seguranca import verificar_token
from app.presentation.clientes_presentation.routes.clientes import (
    router as clientes_router,
)
from app.presentation.fila_espera_presentation.routes.fila_espera import (
    router as fila_espera_router,
)
from app.presentation.pacotes_presentation.routes.pacotes import (
    router as pacotes_router,
)
from app.presentation.pagamentos_presentation.routes.pagamentos import (
    router as pagamentos_router,
)
from app.presentation.profissionais_presentation.routes.profissionais import (
    router as profissionais_router,
)
from app.presentation.reservas_presentation.routes.reservas import (
    router as reservas_router,
)
from app.presentation.servicos_presentation.routes.servicos import (
    router as servicos_router,
)

app = FastAPI(
    title="AV2 SBD",
    version="1.0.0",
)

app.include_router(login_router)
app.include_router(clientes_router, dependencies=[Depends(verificar_token)])
app.include_router(profissionais_router, dependencies=[Depends(verificar_token)])
app.include_router(servicos_router, dependencies=[Depends(verificar_token)])
app.include_router(pacotes_router, dependencies=[Depends(verificar_token)])
app.include_router(reservas_router, dependencies=[Depends(verificar_token)])
app.include_router(pagamentos_router, dependencies=[Depends(verificar_token)])
app.include_router(fila_espera_router, dependencies=[Depends(verificar_token)])
