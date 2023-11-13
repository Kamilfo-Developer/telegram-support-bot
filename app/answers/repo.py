import abc

from app.answers.entities import Answer
from app.shared.db import DBConfig
from app.shared.value_objects import (
    AnswerIdType,
    QuestionIdType,
    SupportUserIdType,
    TgMessageIdType,
)


class AnswersRepo(abc.ABC):
    @abc.abstractmethod
    def __init__(self, db_config: DBConfig) -> None:
        ...

    @abc.abstractmethod
    async def add(
        self,
        answer: Answer,
    ) -> Answer:
        """Adds a new answer to the database.
        If entity with such id already exists, raises `EntityAlreadyExists`

        Args:
            answer (Answer): a new answer

        Returns:
            Answer: the same answer
        """

        ...

    @abc.abstractmethod
    async def update(self, answer: Answer) -> Answer:
        """Updates answer in the database.

        Args:
            answer (Answer): answer to update

        Returns:
            Answer: the same answer
        """
        ...

    @abc.abstractmethod
    async def get_all(self) -> list[Answer]:
        ...

    @abc.abstractmethod
    async def get_by_id(self, answer_id: AnswerIdType) -> Answer | None:
        ...

    @abc.abstractmethod
    async def get_question_last_answer(
        self, question_id: QuestionIdType
    ) -> Answer | None:
        ...

    @abc.abstractmethod
    async def get_by_question_id(
        self, question_id: QuestionIdType
    ) -> list[Answer]:
        ...

    @abc.abstractmethod
    async def delete(self, answer_id: AnswerIdType) -> None:
        ...

    @abc.abstractmethod
    async def delete_by_support_user_id(
        self, support_user_id: SupportUserIdType
    ) -> None:
        """Deletes all answers of Support User with `support_user_id`

        Args:
            support_user_id (SupportUserIdType): the id of support user
        """

        ...

    @abc.abstractmethod
    async def delete_all(self) -> None:
        ...

    @abc.abstractmethod
    async def get_by_support_user_id(
        self, support_user_id: SupportUserIdType
    ) -> list[Answer]:
        ...

    @abc.abstractmethod
    async def get_by_tg_message_id(
        self, tg_message_id: TgMessageIdType
    ) -> Answer | None:
        ...

    @abc.abstractmethod
    async def delete_by_question_id(self, question_id: QuestionIdType) -> None:
        ...

    # NOTE: The next code is supposed to count answers
    # but since the logic migrated to `app/service` module,
    # we don't really need to have thes methods.
    # But they are going to be here in case we need them
    # for some reasons.
    #
    #
    # @abc.abstractmethod
    # async def count_all(self) -> int:
    #     ...

    # @abc.abstractmethod
    # async def count_useful(self) -> int:
    #     ...

    # @abc.abstractmethod
    # async def count_unuseful_answers(self) -> int:
    #     ...

    # @abc.abstractmethod
    # async def count_by_question_id(self, question_id: QuestionIdType) -> int:
    #     ...
    # @abc.abstractmethod
    # async def count_by_support_user_id(
    #     self, support_user_id: SupportUserIdType
    # ) -> int:
    #     ...

    # @abc.abstractmethod
    # async def count_useful_by_support_user_id(
    #     self, support_user_id: SupportUserIdType
    # ) -> int:
    #     ...

    # @abc.abstractmethod
    # async def count_unuseful_by_support_user_id(
    #     self, support_user_id: SupportUserIdType
    # ) -> int:
    #     ...

    # @abc.abstractmethod
    # async def count_for_regular_user(
    #     self, regular_user_id: RegularUserIdType
    # ) -> int:
    #     ...

    # @abc.abstractmethod
    # async def count_useful_for_regular_user(
    #     self, regular_user_id: RegularUserIdType
    # ) -> int:
    #     ...

    # @abc.abstractmethod
    # async def count_unuseful_for_regular_user(
    #     self, regular_user_id: RegularUserIdType
    # ) -> int:
    #     ...

    # @abc.abstractmethod
    # async def count_usestimated_for_regular_user(
    #     self, regular_user_id: RegularUserIdType
    # ) -> int:
    #     ...
