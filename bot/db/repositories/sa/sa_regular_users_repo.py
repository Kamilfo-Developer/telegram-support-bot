from typing import Iterable
from uuid import UUID
from sqlalchemy import delete, func
from sqlalchemy.orm import selectinload
from sqlalchemy.future import select
from tests.db_test_config import async_session
from bot.db.models.sa.question_model import QuestionModel
from bot.db.models.sa.regular_user_model import RegularUserModel
from bot.db.repositories.abc.regular_users_repo import RegularUsersRepo


class SARegularUsersRepo(RegularUsersRepo):
    def __init__(self) -> None:
        self._session = async_session

    async def add_regular_user(self, regular_user: RegularUserModel) -> None:
        async with self._session() as session:
            session.add(regular_user)

            await session.commit()

    async def get_regular_user_by_id(self, id: UUID) -> RegularUserModel:
        async with self._session() as session:
            q = (
                select(RegularUserModel)
                .where(RegularUserModel.id == id)
                .options(selectinload(RegularUserModel.questions))
            )

            return (await session.execute(q)).scalars().first()

    async def get_all_regular_users(self) -> Iterable[RegularUserModel]:
        async with self._session() as session:
            q = select(RegularUserModel).options(
                selectinload(RegularUserModel.questions)
            )

            return (await session.execute(q)).scalars().all()

    async def get_all_regular_users_sorted_by_date(
        self, desc_order: bool = False
    ) -> Iterable[RegularUserModel]:
        async with self._session() as session:
            q = (
                select(RegularUserModel)
                .order_by(
                    RegularUserModel.date.desc()
                    if desc_order
                    else RegularUserModel.date.asc()
                )
                .options(selectinload(RegularUserModel.questions))
            )

            return (await session.execute(q)).scalars().all()

    async def delete_regular_user_with_id(self, id: UUID) -> None:
        async with self._session() as session:
            q = delete(RegularUserModel).where(RegularUserModel.id == id)

            await session.execute(q)

            await session.commit()

    async def delete_all_regular_users(self) -> None:
        async with self._session() as session:
            q = delete(RegularUserModel)

            await session.execute(q)

            await session.commit()

    async def count_all_regular_users(self) -> int:
        async with self._session() as session:

            q = select(func.count(QuestionModel.id))

            return (await session.execute(q)).scalar()
