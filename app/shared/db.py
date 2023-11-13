from __future__ import annotations

import abc
from typing import Any, AsyncContextManager, Callable, TypeVar

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.orm import Session, sessionmaker

from app.config.app_config import AppSettings, RepoType
from app.config.db_sa_config import get_sa_engine, get_session_maker
from app.errors import IncorrectRepoTypeProvided


class DBConfig(abc.ABC):
    connection_provider: Callable[..., AsyncContextManager[Any]]

    @abc.abstractmethod
    def __init__(
        self,
        connection_provider: Callable[..., AsyncContextManager[Any]],
        *args,
        **kwargs,
    ) -> None:
        ...


class SADBConfig(DBConfig):
    engine: AsyncEngine
    connection_provider: Callable[..., AsyncSession]

    def __init__(
        self,
        connection_povider: Callable[..., AsyncSession],
        engine: AsyncEngine,
    ) -> None:
        self.connection_provider = connection_povider
        self.engine = engine


T = TypeVar("T")


def get_db_config(app_settings: AppSettings) -> DBConfig:
    if app_settings.REPO_TYPE == RepoType.SA:
        engine: AsyncEngine = get_sa_engine(app_settings.SA_DB_PROVIDER)

        async_session_maker: sessionmaker[Session] = get_session_maker(engine)

        return SADBConfig(async_session_maker, engine)  # type: ignore

    raise IncorrectRepoTypeProvided(
        "REPO_TYPE has to have one of next values: SA"
    )
