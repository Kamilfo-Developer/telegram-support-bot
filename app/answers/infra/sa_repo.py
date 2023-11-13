from __future__ import annotations

from sqlalchemy import Select, delete, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload

from app.answers.entities import Answer
from app.answers.infra.sa_models import AnswerModel
from app.answers.repo import AnswersRepo
from app.errors import EntityAlreadyExists
from app.shared.db import SADBConfig
from app.shared.value_objects import (
    AnswerIdType,
    QuestionIdType,
    SupportUserIdType,
    TgMessageIdType,
)


class SAAnswersRepo(AnswersRepo):
    def __init__(self, db_config: SADBConfig) -> None:
        self._session = db_config.connection_provider

    async def add(
        self,
        answer: Answer,
    ) -> Answer:
        try:
            async with self._session() as session:
                answer_model = AnswerModel.from_entity(answer)

                session.add(answer_model)

                await session.commit()

                return answer

        except IntegrityError:
            raise EntityAlreadyExists(
                f"Answer entity with id {answer._id} already exists"
            )

    async def update(self, answer: Answer) -> Answer:
        async with self._session() as session:
            answer_model = AnswerModel.from_entity(answer)

            await session.merge(answer_model)

            await session.commit()

            return answer

    async def get_all(self) -> list[Answer]:
        async with self._session() as session:
            q = self.__get_answer_query_with_options(select(AnswerModel))

            result = (await session.execute(q)).scalars().all()

            return [elem.as_entity() for elem in result]

    async def get_by_id(self, answer_id: AnswerIdType) -> Answer | None:
        async with self._session() as session:
            q = self.__get_answer_query_with_options(
                select(AnswerModel).where(AnswerModel.id == answer_id)
            )

            result = (await session.execute(q)).scalars().first()

            return result and result.as_entity()

    async def get_question_last_answer(
        self, question_id: QuestionIdType
    ) -> Answer | None:
        async with self._session() as session:
            q = self.__get_answer_query_with_options(
                select(AnswerModel)
                .where(AnswerModel.question_id == question_id)
                .order_by(AnswerModel.date.desc())
            )

            result = (await session.execute(q)).scalars().first()

            return result and result.as_entity()

    async def get_by_support_user_id(
        self, support_user_id: SupportUserIdType
    ) -> list[Answer]:
        async with self._session() as session:
            q = self.__get_answer_query_with_options(
                select(AnswerModel).where(
                    AnswerModel.support_user_id == support_user_id
                )
            )

            result = (await session.execute(q)).scalars().all()

            return [elem.as_entity() for elem in result]

    async def get_by_question_id(
        self, question_id: QuestionIdType
    ) -> list[Answer]:
        async with self._session() as session:
            q = self.__get_answer_query_with_options(
                select(AnswerModel).where(
                    AnswerModel.question_id == question_id
                )
            )

            result = (await session.execute(q)).scalars().all()

            return [elem.as_entity() for elem in result]

    async def get_by_tg_message_id(
        self, tg_mesage_id: TgMessageIdType
    ) -> Answer | None:
        async with self._session() as session:
            q = self.__get_answer_query_with_options(
                select(AnswerModel).where(
                    AnswerModel.tg_message_id == tg_mesage_id
                )
            )

            result = (await session.execute(q)).scalars().first()

            return result and result.as_entity()

    async def delete(self, answer_id: AnswerIdType) -> None:
        async with self._session() as session:
            q = delete(AnswerModel).where(AnswerModel.id == answer_id)

            await session.execute(q)

            await session.commit()

    async def delete_by_support_user_id(
        self, support_user_id: SupportUserIdType
    ) -> None:
        async with self._session() as session:
            q = delete(AnswerModel).where(
                AnswerModel.support_user_id == support_user_id
            )

            await session.execute(q)

            await session.commit()

    async def delete_all(self) -> None:
        async with self._session() as session:
            q = delete(AnswerModel)

            await session.execute(q)

            await session.commit()

    async def delete_by_question_id(self, question_id: QuestionIdType) -> None:
        async with self._session() as session:
            q = delete(AnswerModel).where(
                AnswerModel.question_id == question_id
            )

            await session.execute(q)

            await session.commit()

    def __get_answer_query_with_options(self, q: Select):
        return q.options(
            # Why these lines? Just legacy. I don't want to remove them
            # in case we're gonna load some more data with an answer entity.
            #
            #
            # selectinload(AnswerModel.question).selectinload(
            #     QuestionModel.regular_user
            # ),
            # selectinload(AnswerModel.question).selectinload(
            #     QuestionModel.question_attachments
            # ),
            # # SUPPORT USER AND ITS CURRENT QUESTIONS PROPERTIES
            # selectinload(AnswerModel.support_user)
            # .selectinload(SupportUserModel.current_question)
            # .selectinload(QuestionModel.regular_user),
            # selectinload(AnswerModel.support_user)
            # .selectinload(SupportUserModel.current_question)
            # .selectinload(QuestionModel.question_attachments),
            # # SUPPORT USER ROLE
            # selectinload(AnswerModel.support_user).selectinload(
            #     SupportUserModel.role
            # ),
            #
            #
            # Attachments
            selectinload(AnswerModel.answer_attachments),
        )

    def __get_answer_attachment_query_with_options(self, q: Select):
        return q
        # .options(selectinload(AnswerAttachmentModel.answer))

    # NOTE: The next code is supposed to count answers
    # but since the logic migrated to `app/service` module,
    # we don't really need to have thes methods.
    # But they are going to be here in case we need them
    # for some reasons.

    # async def count_all(self) -> int:
    #     async with self._session() as session:
    #         q = select(func.count(AnswerModel.id))

    #         return (await session.execute(q)).scalar() or 0

    # async def count_useful(self) -> int:
    #     async with self._session() as session:
    #         q = select(func.count(AnswerModel.id)).where(
    #             AnswerModel.is_useful == True  # noqa: 712
    #         )

    #         return (await session.execute(q)).scalar() or 0

    # async def count_unuseful_answers(self) -> int:
    #     async with self._session() as session:
    #         q = select(func.count(AnswerModel.id)).where(
    #             AnswerModel.is_useful == False  # noqa: 712
    #         )

    #         return (await session.execute(q)).scalar() or 0

    # async def count_by_question_id(self, question_id: QuestionIdType) -> int:
    #     async with self._session() as session:
    #         q = select(func.count(AnswerModel.id)).where(
    #             AnswerModel.question_id == question_id
    #         )

    #         return (await session.execute(q)).scalar() or 0

    # async def count_by_support_user_id(
    #     self, support_user_id: SupportUserIdType
    # ) -> int:
    #     async with self._session() as session:
    #         q = select(func.count(AnswerModel.id)).where(
    #             AnswerModel.support_user_id == support_user_id
    #         )

    #         return (await session.execute(q)).scalar() or 0

    # async def count_useful_by_support_user_id(
    #     self, support_user_id: SupportUserIdType
    # ) -> int:
    #     async with self._session() as session:
    #         q = select(func.count(AnswerModel.id)).where(
    #             and_(
    #                 AnswerModel.is_useful == True,  # noqa: 712
    #                 AnswerModel.support_user_id == support_user_id,
    #             )
    #         )

    #         return (await session.execute(q)).scalar() or 0

    # async def count_unuseful_by_support_user_id(
    #     self, support_user_id: SupportUserIdType
    # ) -> int:
    #     async with self._session() as session:
    #         q = select(func.count(AnswerModel.id)).where(
    #             and_(
    #                 AnswerModel.is_useful == False,  # noqa: 712
    #                 AnswerModel.support_user_id == support_user_id,
    #             )
    #         )

    #         return (await session.execute(q)).scalar() or 0

    # async def count_for_regular_user(
    #     self, regular_user_id: RegularUserIdType
    # ) -> int:
    #     async with self._session() as session:
    #         q = select(func.count(AnswerModel.id)).where(
    #             and_(
    #                 AnswerModel.question.and_(
    #                     QuestionModel.regular_user_id == regular_user_id
    #                 ),
    #             )
    #         )

    #         return (await session.execute(q)).scalar() or 0

    # async def count_useful_for_regular_user(
    #     self, regular_user_id: RegularUserIdType
    # ) -> int:
    #     async with self._session() as session:
    #         q = select(func.count(AnswerModel.id)).where(
    #             and_(
    #                 AnswerModel.question.and_(
    #                     QuestionModel.regular_user_id == regular_user_id
    #                 ),
    #                 AnswerModel.is_useful == True,  # noqa: 712
    #             )
    #         )

    #         return (await session.execute(q)).scalar() or 0

    # async def count_unuseful_for_regular_user(
    #     self, regular_user_id: RegularUserIdType
    # ) -> int:
    #     async with self._session() as session:
    #         q = select(func.count(AnswerModel.id)).where(
    #             and_(
    #                 AnswerModel.question.and_(
    #                     QuestionModel.regular_user_id == regular_user_id
    #                 ),
    #                 AnswerModel.is_useful == False,  # noqa: 712
    #             )
    #         )

    #         return (await session.execute(q)).scalar() or 0

    # async def count_usestimated_for_regular_user(
    #     self, regular_user_id: RegularUserIdType
    # ) -> int:
    #     async with self._session() as session:
    #         q = select(func.count(AnswerModel.id)).where(
    #             and_(
    #                 AnswerModel.question.and_(
    #                     QuestionModel.regular_user_id == regular_user_id
    #                 ),
    #                 AnswerModel.is_useful == None,  # noqa: 712
    #             )
    #         )

    #         return (await session.execute(q)).scalar() or 0
