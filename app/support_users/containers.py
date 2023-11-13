from dependency_injector.providers import Dependency, Singleton
from dependency_injector.containers import DeclarativeContainer
from app.answers.repo import AnswersRepo
from app.errors import IncorrectDBConfigTypeProvided
from app.questions.repo import QuestionsRepo
from app.regular_users.repo import RegularUsersRepo
from app.roles.repo import RolesRepo
from app.shared.db import DBConfig, SADBConfig
from app.statistics.service import StatisticsService
from app.support_users.controller import SupportUserController
from app.support_users.infra.sa_queries import SASupportUsersQueriesFactory
from app.support_users.infra.sa_repo import SASupportUsersRepo
from app.support_users.queries import SupportUsersQueriesFactory
from app.support_users.repo import SupportUsersRepo


def get_support_users_repo(
    db_config: DBConfig,
) -> SupportUsersRepo:
    if isinstance(db_config, SADBConfig):
        return SASupportUsersRepo(db_config)

    raise IncorrectDBConfigTypeProvided()


def get_suuport_users_queries_factory(
    db_config,
) -> SupportUsersQueriesFactory:
    if isinstance(db_config, SADBConfig):
        return SASupportUsersQueriesFactory(db_config)

    raise IncorrectDBConfigTypeProvided()


class SupportUsersContainer(DeclarativeContainer):
    db_config = Dependency(DBConfig)  # type: ignore

    roles_repo = Dependency(RolesRepo)  # type: ignore

    regular_users_repo = Dependency(RegularUsersRepo)  # type: ignore

    questions_repo = Dependency(QuestionsRepo)  # type: ignore

    answers_repo = Dependency(AnswersRepo)  # type: ignore

    statistics_service = Dependency(StatisticsService)

    support_users_repo = Singleton(get_support_users_repo, db_config)

    support_users_queries_factory = Singleton(
        get_suuport_users_queries_factory, db_config
    )

    support_user_controller = Singleton(
        SupportUserController,
        support_users_repo=support_users_repo,
        regular_users_repo=regular_users_repo,
        questions_repo=questions_repo,
        answers_repo=answers_repo,
        roles_repo=roles_repo,
        statistics_service=statistics_service,
        support_users_queries_factory=support_users_queries_factory,
    )
