from __future__ import annotations

from sqlalchemy import Select, delete, func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload

from app.errors import EntityAlreadyExists
from app.shared.db import SADBConfig
from app.shared.value_objects import RoleIdType, SupportUserIdType, TgUserId
from app.support_users.entities import SupportUser
from app.support_users.infra.sa_models import SupportUserModel
from app.support_users.repo import SupportUsersRepo


class SASupportUsersRepo(SupportUsersRepo):
    def __init__(self, db_config: SADBConfig) -> None:
        self._session = db_config.connection_provider

    async def add(self, support_user: SupportUser) -> SupportUser:
        try:
            async with self._session() as session:
                support_user_model = SupportUserModel.from_entity(
                    support_user_entity=support_user
                )

                session.add(support_user_model)

                await session.commit()

                return support_user
        except IntegrityError:
            raise EntityAlreadyExists(
                f"Support User entity with id "
                f"{support_user._id} already exists"
            )

    async def update(self, support_user: SupportUser) -> SupportUser:
        async with self._session() as session:
            support_user_model = SupportUserModel.from_entity(
                support_user_entity=support_user
            )

            await session.merge(support_user_model)

            await session.commit()

            return support_user

    async def get_by_id(
        self, support_user_id: SupportUserIdType
    ) -> SupportUser | None:
        async with self._session() as session:
            q = self.__get_support_user_query_with_options(
                select(SupportUserModel).where(
                    SupportUserModel.id == support_user_id
                )
            )

            result = (await session.execute(q)).scalars().first()

            return result and result.as_entity()

    async def get_by_tg_bot_user_id(
        self, tg_bot_user_id: TgUserId
    ) -> SupportUser | None:
        async with self._session() as session:
            q = self.__get_support_user_query_with_options(
                select(SupportUserModel).where(
                    SupportUserModel.tg_bot_user_id == tg_bot_user_id
                )
            )

            result = (await session.execute(q)).scalars().first()

            return result and result.as_entity()

    async def get_owner(self) -> SupportUser | None:
        async with self._session() as session:
            q = self.__get_support_user_query_with_options(
                select(SupportUserModel).where(
                    SupportUserModel.is_owner == True  # noqa: E712
                )
            )

            result = (await session.execute(q)).scalars().first()

            return result and result.as_entity()

    async def get_by_role_id(self, role_id: RoleIdType) -> list[SupportUser]:
        async with self._session() as session:
            q = self.__get_support_user_query_with_options(
                select(SupportUserModel).where(
                    SupportUserModel.role_id == role_id
                )
            )

            result = (await session.execute(q)).scalars().all()

            return [elem.as_entity() for elem in result]

    async def get_all(self) -> list[SupportUser]:
        async with self._session() as session:
            q = self.__get_support_user_query_with_options(
                select(SupportUserModel)
            )

            result = (await session.execute(q)).scalars().all()

            return [elem.as_entity() for elem in result]

    async def delete(self, support_user_id: SupportUserIdType) -> None:
        async with self._session() as session:
            q = self.__get_support_user_query_with_options(
                select(SupportUserModel).where(
                    SupportUserModel.id == support_user_id
                )
            )

            result = (await session.execute(q)).scalars().first()

            await session.delete(result)

            await session.commit()

    async def delete_all(self) -> None:
        async with self._session() as session:
            q = delete(SupportUserModel)

            await session.execute(q)

            await session.commit()

    # Count methods

    async def count_all(self) -> int:
        async with self._session() as session:
            q = select(func.count(SupportUserModel.id))

            return (await session.execute(q)).scalar() or 0

    async def count_by_role_id(self, role_id: RoleIdType) -> int:
        async with self._session() as session:
            q = select(func.count(SupportUserModel.id)).where(
                SupportUserModel.role_id == role_id
            )

            return (await session.execute(q)).scalar() or 0

    async def count_activated(self) -> int:
        async with self._session() as session:
            q = select(func.count(SupportUserModel.id)).where(
                SupportUserModel.is_active == True  # noqa: E712
            )

            return (await session.execute(q)).scalar() or 0

    async def count_deactivated(self) -> int:
        async with self._session() as session:
            q = select(func.count(SupportUserModel.id)).where(
                SupportUserModel.is_active == False  # noqa: E712
            )

            return (await session.execute(q)).scalar() or 0

    def __get_support_user_query_with_options(self, q: Select):
        return q.options(
            # selectinload(SupportUserModel.current_question).selectinload(
            #     QuestionModel.regular_user
            # ),
            # selectinload(SupportUserModel.current_question).selectinload(
            #     QuestionModel.current_support_user
            # ),
            # selectinload(SupportUserModel.current_question).selectinload(
            #     QuestionModel.question_attachments
            # ),
            selectinload(SupportUserModel.role),
            # selectinload(SupportUserModel.current_question).selectinload(
            #     QuestionModel.regular_user
            # ),
        )
