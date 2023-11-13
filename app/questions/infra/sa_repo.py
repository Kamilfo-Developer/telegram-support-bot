from __future__ import annotations

from sqlalchemy import Select, and_, delete, func, select
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError
from app.errors import EntityAlreadyExists

from app.questions.entities import Question
from app.questions.infra.sa_models import QuestionModel
from app.questions.repo import QuestionsRepo
from app.shared.db import DBConfig
from app.shared.value_objects import (
    QuestionIdType,
    RegularUserIdType,
    TgMessageIdType,
)


class SAQuestionsRepo(QuestionsRepo):
    def __init__(self, db_config: DBConfig) -> None:
        self._session = db_config.connection_provider

    async def add(self, question: Question) -> Question:
        try:
            async with self._session() as session:
                question_model = QuestionModel.from_entity(question)

                session.add(question_model)

                await session.commit()

                return question
        except IntegrityError:
            raise EntityAlreadyExists(
                f"Question entity with id {question._id} already exists"
            )

    async def update(self, question: Question) -> Question:
        async with self._session() as session:
            question_model = QuestionModel.from_entity(question)

            await session.merge(question_model)

            await session.commit()

            return question_model.as_entity()

    async def get_random_unbound(self) -> Question | None:
        async with self._session() as session:
            q = self.__get_question_query_with_options(
                select(QuestionModel)
                .where(QuestionModel.current_support_user == None)
                .order_by(func.random())
                .limit(1)
            )

            result = (await session.execute(q)).scalars().first()

            return result and result.as_entity()

    async def get_random_unanswered_unbound(self) -> Question | None:
        async with self._session() as session:
            q = self.__get_question_query_with_options(
                select(QuestionModel)
                .where(QuestionModel.current_support_user == None)
                .where(QuestionModel.answers == None)
                .order_by(func.random())
                .limit(1)
            )

            result = (await session.execute(q)).scalars().first()

            return result and result.as_entity()

    async def get_random_answered(self) -> Question | None:
        async with self._session() as session:
            q = self.__get_question_query_with_options(
                select(QuestionModel)
                .where(QuestionModel.answers != None)
                .order_by(func.random())
                .limit(1)
            )

            result = (await session.execute(q)).scalars().first()

            return result and result.as_entity()

    async def get_all(self) -> list[Question]:
        async with self._session() as session:
            q = self.__get_question_query_with_options(select(QuestionModel))

            result = (await session.execute(q)).scalars().all()

            return [elem.as_entity() for elem in result]

    async def get_by_id(self, question_id: QuestionIdType) -> Question | None:
        async with self._session() as session:
            q = self.__get_question_query_with_options(
                select(QuestionModel).where(QuestionModel.id == question_id)
            )

            result = (await session.execute(q)).scalars().first()

            return result and result.as_entity()

    async def get_last_asked(
        self, regular_user_id: RegularUserIdType
    ) -> Question | None:
        async with self._session() as session:
            q = self.__get_question_query_with_options(
                select(QuestionModel)
                .where(QuestionModel.regular_user_id == regular_user_id)
                .order_by(QuestionModel.date.desc())
            )

            result = (await session.execute(q)).scalars().first()

            return result and result.as_entity()

    async def get_by_tg_message_id(
        self, tg_message_id: TgMessageIdType
    ) -> Question | None:
        async with self._session() as session:
            q = self.__get_question_query_with_options(
                select(QuestionModel).where(
                    QuestionModel.tg_message_id == tg_message_id
                )
            )

            result = (await session.execute(q)).scalars().first()

            return result and result.as_entity()

    async def get_by_regular_user_id(
        self, regular_user_id: RegularUserIdType
    ) -> list[Question]:
        async with self._session() as session:
            q = self.__get_question_query_with_options(
                select(QuestionModel).where(
                    QuestionModel.regular_user_id == regular_user_id
                )
            )

            result = (await session.execute(q)).scalars().all()

            return [elem.as_entity() for elem in result]

    async def get_unbound(self) -> list[Question]:
        async with self._session() as session:
            q = self.__get_question_query_with_options(
                select(QuestionModel).where(
                    QuestionModel.current_support_user == None
                )
            )

            result = (await session.execute(q)).scalars().all()

            return [elem.as_entity() for elem in result]

    async def get_unanswered(self) -> list[Question]:
        async with self._session() as session:
            q = self.__get_question_query_with_options(
                select(QuestionModel).where(
                    and_(
                        QuestionModel.current_support_user == None,
                        QuestionModel.answers == None,
                    )  # type: ignore
                )
            )

            result = (await session.execute(q)).scalars().all()

            return [elem.as_entity() for elem in result]

    async def delete(self, question_id: QuestionIdType) -> None:
        async with self._session() as session:
            q = delete(QuestionModel).where(QuestionModel.id == question_id)

            await session.execute(q)

            await session.commit()

    async def delete_by_regular_user_id(
        self, regular_user_id: RegularUserIdType
    ) -> None:
        async with self._session() as session:
            q = delete(QuestionModel).where(
                QuestionModel.regular_user_id == regular_user_id
            )

            await session.execute(q)

            await session.commit()

    async def delete_all(self) -> None:
        async with self._session() as session:
            q = delete(QuestionModel)

            await session.execute(q)

            await session.commit()

    def __get_question_query_with_options(self, q: Select):
        return q.options(
            # selectinload(QuestionModel.regular_user),
            # selectinload(QuestionModel.current_support_user),
            selectinload(QuestionModel.question_attachments),
        )

    # Legacy code. Explanation can be found in app/answers/repo.py

    # async def count_all(self) -> int:
    #     async with self._session() as session:
    #         q = select(func.count(QuestionModel.id))

    #         return (await session.execute(q)).scalar()

    # async def count_by_regular_user_id(
    #     self, regular_user_id: RegularUserIdType
    # ) -> int:
    #     async with self._session() as session:
    #         q = select(func.count(QuestionModel.id)).where(
    #             QuestionModel.regular_user_id == regular_user_id
    #         )

    #         return (await session.execute(q)).scalar()

    # async def count_unanswered(self) -> int:
    #     async with self._session() as session:
    #         q = select(func.count(QuestionModel.id)).where(
    #             QuestionModel.answers == None
    #         )

    #         return (await session.execute(q)).scalar()

    # async def count_answered(self) -> int:
    #     async with self._session() as session:
    #         q = select(func.count(QuestionModel.id)).where(
    #             QuestionModel.answers != None
    #         )

    #         return (await session.execute(q)).scalar()

    # async def count_answerd_by_regular_user_id(
    #     self, regular_user_id: RegularUserIdType
    # ) -> int:
    #     async with self._session() as session:
    #         q = select(func.count(QuestionModel.id)).where(
    #             and_(
    #                 QuestionModel.regular_user_id == regular_user_id,
    #                 QuestionModel.answers != None,  # noqa: 712
    #             )
    #         )

    #         return (await session.execute(q)).scalar()
