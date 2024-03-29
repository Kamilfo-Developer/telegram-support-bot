from __future__ import annotations
from uuid import UUID
from typing import TYPE_CHECKING, Any, AsyncContextManager, Callable
import abc

if TYPE_CHECKING:
    from bot.entities.support_user import SupportUser
    from bot.entities.answer import Answer
    from bot.entities.answer_attachment import AnswerAttachment
    from bot.entities.question import Question
    from bot.entities.question_attachment import QuestionAttachment
    from bot.entities.regular_user import RegularUser
    from bot.entities.role import Role


class RepoConfig(abc.ABC):
    connection_provider: Callable[..., AsyncContextManager[Any]]

    @abc.abstractmethod
    def __init__(
        self, connection_provider: Callable[..., AsyncContextManager[Any]]
    ):
        raise NotImplementedError()


class Repo(abc.ABC):
    # ROLES METHODS
    repo_config: RepoConfig

    @abc.abstractmethod
    def __init__(self, repo_config: RepoConfig):
        raise NotImplementedError()

    @abc.abstractmethod
    async def add_role(self, role: Role) -> Role:
        raise NotImplementedError()

    @abc.abstractmethod
    async def get_role_by_id(self, id: int) -> Role | None:
        raise NotImplementedError()

    @abc.abstractmethod
    async def get_role_by_name(self, name: str) -> Role | None:
        raise NotImplementedError()

    @abc.abstractmethod
    async def get_all_roles(self) -> list[Role]:
        raise NotImplementedError()

    @abc.abstractmethod
    async def get_all_roles_sorted_by_date(
        self, desc_order: bool = False
    ) -> list[Role]:
        raise NotImplementedError()

    @abc.abstractmethod
    async def delete_role_with_id(self, role_id: int) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    async def delete_all_roles(self) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    async def count_all_roles(self) -> int:
        raise NotImplementedError()

    # REGULAR USERS METHODS

    @abc.abstractmethod
    async def add_regular_user(self, regular_user: RegularUser) -> RegularUser:
        raise NotImplementedError()

    @abc.abstractmethod
    async def get_regular_user_by_id(self, id: UUID) -> RegularUser | None:
        raise NotImplementedError()

    @abc.abstractmethod
    async def get_regular_user_by_tg_bot_user_id(
        self, tg_bot_user_id: int
    ) -> RegularUser | None:
        raise NotImplementedError()

    @abc.abstractmethod
    async def get_all_regular_users(self) -> list[RegularUser]:
        raise NotImplementedError()

    @abc.abstractmethod
    async def get_all_regular_users_sorted_by_date(
        self, desc_order: bool
    ) -> list[RegularUser]:
        raise NotImplementedError()

    @abc.abstractmethod
    async def delete_regular_user_with_id(self, id: UUID) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    async def delete_all_regular_users(self) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    async def count_all_regular_users(self) -> int:
        raise NotImplementedError()

    # SUPPORT USERS METHODS

    @abc.abstractmethod
    async def add_support_user(self, support_user: SupportUser) -> SupportUser:
        raise NotImplementedError()

    @abc.abstractmethod
    async def change_support_user_role(
        self, support_user_id: UUID, new_role_id: int
    ) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    async def deactivate_support_user(self, support_user_id: UUID) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    async def activate_support_user(self, support_user_id: UUID) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    async def make_support_user_owner(self, support_user_id: UUID) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    async def remove_owner_rights_from_support_user(
        self, support_user_id: UUID
    ) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    async def get_support_user_by_id(self, id: UUID) -> SupportUser | None:
        raise NotImplementedError()

    @abc.abstractmethod
    async def get_support_user_by_tg_bot_user_id(
        self, tg_bot_user_id: int
    ) -> SupportUser | None:
        raise NotImplementedError()

    @abc.abstractmethod
    async def get_owner(self) -> SupportUser | None:
        raise NotImplementedError()

    @abc.abstractmethod
    async def get_support_users_with_role_id(
        self, role_id: int
    ) -> list[SupportUser]:
        raise NotImplementedError()

    @abc.abstractmethod
    async def get_all_support_users(self) -> list[SupportUser]:
        raise NotImplementedError()

    @abc.abstractmethod
    async def get_all_support_users_sorted_by_date(
        self, desc_order: bool
    ) -> list[SupportUser]:
        raise NotImplementedError()

    @abc.abstractmethod
    async def delete_support_user_with_id(self, id: UUID) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    async def delete_all_support_users(self) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    async def count_all_support_users(self) -> int:
        raise NotImplementedError()

    @abc.abstractmethod
    async def count_support_users_with_role(self, role_id: int) -> int:
        raise NotImplementedError()

    @abc.abstractmethod
    async def count_activated_support_users(self) -> int:
        raise NotImplementedError()

    @abc.abstractmethod
    async def count_deactivated_support_users(self) -> int:
        raise NotImplementedError()

    # QUESTIONS METHODS

    @abc.abstractmethod
    async def get_random_unbinded_question(self) -> Question | None:
        raise NotImplementedError()

    async def get_random_unanswered_unbinded_question(self) -> Question | None:
        raise NotImplementedError()

    @abc.abstractmethod
    async def get_all_questions(self) -> list[Question]:
        raise NotImplementedError()

    @abc.abstractmethod
    async def get_question_by_id(self, question_id: UUID) -> Question | None:
        raise NotImplementedError()

    @abc.abstractmethod
    async def get_regular_user_last_asked_question(
        self, regular_user_id: UUID
    ) -> Question | None:
        raise NotImplementedError()

    @abc.abstractmethod
    async def get_question_by_tg_message_id(
        self, tg_message_id: int
    ) -> Question | None:
        raise NotImplementedError()

    @abc.abstractmethod
    async def get_questions_with_regular_user_id(
        self, regular_user_id: UUID
    ) -> list[Question]:
        raise NotImplementedError()

    @abc.abstractmethod
    async def get_unbinded_questions(self) -> list[Question]:
        raise NotImplementedError()

    @abc.abstractmethod
    async def get_unanswered_questions(self) -> list[Question]:
        raise NotImplementedError()

    @abc.abstractmethod
    async def delete_question_with_id(self, question_id: UUID) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    async def delete_questions_with_regular_user_id(
        self, regular_user_id: UUID
    ) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    async def delete_all_questions(self) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    async def add_question(self, question: Question) -> Question:
        raise NotImplementedError()

    @abc.abstractmethod
    async def bind_question_to_support_user(
        self, support_user_id, question_id
    ) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    async def unbind_question_from_support_user(
        self, support_user_id: UUID
    ) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    async def count_answered_questions(self) -> int:
        raise NotImplementedError()

    @abc.abstractmethod
    async def count_unanswered_questions(self) -> int:
        raise NotImplementedError()
        raise NotImplementedError()

    @abc.abstractmethod
    async def count_regular_users_questions(
        self, regular_user_id: UUID
    ) -> int:
        raise NotImplementedError()

    @abc.abstractmethod
    async def count_all_questions(self) -> int:
        raise NotImplementedError()

    @abc.abstractmethod
    async def count_regular_user_answered_questions(
        self, regular_user_id: UUID
    ) -> int:
        raise NotImplementedError()

    # ANSWERS METHODS

    @abc.abstractmethod
    async def get_all_answers(self) -> list[Answer]:
        raise NotImplementedError()

    @abc.abstractmethod
    async def get_answer_by_id(self, answer_id: UUID) -> Answer | None:
        raise NotImplementedError()

    @abc.abstractmethod
    async def get_question_last_answer(
        self, question_id: UUID
    ) -> Answer | None:
        raise NotImplementedError()

    @abc.abstractmethod
    async def get_answers_with_question_id(
        self, question_id: UUID
    ) -> list[Answer]:
        raise NotImplementedError()

    @abc.abstractmethod
    async def delete_answer_with_id(self, answer_id: UUID) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    async def delete_support_user_answers_with_id(
        self, support_user_id: UUID
    ) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    async def delete_all_answers(self) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    async def get_support_user_answers_with_id(
        self, support_user_id: UUID
    ) -> list[Answer]:
        raise NotImplementedError()

    @abc.abstractmethod
    async def get_answer_by_tg_message_id(
        self, tg_message_id: int
    ) -> Answer | None:
        raise NotImplementedError()

    @abc.abstractmethod
    async def delete_answers_with_question_id(self, question_id: UUID) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    async def estimate_answer_as_useful(self, answer_id: UUID) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    async def estimate_answer_as_unuseful(self, answer_id: UUID) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    async def add_answer(
        self,
        answer: Answer,
    ) -> Answer:
        raise NotImplementedError()

    @abc.abstractmethod
    async def count_all_answers(self) -> int:
        raise NotImplementedError()

    @abc.abstractmethod
    async def count_all_useful_answers(self) -> int:
        raise NotImplementedError()

    @abc.abstractmethod
    async def count_all_unuseful_answers(self) -> int:
        raise NotImplementedError()

    @abc.abstractmethod
    async def count_question_answers(self, question_id: UUID) -> int:
        raise NotImplementedError()

    @abc.abstractmethod
    async def count_support_user_answers(self, support_user_id: UUID) -> int:
        raise NotImplementedError()

    @abc.abstractmethod
    async def count_support_user_useful_answers(
        self, support_user: UUID
    ) -> int:
        raise NotImplementedError()

    @abc.abstractmethod
    async def count_support_user_unuseful_answers(
        self, support_user: UUID
    ) -> int:
        raise NotImplementedError()

    @abc.abstractmethod
    async def count_regular_user_questions_answers(
        self, regular_user_id: UUID
    ) -> int:
        raise NotImplementedError()

    @abc.abstractmethod
    async def count_regular_user_questions_useful_answers(
        self, regular_user_id: UUID
    ) -> int:
        raise NotImplementedError()

    @abc.abstractmethod
    async def count_regular_user_questions_unuseful_answers(
        self, regular_user_id: UUID
    ) -> int:
        raise NotImplementedError()

    @abc.abstractmethod
    async def count_regular_user_questions_unestimated_answers(
        self, regular_user_id: UUID
    ) -> int:
        raise NotImplementedError()

    # QUESTIONS ATTACHMENTS METHODS

    @abc.abstractmethod
    async def add_question_attachment(
        self, question_attachment: QuestionAttachment
    ) -> QuestionAttachment:
        raise NotImplementedError()

    @abc.abstractmethod
    async def get_question_attachment_by_id(
        self, id: UUID
    ) -> QuestionAttachment:
        raise NotImplementedError()

    @abc.abstractmethod
    async def get_question_attachments(
        self, question_id: UUID
    ) -> list[QuestionAttachment]:
        raise NotImplementedError()

    @abc.abstractmethod
    async def get_all_questions_attachments(self) -> list[QuestionAttachment]:
        raise NotImplementedError()

    @abc.abstractmethod
    async def delete_question_attachment_with_id(
        self, question_attachment_id: UUID
    ) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    async def count_all_questions_attachments(self) -> int:
        raise NotImplementedError()

    @abc.abstractmethod
    async def count_question_attachments(self, question_id: UUID) -> int:
        raise NotImplementedError()

    # ANSWERS ATTACHMENTS METHODS
    @abc.abstractmethod
    async def add_answer_attachment(
        self, answer_attachment: AnswerAttachment
    ) -> AnswerAttachment:
        raise NotImplementedError()

    @abc.abstractmethod
    async def get_answer_attachment_by_id(self, id: UUID) -> AnswerAttachment:
        raise NotImplementedError()

    @abc.abstractmethod
    async def get_answer_attachments(
        self, answer_id: UUID
    ) -> list[AnswerAttachment]:
        raise NotImplementedError()

    @abc.abstractmethod
    async def get_all_answers_attachments(self) -> list[AnswerAttachment]:
        raise NotImplementedError()

    @abc.abstractmethod
    async def delete_answer_attachment_with_id(
        self, answer_attachment_id: UUID
    ) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    async def count_all_answers_attachments(self) -> int:
        raise NotImplementedError()

    @abc.abstractmethod
    async def count_answer_attachments(self, answer_id: UUID) -> int:
        raise NotImplementedError()
