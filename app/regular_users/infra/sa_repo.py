from __future__ import annotations

from sqlalchemy import Select, delete, select
from sqlalchemy.exc import IntegrityError

from app.errors import EntityAlreadyExists
from app.regular_users.entities import RegularUser
from app.regular_users.infra.sa_models import RegularUserModel
from app.regular_users.repo import RegularUsersRepo
from app.shared.db import SADBConfig
from app.shared.value_objects import RegularUserIdType


class SARegularUsersRepo(RegularUsersRepo):
    def __init__(self, db_config: SADBConfig) -> None:
        self._session = db_config.connection_provider

    async def add(self, regular_user: RegularUser) -> RegularUser:
        try:
            async with self._session() as session:
                regular_user_model = RegularUserModel.from_entity(regular_user)

                session.add(regular_user_model)

                await session.commit()

                return regular_user

        except IntegrityError:
            raise EntityAlreadyExists(
                f"Regular User entity with id "
                f"{regular_user._id} already exists"
            )

    async def update(self, regular_user: RegularUser) -> RegularUser:
        async with self._session() as session:
            regular_user_model = RegularUserModel.from_entity(regular_user)

            await session.merge(regular_user_model)

            await session.commit()

            return regular_user

    async def get_by_id(
        self, regular_user_id: RegularUserIdType
    ) -> RegularUser | None:
        async with self._session() as session:
            q = self.__get_regular_user_query_with_options(
                select(RegularUserModel).where(
                    RegularUserModel.id == regular_user_id
                )
            )

            result = (await session.execute(q)).scalars().first()

            return result and result.as_entity()

    async def get_by_tg_bot_user_id(
        self, tg_bot_user_id: int
    ) -> RegularUser | None:
        async with self._session() as session:
            q = self.__get_regular_user_query_with_options(
                select(RegularUserModel).where(
                    RegularUserModel.tg_bot_user_id == tg_bot_user_id
                )
            )

            result = (await session.execute(q)).scalars().first()

            return result and result.as_entity()

    async def get_all(self) -> list[RegularUser]:
        async with self._session() as session:
            q = self.__get_regular_user_query_with_options(
                select(RegularUserModel)
            )

            result = (await session.execute(q)).scalars().all()

            return [elem.as_entity() for elem in result]

    async def delete(self, regular_user_id: RegularUserIdType) -> None:
        async with self._session() as session:
            q = delete(RegularUserModel).where(
                RegularUserModel.id == regular_user_id
            )

            await session.execute(q)

            await session.commit()

    async def delete_all(self) -> None:
        async with self._session() as session:
            q = delete(RegularUserModel)

            await session.execute(q)

            await session.commit()

    def __get_regular_user_query_with_options(self, q: Select):
        return q
        # .options(selectinload(RegularUserModel.questions))

    # Legacy code, the explanation can be found in app/answers/repo.py

    # async def count_all(self) -> int:
    #     async with self._session() as session:
    #         q = select(func.count(RegularUserModel.id))

    #         return (await session.execute(q)).scalar() or 0
