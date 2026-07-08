from fastapi import FastAPI
from app.clientes.presentation.routes.clientes import router as clientes_router
from app.fila_espera.presentation.routes.fila_espera import router as fila_espera_router
from app.pacotes.presentation.routes.pacotes import router as pacotes_router
from app.pagamentos.presentation.routes.pagamentos import router as pagamentos_router
from app.profissionais.presentation.routes.profissionais import (
    router as profissionais_router,
)
from app.reservas.presentation.routes.reservas import router as reservas_router
from app.servicos.presentation.routes.servicos import router as servicos_router

app = FastAPI(
    title="AV2 SBD",
    version="1.0.0",
)

app.include_router(clientes_router)
app.include_router(profissionais_router)
app.include_router(servicos_router)
app.include_router(pacotes_router)
app.include_router(reservas_router)
app.include_router(pagamentos_router)
app.include_router(fila_espera_router)
