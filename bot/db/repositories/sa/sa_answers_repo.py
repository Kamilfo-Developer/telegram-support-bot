from typing import Iterable
from uuid import UUID
from sqlalchemy import delete, func
from sqlalchemy.orm import selectinload
from sqlalchemy.future import select
from tests.db_test_config import async_session
from bot.db.models.sa.answer_model import AnswerModel
from bot.db.models.sa.question_model import QuestionModel
from bot.db.models.sa.support_user_model import SupportUserModel
from bot.db.repositories.abc.answers_repo import AnswersRepo


class SAAnswersRepo(AnswersRepo):
    def __init__(self) -> None:
        self._session = async_session

    async def get_all_answers(self) -> Iterable[AnswerModel]:
        async with self._session() as session:
            q = select(AnswerModel).options(
                selectinload(AnswerModel.support_user),
                selectinload(AnswerModel.question),
            )

            return (await session.execute(q)).scalars().all()

    async def get_answer_by_id(self, answer_id: UUID) -> AnswerModel:
        async with self._session() as session:

            q = (
                select(AnswerModel)
                .where(AnswerModel.id == answer_id)
                .options(
                    selectinload(AnswerModel.support_user),
                    selectinload(AnswerModel.question),
                )
            )

            return (await session.execute(q)).scalars().first()

    async def get_all_answers_with_question_id(
        self, question_id: UUID
    ) -> Iterable[AnswerModel]:
        async with self._session() as session:

            q = (
                select(AnswerModel)
                .where(AnswerModel.question_id == question_id)
                .options(
                    selectinload(AnswerModel.support_user),
                    selectinload(AnswerModel.question),
                )
            )

            return (await session.execute(q)).scalars().all()

    async def delete_answer_with_id(self, answer_id: UUID) -> None:
        async with self._session() as session:

            q = delete(AnswerModel).where(AnswerModel.id == answer_id)

            await session.execute(q)

            await session.commit()

    async def delete_all_answers(self) -> None:
        async with self._session() as session:

            q = delete(AnswerModel)

            await session.execute(q)

            await session.commit()

    async def delete_all_answers_with_question_id(
        self, question_id: UUID
    ) -> None:
        async with self._session() as session:

            q = delete(AnswerModel).where(
                AnswerModel.question_id == question_id
            )

            await session.execute(q)

            await session.commit()

    async def add_answer_to_question(
        self,
        answer: AnswerModel,
        question: QuestionModel,
        support_user: SupportUserModel,
    ) -> None:
        async with self._session() as session:

            session.add(question)
            session.add(support_user)
            session.add(answer)

            question.add_answer(answer=answer)
            support_user.add_answer(answer=answer)

            await session.commit()

    async def count_all_answers(self) -> int:
        async with self._session() as session:

            q = select(func.count(AnswerModel.id))

            return (await session.execute(q)).scalar()
