from __future__ import annotations
from uuid import UUID
from typing import TYPE_CHECKING, Any, AsyncContextManager, Callable
import abc

if TYPE_CHECKING:
    from app.entities.support_user import SupportUser
    from app.entities.answer import Answer
    from app.entities.answer_attachment import AnswerAttachment
    from app.entities.question import Question
    from app.entities.question_attachment import QuestionAttachment
    from app.entities.regular_user import RegularUser
    from app.entities.role import Role


class RepoConfig(abc.ABC):
    connection_provider: Callable[..., AsyncContextManager[Any]]

    @abc.abstractmethod
    def __init__(
        self, connection_provider: Callable[..., AsyncContextManager[Any]]
    ):
        raise NotImplementedError()


class RolesRepo(abc.ABC):
    @abc.abstractmethod
    def __init__(self, repo_config: RepoConfig):
        raise NotImplementedError()

    @abc.abstractmethod
    async def add(self, role: Role) -> Role:
        raise NotImplementedError()

    @abc.abstractmethod
    async def update(self, role: Role) -> Role:
        raise NotImplementedError()

    @abc.abstractmethod
    async def get_by_id(self, id: int) -> Role | None:
        raise NotImplementedError()

    @abc.abstractmethod
    async def get_by_name(self, name: str) -> Role | None:
        raise NotImplementedError()

    @abc.abstractmethod
    async def get_all(self) -> list[Role]:
        raise NotImplementedError()

    @abc.abstractmethod
    async def delete(self, role_id: int) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    async def delete_all(self) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    async def count_all(self) -> int:
        raise NotImplementedError()


class SupportUsersRepo(abc.ABC):
    @abc.abstractmethod
    def __init__(self, repo_config: RepoConfig) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    async def add(self, support_user: SupportUser) -> SupportUser:
        raise NotImplementedError()

    @abc.abstractmethod
    async def update(self, support_user: SupportUser) -> SupportUser:
        raise NotImplementedError()

    @abc.abstractmethod
    async def get_by_id(self, id: UUID) -> SupportUser | None:
        raise NotImplementedError()

    @abc.abstractmethod
    async def get_by_tg_bot_user_id(
        self, tg_bot_user_id: int
    ) -> SupportUser | None:
        raise NotImplementedError()

    @abc.abstractmethod
    async def get_owner(self) -> SupportUser | None:
        raise NotImplementedError()

    @abc.abstractmethod
    async def get_by_role_id(self, role_id: int) -> list[SupportUser]:
        raise NotImplementedError()

    @abc.abstractmethod
    async def get_all(self) -> list[SupportUser]:
        raise NotImplementedError()

    @abc.abstractmethod
    async def delete(self, id: UUID) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    async def delete_all(self) -> None:
        raise NotImplementedError()

    # Count methods

    @abc.abstractmethod
    async def count_all(self) -> int:
        raise NotImplementedError()

    @abc.abstractmethod
    async def count_by_role_id(self, role_id: int) -> int:
        raise NotImplementedError()

    @abc.abstractmethod
    async def count_activated(self) -> int:
        raise NotImplementedError()

    @abc.abstractmethod
    async def count_deactivated(self) -> int:
        raise NotImplementedError()


class RegularUsersRepo(abc.ABC):
    @abc.abstractmethod
    def __init__(self, repo_config: RepoConfig) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    async def add(self, regular_user: RegularUser) -> RegularUser:
        raise NotImplementedError()

    @abc.abstractmethod
    async def update(self, regular_user: RegularUser) -> RegularUser:
        raise NotImplementedError()

    @abc.abstractmethod
    async def get_by_id(self, id: UUID) -> RegularUser | None:
        raise NotImplementedError()

    @abc.abstractmethod
    async def get_by_tg_bot_user_id(
        self, tg_bot_user_id: int
    ) -> RegularUser | None:
        raise NotImplementedError()

    @abc.abstractmethod
    async def get_all(self) -> list[RegularUser]:
        raise NotImplementedError()

    @abc.abstractmethod
    async def delete(self, id: UUID) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    async def delete_all(self) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    async def count_all(self) -> int:
        raise NotImplementedError()


class QuestionsRepo(abc.ABC):
    @abc.abstractmethod
    def __init__(self, repo_config: RepoConfig) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    async def add(self, question: Question) -> Question:
        raise NotImplementedError()

    @abc.abstractmethod
    async def update(self, question: Question) -> Question:
        raise NotImplementedError()

    @abc.abstractmethod
    async def get_random_unbinded(self) -> Question | None:
        raise NotImplementedError()

    async def get_random_unanswered_unbinded(self) -> Question | None:
        raise NotImplementedError()

    @abc.abstractmethod
    async def get_all(self) -> list[Question]:
        raise NotImplementedError()

    @abc.abstractmethod
    async def get_by_id(self, question_id: UUID) -> Question | None:
        raise NotImplementedError()

    @abc.abstractmethod
    async def get_last_asked(self, regular_user_id: UUID) -> Question | None:
        raise NotImplementedError()

    @abc.abstractmethod
    async def get_by_tg_message_id(
        self, tg_message_id: int
    ) -> Question | None:
        raise NotImplementedError()

    @abc.abstractmethod
    async def get_by_regular_user_id(
        self, regular_user_id: UUID
    ) -> list[Question]:
        raise NotImplementedError()

    @abc.abstractmethod
    async def get_unbinded(self) -> list[Question]:
        raise NotImplementedError()

    @abc.abstractmethod
    async def get_unanswered(self) -> list[Question]:
        raise NotImplementedError()

    @abc.abstractmethod
    async def delete(self, question_id: UUID) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    async def delete_by_regular_user_id(self, regular_user_id: UUID) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    async def delete_all(self) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    async def count_all(self) -> int:
        raise NotImplementedError()

    @abc.abstractmethod
    async def count_for_regular_users(self, regular_user_id: UUID) -> int:
        raise NotImplementedError()

    @abc.abstractmethod
    async def count_unanswered(self) -> int:
        raise NotImplementedError()

    @abc.abstractmethod
    async def count_answered(self) -> int:
        raise NotImplementedError()

    @abc.abstractmethod
    async def count_answered_questions(self, regular_user_id: UUID) -> int:
        raise NotImplementedError()


class AnswersRepo(abc.ABC):
    @abc.abstractmethod
    def __init__(self, repo_config: RepoConfig) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    async def add(
        self,
        answer: Answer,
    ) -> Answer:
        raise NotImplementedError()

    @abc.abstractmethod
    async def update(self, answer: Answer) -> Answer:
        raise NotImplementedError()

    @abc.abstractmethod
    async def get_all(self) -> list[Answer]:
        raise NotImplementedError()

    @abc.abstractmethod
    async def get_by_id(self, answer_id: UUID) -> Answer | None:
        raise NotImplementedError()

    @abc.abstractmethod
    async def get_question_last_answer(
        self, question_id: UUID
    ) -> Answer | None:
        raise NotImplementedError()

    @abc.abstractmethod
    async def get_by_question_id(self, question_id: UUID) -> list[Answer]:
        raise NotImplementedError()

    @abc.abstractmethod
    async def delete(self, answer_id: UUID) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    async def delete_by_support_user_id(self, support_user_id: UUID) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    async def delete_all_answers(self) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    async def get_by_support_user_id(
        self, support_user_id: UUID
    ) -> list[Answer]:
        raise NotImplementedError()

    @abc.abstractmethod
    async def get_by_tg_message_id(self, tg_message_id: int) -> Answer | None:
        raise NotImplementedError()

    @abc.abstractmethod
    async def delete_by_question_id(self, question_id: UUID) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    async def count_all(self) -> int:
        raise NotImplementedError()

    @abc.abstractmethod
    async def count_useful(self) -> int:
        raise NotImplementedError()

    @abc.abstractmethod
    async def count_unuseful_answers(self) -> int:
        raise NotImplementedError()

    @abc.abstractmethod
    async def count_by_question_id(self, question_id: UUID) -> int:
        raise NotImplementedError()

    @abc.abstractmethod
    async def count_by_support_user_id(self, support_user_id: UUID) -> int:
        raise NotImplementedError()

    @abc.abstractmethod
    async def count_useful_by_support_user_id(
        self, support_user_id: UUID
    ) -> int:
        raise NotImplementedError()

    @abc.abstractmethod
    async def count_unuseful_by_support_user_id(
        self, support_user_id: UUID
    ) -> int:
        raise NotImplementedError()

    @abc.abstractmethod
    async def count_for_regular_user(self, regular_user_id: UUID) -> int:
        raise NotImplementedError()

    @abc.abstractmethod
    async def count_useful_for_regular_user(
        self, regular_user_id: UUID
    ) -> int:
        raise NotImplementedError()

    @abc.abstractmethod
    async def count_unuseful_for_regular_user(
        self, regular_user_id: UUID
    ) -> int:
        raise NotImplementedError()

    @abc.abstractmethod
    async def count_usestimated_for_regular_user(
        self, regular_user_id: UUID
    ) -> int:
        raise NotImplementedError()
