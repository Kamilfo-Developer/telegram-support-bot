import abc

from app.roles.entities import Role
from app.roles.value_objects import RoleName
from app.shared.db import DBConfig
from app.shared.value_objects import RoleIdType


class RolesRepo(abc.ABC):
    @abc.abstractmethod
    def __init__(self, db_config: DBConfig):
        ...

    @abc.abstractmethod
    async def add(self, role: Role) -> Role:
        ...

    @abc.abstractmethod
    async def update(self, role: Role) -> Role:
        ...

    @abc.abstractmethod
    async def get_by_id(self, role_id: RoleIdType) -> Role | None:
        ...

    @abc.abstractmethod
    async def get_by_name(self, name: RoleName) -> Role | None:
        ...

    @abc.abstractmethod
    async def get_all(self) -> list[Role]:
        ...

    @abc.abstractmethod
    async def delete(self, role_id: RoleIdType) -> None:
        ...

    @abc.abstractmethod
    async def delete_all(self) -> None:
        ...

    # Legacy code, the explanation can be found in app/answers/repo.py

    # @abc.abstractmethod
    # async def count_all(self) -> int:
    #     ...
