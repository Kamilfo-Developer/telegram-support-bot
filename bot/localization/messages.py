from telegram import User
from bot.entities.regular_user import RegularUser
from bot.entities.support_user import SupportUser
from bot.entities.role import Role
from bot.entities.question import Question
from bot.entities.answer import Answer

import abc


class Messages(abc.ABC):
    @abc.abstractmethod
    async def get_start_reg_user_message(
        self,
        telegram_user: User,
        user_entity: RegularUser | None = None,
        *args,
        **kwargs
    ) -> list[str]:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_start_sup_user_message(
        self,
        telegram_user: User,
        user_entity: SupportUser | None = None,
        *args,
        **kwargs
    ) -> list[str]:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_start_owner_message(
        self,
        telegram_user: User,
        user_entity: SupportUser | None = None,
        *args,
        **kwargs
    ) -> list[str]:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_id_message(self, id: int, *args, **kwargs) -> list[str]:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_support_user_info_message(
        self,
        support_user: SupportUser,
        role: Role | None = None,
        *args,
        **kwargs
    ) -> list[str]:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_all_support_users_list_message(
        self, support_users: list[SupportUser], *args, **kwargs
    ) -> list[str]:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_incorrect_id_message(self, *args, **kwargs) -> list[str]:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_question_info_message(
        self, question: Question, regular_user: RegularUser, *args, **kwargs
    ) -> list[str]:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_permission_denied_message(
        self, user: User, *args, **kwargs
    ) -> list[str]:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_no_binded_question_message(
        self, *args, **kwargs
    ) -> list[str]:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_answer_info_message(
        self, answer: Answer, support_user: SupportUser, *args, **kwargs
    ) -> list[str]:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_owner_start_message(
        self, user: User, *args, **kwargs
    ) -> list[str]:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_already_inited_owner_message(
        self, user: User, *args, **kwargs
    ) -> list[str]:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_successful_owner_init_message(
        self, user: User, support_user: SupportUser, *args, **kwargs
    ) -> list[str]:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_successful_unbinding_message(
        self, *args, **kwargs
    ) -> list[str]:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_unsupported_message_type_message(
        self, *args, **kwargs
    ) -> list[str]:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_answer_for_regular_user_message(
        self, answer: Answer, question: Question, *args, **kwargs
    ) -> list[str]:
        raise NotImplementedError
