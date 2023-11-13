from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Dependency, Singleton

from app.answers.repo import AnswersRepo
from app.errors import IncorrectDBConfigTypeProvided
from app.questions.repo import QuestionsRepo
from app.regular_users.controller import RegularUserController
from app.regular_users.infra.sa_queries import SARegularUsersQueriesFactory
from app.regular_users.infra.sa_repo import SARegularUsersRepo
from app.regular_users.queries import RegularUsersQueriesFactory
from app.regular_users.repo import RegularUsersRepo
from app.roles.repo import RolesRepo
from app.shared.db import DBConfig, SADBConfig
from app.statistics.service import StatisticsService


def get_regular_users_repo(
    db_config: DBConfig,
) -> RegularUsersRepo:
    if isinstance(db_config, SADBConfig):
        return SARegularUsersRepo(db_config)

    raise IncorrectDBConfigTypeProvided()


def get_regular_users_queries_factory(
    db_config: DBConfig,
) -> RegularUsersQueriesFactory:
    if isinstance(db_config, SADBConfig):
        return SARegularUsersQueriesFactory(db_config)

    raise IncorrectDBConfigTypeProvided()


class RegularUsersContainer(DeclarativeContainer):
    db_config = Dependency(DBConfig)  # type: ignore

    roles_repo = Dependency(RolesRepo)  # type: ignore

    questions_repo = Dependency(QuestionsRepo)  # type: ignore

    answers_repo = Dependency(AnswersRepo)  # type: ignore

    statistics_service = Dependency(StatisticsService)

    regular_users_repo = Singleton(get_regular_users_repo, db_config)

    regular_users_queries_factory = Singleton(
        get_regular_users_queries_factory, db_config=db_config
    )

    regular_user_controller = Singleton(
        RegularUserController,
        regular_users_repo=regular_users_repo,
        questions_repo=questions_repo,
        answers_repo=answers_repo,
        regular_users_queries_factory=regular_users_queries_factory,
        statistics_service=statistics_service,
    )
