import os
from pathlib import Path

from pydantic import BaseSettings, FilePath
from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config.app_config import SADBProviderType


class SAPostgresSettings(BaseSettings):
    POSTGRES_DRIVER_NAME: str = "asyncpg"

    POSTGRES_DB_NAME: str = "postgres"

    POSTGRES_USERNAME: str = "postgres"

    POSTGRES_HOST: str = "localhost"

    POSTGRES_DB_PORT: int = 5432

    POSTGRES_PASSWORD: str = "postgres"

    class Config:
        env_file = ".env"


class SAMySQLSettings(BaseSettings):
    MYSQL_DRIVER_NAME: str = "asyncmy"

    MYSQL_USERNAME: str = "root"

    MYSQL_HOST: str = "localhost"

    MYSQL_DB_PORT: int = 3306

    MYSQL_DB_NAME: str

    MYSQL_PASSWORD: str

    class Config:
        env_file = ".env"


class SASQLiteSettings(BaseSettings):
    SQLITE_DRIVER_NAME: str = "aiosqlite"

    SQLITE_DB_NAME: str = "data.db"

    # In case you want to change path to SQLite DB file,
    # just change this variable

    SQLITE_DB_FILE_PATH: FilePath = Path(
        os.path.join(
            Path(__file__).parent.parent.parent.resolve(),  # Root path
            f"data/{SQLITE_DB_NAME}",
        )
    )

    class Config:
        env_file = ".env"


def get_sa_db_url(sa_db_provider_type: SADBProviderType) -> str:
    match sa_db_provider_type:
        case SADBProviderType.POSTGRES:
            pgs_conf = SAPostgresSettings()

            DB_URL = (
                f"postgresql+{pgs_conf.POSTGRES_DRIVER_NAME}://"
                + f"{pgs_conf.POSTGRES_USERNAME}:{pgs_conf.POSTGRES_PASSWORD}"
                + f"@{pgs_conf.POSTGRES_HOST}:{pgs_conf.POSTGRES_DB_PORT}"
                + f"/{pgs_conf.POSTGRES_DB_NAME}"
            )

        case SADBProviderType.MYSQL:
            mysql_conf = SAMySQLSettings()  # type: ignore

            DB_URL = (
                f"mysql+{mysql_conf.MYSQL_DRIVER_NAME}://"
                + f"{mysql_conf.MYSQL_USERNAME}:{mysql_conf.MYSQL_PASSWORD}"
                + f"@{mysql_conf.MYSQL_HOST}:{mysql_conf.MYSQL_DB_PORT}"
                + f"/{mysql_conf.MYSQL_DB_NAME}"
            )

        case _:
            sqlite_conf = SASQLiteSettings()

            # URL for your database
            DB_URL = f"sqlite+{sqlite_conf.SQLITE_DRIVER_NAME}:///" + str(
                sqlite_conf.SQLITE_DB_FILE_PATH
            )

    return DB_URL


def get_sa_engine(sa_db_provider_type: SADBProviderType) -> AsyncEngine:
    if sa_db_provider_type == SADBProviderType.SQLITE:

        @event.listens_for(Engine, "connect")
        def set_sqlite_pragma(dbapi_connection, connection_record):
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()

    return create_async_engine(get_sa_db_url(sa_db_provider_type), echo=False)


def get_session_maker(engine: AsyncEngine) -> sessionmaker:
    return sessionmaker(
        engine,  # type: ignore
        expire_on_commit=False,
        class_=AsyncSession,
    )


class ModelBase(DeclarativeBase):
    pass
