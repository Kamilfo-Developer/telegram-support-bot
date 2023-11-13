from dependency_injector.providers import Dependency, Singleton
from dependency_injector.containers import DeclarativeContainer
from app.errors import IncorrectDBConfigTypeProvided
from app.questions.controller import QuestionsController
from app.questions.infra.sa_repo import SAQuestionsRepo
from app.questions.repo import QuestionsRepo
from app.shared.db import DBConfig, SADBConfig


def get_questions_repo(
    db_config: DBConfig,
) -> QuestionsRepo:
    if isinstance(db_config, SADBConfig):
        return SAQuestionsRepo(db_config)

    raise IncorrectDBConfigTypeProvided()


class QuestionsContainer(DeclarativeContainer):
    db_config = Dependency(DBConfig)  # type: ignore

    questions_repo = Singleton(get_questions_repo, db_config)

    questions_controller = Singleton(
        QuestionsController,
        questions_repo=questions_repo,
    )
