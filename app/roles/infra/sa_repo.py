from __future__ import annotations

from sqlalchemy import Select, delete, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload
from app.errors import EntityAlreadyExists

from app.roles.entities import Role
from app.roles.infra.sa_models import RoleModel
from app.roles.repo import RolesRepo
from app.roles.value_objects import RoleName
from app.shared.db import SADBConfig
from app.shared.value_objects import RoleIdType


class SARolesRepo(RolesRepo):
    def __init__(self, db_config: SADBConfig) -> None:
        self._session = db_config.connection_provider

    async def add(self, role: Role) -> Role:
        try:
            async with self._session() as session:
                role_model = RoleModel.from_entity(role)

                session.add(role_model)

                await session.commit()

                role._id = role_model.id  # type: ignore

                return role

        except IntegrityError:
            raise EntityAlreadyExists(
                f"Role entity with id {role._id} already exists"
            )

    async def update(self, role: Role) -> Role:
        async with self._session() as session:
            role_model = RoleModel.from_entity(role)

            await session.merge(role_model)

            await session.commit()

            return role

    async def get_by_id(self, role_id: RoleIdType) -> Role | None:
        if not role_id.is_initialized():
            return None

        async with self._session() as session:
            q = self.__get_role_query_with_options(
                select(RoleModel).where(RoleModel.id == role_id)
            )

            result = (await session.execute(q)).scalars().first()

            return result and result.as_entity()

    async def get_by_name(self, name: RoleName) -> Role | None:
        async with self._session() as session:
            q = self.__get_role_query_with_options(
                select(RoleModel).where(RoleModel.name == name)
            )

            result = (await session.execute(q)).scalars().first()

            return result and result.as_entity()

    async def get_all(self) -> list[Role]:
        async with self._session() as session:
            q = select(RoleModel).options(selectinload(RoleModel.users))

            result = (await session.execute(q)).scalars().all()

            return [elem.as_entity() for elem in result]

    async def delete(self, role_id: RoleIdType) -> None:
        async with self._session() as session:
            q = delete(RoleModel).where(RoleModel.id == role_id)

            await session.execute(q)

            await session.commit()

    async def delete_all(self) -> None:
        async with self._session() as session:
            q = delete(RoleModel)

            await session.execute(q)

            await session.commit()

    def __get_role_query_with_options(self, q: Select):
        return q
        # .options(selectinload(RoleModel.users))

    # Legacy code, the explanation can be found in app/answers/repo.py
    # async def count_all(self) -> int:
    #     async with self._session() as session:
    #         q = select(func.count(RoleModel.id))

    #         return (await session.execute(q)).scalar() or 0
