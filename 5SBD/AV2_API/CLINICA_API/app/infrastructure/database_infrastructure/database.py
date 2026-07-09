import os

from sqlalchemy import URL, create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


def criar_url_banco():
    url_completa = os.getenv("DATABASE_URL")
    if url_completa:
        return url_completa

    servidor = os.getenv("DB_SERVER", ".")
    banco = os.getenv("DB_NAME", "AV2_SBD")
    usuario = os.getenv("DB_USER")
    senha = os.getenv("DB_PASSWORD")
    driver = os.getenv("DB_DRIVER", "ODBC Driver 18 for SQL Server")

    parametros = {
        "driver": driver,
        "TrustServerCertificate": "yes",
    }

    if not usuario:
        parametros["Trusted_Connection"] = "yes"

    return URL.create(
        "mssql+pyodbc",
        username=usuario,
        password=senha,
        host=servidor,
        database=banco,
        query=parametros,
    )


URL_BANCO = criar_url_banco()

engine = create_engine(
    URL_BANCO,
    pool_pre_ping=True,
    connect_args={"timeout": int(os.getenv("DB_TIMEOUT", "5"))},
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    pass
