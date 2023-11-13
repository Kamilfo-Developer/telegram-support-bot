from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import (
    Singleton,
    Container,
)
from app.answers.containers import AnswersContainer

from app.bot.containers import BotContainer
from app.config.app_config import AppSettings
from app.loggers.containers import LoggersContainer
from app.questions.containers import QuestionsContainer
from app.regular_users.containers import RegularUsersContainer
from app.roles.containers import RolesContainer
from app.shared.db import get_db_config
from app.statistics.containers import StatisticsContainer
from app.support_users.containers import SupportUsersContainer


class AppContainer(DeclarativeContainer):
    app_settings = Singleton(AppSettings)

    db_config = Singleton(get_db_config, app_settings)

    loggers_container = Container(LoggersContainer, app_settings=app_settings)

    roles_container: Container[RolesContainer] = Container(
        RolesContainer, db_config=db_config
    )

    answers_container = Container(AnswersContainer, db_config=db_config)

    quesions_container = Container(QuestionsContainer, db_config=db_config)

    statistics_container = Container(StatisticsContainer, db_config=db_config)

    regular_users_container = Container(
        RegularUsersContainer,
        db_config=db_config,
        roles_repo=roles_container.roles_repo,
        questions_repo=quesions_container.questions_repo,
        answers_repo=answers_container.answers_repo,
        statistics_service=statistics_container.statistics_service,
    )

    support_users_container = Container(
        SupportUsersContainer,
        db_config=db_config,
        roles_repo=roles_container.roles_repo,
        regular_users_repo=regular_users_container.regular_users_repo,
        questions_repo=quesions_container.questions_repo,
        answers_repo=answers_container.answers_repo,
        statistics_service=statistics_container.statistics_service,
    )

    bot_container = Container(
        BotContainer,
        app_settings=app_settings,
        app_logger=loggers_container.app_logger,
        support_user_controller=support_users_container.support_user_controller,  # noqa: E501
        regular_user_controller=regular_users_container.regular_user_controller,  # noqa: E501
    )
