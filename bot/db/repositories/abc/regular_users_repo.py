from typing import Iterable
from uuid import UUID
import abc


class RegularUsersRepo(abc.ABC):
    @abc.abstractmethod
    async def add_support_user(self, support_user) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_support_user_by_id(self, id: UUID):
        raise NotImplementedError

    @abc.abstractmethod
    async def get_all_support_users(self) -> Iterable:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_all_support_users_sorted_by_date(self, desc_order: bool):
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
