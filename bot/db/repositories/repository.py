from typing import Iterable
from uuid import UUID
import abc


class Repo(abc.ABC):
    # Roles Methods
    @abc.abstractmethod
    async def add_role(self, role) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_role_by_id(self, id: UUID):
        raise NotImplementedError

    @abc.abstractmethod
    async def get_all_roles(self) -> Iterable:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_all_roles_sorted_by_date(self, desc_order: bool) -> Iterable:
        raise NotImplementedError

    @abc.abstractmethod
    async def delete_role_with_id(self, id: UUID) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def delete_all_roles(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def count_all_roles(self) -> int:
        raise NotImplementedError

    # Regular Users Methods
    @abc.abstractmethod
    async def add_regular_user(self, regular_user) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_regular_user_by_id(self, id: UUID):
        raise NotImplementedError

    @abc.abstractmethod
    async def get_all_regular_users(self):
        raise NotImplementedError

    @abc.abstractmethod
    async def get_all_regular_users_sorted_by_date(self, desc_order: bool):
        raise NotImplementedError

    @abc.abstractmethod
    async def delete_regular_user_with_id(self, id: UUID) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def delete_all_regular_users(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def count_all_regular_users(self) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    # Regular Users Methods
    async def add_support_user(self, support_user) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_support_user_by_id(self, id: UUID):
        raise NotImplementedError

    @abc.abstractmethod
    async def get_all_support_users(self) -> Iterable:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_all_support_users_sorted_by_date(
        self, desc_order: bool
    ) -> Iterable:
        raise NotImplementedError

    @abc.abstractmethod
    async def delete_support_user_with_id(self, id: UUID) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def delete_all_support_users(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def count_all_support_users(self) -> int:
        raise NotImplementedError

    # Questions Methods
    @abc.abstractmethod
    async def get_all_questions(self) -> Iterable:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_question_by_id(self, answer_id: UUID):
        raise NotImplementedError

    @abc.abstractmethod
    async def get_questions_with_regular_user_id(
        self, regular_user_id: UUID
    ) -> Iterable:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_unbinded_questions(self) -> Iterable:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_unanswered_questions(self) -> Iterable:
        raise NotImplementedError

    @abc.abstractmethod
    async def delete_question_with_id(self, answer_id: UUID):
        raise NotImplementedError

    @abc.abstractmethod
    async def delete_questions_with_regular_user_id(
        self, regular_user_id: UUID
    ) -> Iterable:
        raise NotImplementedError

    @abc.abstractmethod
    async def delete_all_questions(self):
        raise NotImplementedError

    @abc.abstractmethod
    async def add_question(self, question, regular_user):
        raise NotImplementedError

    @abc.abstractmethod
    async def count_unanswered_questions(self) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    async def count_all_questions(self) -> int:
        raise NotImplementedError

    # Answers Methods
    @abc.abstractmethod
    async def get_all_answers(self) -> Iterable:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_answer_by_id(self, answer_id: UUID):
        raise NotImplementedError

    @abc.abstractmethod
    async def get_answers_with_question_id(
        self, question_id: UUID
    ) -> Iterable:
        raise NotImplementedError

    @abc.abstractmethod
    async def delete_answer_with_id(self, answer_id: UUID) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def delete_support_user_answers_with_id(
        self, support_user_id: UUID
    ) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def delete_all_answers(self) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_support_user_answers_with_id(
        self, support_user_id: UUID
    ) -> Iterable:
        raise NotImplementedError

    @abc.abstractmethod
    async def delete_answers_with_question_id(self, question_id: UUID) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def add_answer_to_question(
        self,
        answer,
        question,
        support_user,
    ) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def count_all_answers(self) -> int:
        raise NotImplementedError
