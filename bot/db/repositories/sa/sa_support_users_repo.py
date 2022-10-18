from typing import Iterable
from uuid import UUID
from sqlalchemy import delete, func
from sqlalchemy.orm import selectinload
from sqlalchemy.future import select
from tests.db_test_config import async_session
from bot.db.models.sa.question_model import QuestionModel
from bot.db.models.sa.support_user_model import SupportUserModel
from bot.db.repositories.abc.support_users_repo import SupportUsersRepo


class SASupportUsersRepo(SupportUsersRepo):
    def __init__(self) -> None:
        self._session = async_session

    async def add_support_user(self, support_user: SupportUserModel) -> None:
        async with self._session() as session:
            session.add(support_user)

            await session.commit()

    async def get_support_user_by_id(self, id: UUID) -> SupportUserModel:
        async with self._session() as session:
            q = (
                select(SupportUserModel)
                .where(SupportUserModel.id == id)
                .options(
                    selectinload(SupportUserModel.answers),
                    selectinload(SupportUserModel.current_question),
                    selectinload(SupportUserModel.role),
                )
            )

            return (await session.execute(q)).scalars().first()

    async def get_all_support_users(self) -> Iterable[SupportUserModel]:
        async with self._session() as session:
            q = select(SupportUserModel).options(
                selectinload(SupportUserModel.answers),
                selectinload(SupportUserModel.current_question),
                selectinload(SupportUserModel.role),
            )

            return (await session.execute(q)).scalars().all()

    async def get_all_support_users_sorted_by_date(
        self, desc_order: bool = False
    ) -> Iterable[SupportUserModel]:
        async with self._session() as session:
            q = (
                select(SupportUserModel)
                .order_by(
                    SupportUserModel.date.desc()
                    if desc_order
                    else SupportUserModel.date.asc()
                )
                .options(
                    selectinload(SupportUserModel.answers),
                    selectinload(SupportUserModel.current_question),
                    selectinload(SupportUserModel.role),
                )
            )

            return (await session.execute(q)).scalars().all()

    async def delete_support_user_with_id(self, id: UUID) -> None:
        async with self._session() as session:
            q = delete(SupportUserModel).where(SupportUserModel.id == id)

            await session.execute(q)

            await session.commit()

    async def delete_all_support_users(self) -> None:
        async with self._session() as session:
            q = delete(SupportUserModel)

            await session.execute(q)

            await session.commit()

    async def count_all_support_users(self) -> int:
        async with self._session() as session:

            q = select(func.count(QuestionModel.id))

            return (await session.execute(q)).scalar()
