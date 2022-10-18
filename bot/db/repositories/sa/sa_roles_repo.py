from typing import Iterable
from uuid import UUID
from sqlalchemy import delete, func
from sqlalchemy.orm import selectinload
from sqlalchemy.future import select
from tests.db_test_config import async_session
from bot.db.models.sa.question_model import QuestionModel
from bot.db.models.sa.role_model import RoleModel
from bot.db.repositories.abc.roles_repo import RolesRepo


class SARolesRepo(RolesRepo):
    def __init__(self) -> None:
        self._session = async_session

    async def add_role(self, role: RoleModel) -> None:
        async with self._session() as session:
            session.add(role)
            await session.commit()

    async def get_role_by_id(self, id: UUID) -> RoleModel:
        async with self._session() as session:
            q = (
                select(RoleModel)
                .where(RoleModel.id == id)
                .options(selectinload(RoleModel.users))
            )

            return (await session.execute(q)).scalars().first()

    async def get_all_roles(self) -> Iterable[RoleModel]:
        async with self._session() as session:
            q = select(RoleModel).options(selectinload(RoleModel.users))

            return (await session.execute(q)).scalars().all()

    async def get_all_roles_sorted_by_date(
        self, desc_order: bool = False
    ) -> Iterable[RoleModel]:
        async with self._session() as session:
            q = (
                select(RoleModel)
                .order_by(
                    RoleModel.date.desc()
                    if desc_order
                    else RoleModel.date.asc()
                )
                .options(selectinload(RoleModel.users))
            )

            return (await session.execute(q)).scalars().all()

    async def delete_role_with_id(self, id: UUID) -> None:
        async with self._session() as session:
            q = delete(RoleModel).where(RoleModel.id == id)

            await session.execute(q)

            await session.commit()

    async def delete_all_roles(self) -> None:
        async with self._session() as session:
            q = delete(RoleModel)

            await session.execute(q)

            await session.commit()

    async def count_all_roles(self) -> int:
        async with self._session() as session:

            q = select(func.count(QuestionModel.id))

            return (await session.execute(q)).scalar()
