from telegram import User
from bot.entities.regular_user import RegularUser
from bot.entities.support_user import SupportUser


import abc


class Messages(abc.ABC):
    @abc.abstractmethod
    async def get_start_reg_user_message(
        self, telegram_user: User, user_entity: RegularUser, *args, **kwargs
    ) -> list[str]:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_start_sup_user_message(
        self, telegram_user: User, user_entity: SupportUser, *args, **kwargs
    ) -> list[str]:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_start_owner_message(
        self, telegram_user: User, user_entity: SupportUser, *args, **kwargs
    ) -> list[str]:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_get_id_message(self, id: int, *args, **kwargs) -> list[str]:
        raise NotImplementedError
