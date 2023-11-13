import abc

from app.questions.entities import Question
from app.shared.db import DBConfig
from app.shared.value_objects import (
    QuestionIdType,
    RegularUserIdType,
    TgMessageIdType,
)


class QuestionsRepo(abc.ABC):
    @abc.abstractmethod
    def __init__(self, db_config: DBConfig) -> None:
        ...

    @abc.abstractmethod
    async def add(self, question: Question) -> Question:
        """Adds a new question to the database.
        If question with this id already exsists, raises `EntityAlreadyExists`


        Args:
            question (Question): qustion to add

        Returns:
            Question: the same question
        """
        ...

    @abc.abstractmethod
    async def update(self, question: Question) -> Question:
        """Updates entity in the database.

        Args:
            question (Question): question to update

        Returns:
            Question: the same question
        """
        ...

    @abc.abstractmethod
    async def get_random_unbound(self) -> Question | None:
        ...

    @abc.abstractmethod
    async def get_random_unanswered_unbound(self) -> Question | None:
        ...

    @abc.abstractmethod
    async def get_random_answered(self) -> Question | None:
        ...

    @abc.abstractmethod
    async def get_all(self) -> list[Question]:
        ...

    @abc.abstractmethod
    async def get_by_id(self, question_id: QuestionIdType) -> Question | None:
        ...

    @abc.abstractmethod
    async def get_last_asked(
        self, regular_user_id: RegularUserIdType
    ) -> Question | None:
        ...

    @abc.abstractmethod
    async def get_by_tg_message_id(
        self, tg_message_id: TgMessageIdType
    ) -> Question | None:
        ...

    @abc.abstractmethod
    async def get_by_regular_user_id(
        self, regular_user_id: RegularUserIdType
    ) -> list[Question]:
        ...

    @abc.abstractmethod
    async def get_unbound(self) -> list[Question]:
        ...

    @abc.abstractmethod
    async def get_unanswered(self) -> list[Question]:
        ...

    @abc.abstractmethod
    async def delete(self, question_id: QuestionIdType) -> None:
        ...

    @abc.abstractmethod
    async def delete_by_regular_user_id(
        self, regular_user_id: RegularUserIdType
    ) -> None:
        """Deletes the questions of Regular User with `regular_user_id`

        Args:
            regular_user_id (RegularUserIdType): id of the Regular User
        """
        ...

    @abc.abstractmethod
    async def delete_all(self) -> None:
        ...

    # Legacy code. Explanation can be found in app/answers/repo.py

    # @abc.abstractmethod
    # async def count_all(self) -> int:
    #     ...

    # @abc.abstractmethod
    # async def count_by_regular_user_id(
    #     self, regular_user_id: RegularUserIdType
    # ) -> int:
    #     ...

    # @abc.abstractmethod
    # async def count_unanswered(self) -> int:
    #     ...

    # @abc.abstractmethod
    # async def count_answered(self) -> int:
    #     ...

    # @abc.abstractmethod
    # async def count_answerd_by_regular_user_id(
    #     self, regular_user_id: RegularUserIdType
    # ) -> int:
    #     ...
