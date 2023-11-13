from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Dependency, Singleton

from app.answers.controller import AnswersController
from app.answers.infra.sa_repo import SAAnswersRepo
from app.answers.repo import AnswersRepo
from app.errors import IncorrectDBConfigTypeProvided
from app.shared.db import DBConfig, SADBConfig


def get_answers_repo(
    db_config: DBConfig,
) -> AnswersRepo:
    if isinstance(db_config, SADBConfig):
        return SAAnswersRepo(db_config)

    raise IncorrectDBConfigTypeProvided()


class AnswersContainer(DeclarativeContainer):
    db_config = Dependency(DBConfig)  # type: ignore

    answers_repo = Singleton(get_answers_repo, db_config)

    answers_controller = Singleton(
        AnswersController,
        answers_repo=answers_repo,
    )
