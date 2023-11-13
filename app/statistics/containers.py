from dependency_injector.providers import Dependency, Singleton
from dependency_injector.containers import DeclarativeContainer
from app.errors import IncorrectDBConfigTypeProvided
from app.shared.db import DBConfig, SADBConfig
from app.statistics.service import StatisticsService

from app.statistics.infra.sa_queries import (
    SAStatisticsQueriesFactory,
)
from app.statistics.queries import StatisticsQueriesFactory


def get_statistics_queries_factory(
    db_config: DBConfig,
) -> StatisticsQueriesFactory:
    if isinstance(db_config, SADBConfig):
        return SAStatisticsQueriesFactory(db_config)

    raise IncorrectDBConfigTypeProvided()


class StatisticsContainer(DeclarativeContainer):
    db_config: Dependency[DBConfig] = Dependency(SADBConfig)

    statistics_queries_factory: Singleton[
        StatisticsQueriesFactory
    ] = Singleton(get_statistics_queries_factory, db_config)

    statistics_service: Singleton[StatisticsService] = Singleton(
        StatisticsService, statistics_queries_factory
    )
