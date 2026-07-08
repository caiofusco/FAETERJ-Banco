from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.core.config import get_settings
from app.domain.exceptions import BusinessRuleError, DomainError, NotFoundError
from app.infrastructure.database import Base, engine
from app.interfaces.routes import router

settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="API de reservas para salão de beleza e centro de estética, com DDD, ORM, JWT e SQLAlchemy.",
)


@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)


@app.exception_handler(DomainError)
async def domain_error_handler(_: Request, exc: DomainError):
    code = status.HTTP_400_BAD_REQUEST
    if isinstance(exc, NotFoundError):
        code = status.HTTP_404_NOT_FOUND
    elif isinstance(exc, BusinessRuleError):
        code = status.HTTP_400_BAD_REQUEST
    return JSONResponse(status_code=code, content={"detail": str(exc)})


@app.get("/", tags=["Healthcheck"])
def healthcheck():
    return {"status": "ok", "app": settings.APP_NAME}


app.include_router(router, prefix="/api/v1")
