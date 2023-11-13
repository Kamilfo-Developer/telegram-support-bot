from app.shared.db import DBConfig
from app.shared.value_objects import RoleIdType, SupportUserIdType, TgUserId
from app.support_users.entities import SupportUser

import abc


class SupportUsersRepo(abc.ABC):
    @abc.abstractmethod
    def __init__(self, db_config: DBConfig) -> None:
        ...

    @abc.abstractmethod
    async def add(self, support_user: SupportUser) -> SupportUser:
        ...

    @abc.abstractmethod
    async def update(self, support_user: SupportUser) -> SupportUser:
        ...

    @abc.abstractmethod
    async def get_by_id(self, id: SupportUserIdType) -> SupportUser | None:
        ...

    @abc.abstractmethod
    async def get_by_tg_bot_user_id(
        self, tg_bot_user_id: TgUserId
    ) -> SupportUser | None:
        ...

    @abc.abstractmethod
    async def get_owner(self) -> SupportUser | None:
        ...

    @abc.abstractmethod
    async def get_by_role_id(self, role_id: RoleIdType) -> list[SupportUser]:
        ...

    @abc.abstractmethod
    async def get_all(self) -> list[SupportUser]:
        ...

    @abc.abstractmethod
    async def delete(self, id: SupportUserIdType) -> None:
        ...

    @abc.abstractmethod
    async def delete_all(self) -> None:
        ...

    # Count methods

    @abc.abstractmethod
    async def count_all(self) -> int:
        ...

    @abc.abstractmethod
    async def count_by_role_id(self, role_id: RoleIdType) -> int:
        ...

    @abc.abstractmethod
    async def count_activated(self) -> int:
        ...

    @abc.abstractmethod
    async def count_deactivated(self) -> int:
        ...
