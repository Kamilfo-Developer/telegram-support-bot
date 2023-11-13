import abc

from app.regular_users.entities import RegularUser
from app.shared.db import DBConfig
from app.shared.value_objects import RegularUserIdType, TgUserId


class RegularUsersRepo(abc.ABC):
    @abc.abstractmethod
    def __init__(self, db_config: DBConfig) -> None:
        ...

    @abc.abstractmethod
    async def add(self, regular_user: RegularUser) -> RegularUser:
        ...

    @abc.abstractmethod
    async def update(self, regular_user: RegularUser) -> RegularUser:
        ...

    @abc.abstractmethod
    async def get_by_id(
        self, regular_user_id: RegularUserIdType
    ) -> RegularUser | None:
        ...

    @abc.abstractmethod
    async def get_by_tg_bot_user_id(
        self, tg_bot_user_id: TgUserId
    ) -> RegularUser | None:
        ...

    @abc.abstractmethod
    async def get_all(self) -> list[RegularUser]:
        ...

    @abc.abstractmethod
    async def delete(self, regular_user_id: RegularUserIdType) -> None:
        ...

    @abc.abstractmethod
    async def delete_all(self) -> None:
        ...

    # Legacy code, the explanation can be found in app/answers/repo.py
    # @abc.abstractmethod
    # async def count_all(self) -> int:
    #     ...
