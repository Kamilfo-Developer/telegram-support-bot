from typing import Iterable
from uuid import UUID
from sqlalchemy import delete, func
from sqlalchemy.orm import selectinload
from sqlalchemy.future import select
from tests.db_test_config import async_session

from bot.db.models.sa.question_model import QuestionModel
from bot.db.models.sa.regular_user_model import RegularUserModel
from bot.db.repositories.abc.questions_repo import QuestionsRepo


class SAQuestionsRepo(QuestionsRepo):
    def __init__(self) -> None:
        self._session = async_session

    async def get_all_questions(self) -> Iterable[QuestionModel]:
        async with self._session() as session:

            q = select(QuestionModel).options(
                selectinload(QuestionModel.regular_user),
                selectinload(QuestionModel.current_support_user),
                selectinload(QuestionModel.answers),
            )

            return (await session.execute(q)).scalars().all()

    async def get_question_by_id(self, answer_id: UUID) -> QuestionModel:
        async with self._session() as session:

            q = (
                select(QuestionModel)
                .where(QuestionModel.id == answer_id)
                .options(
                    selectinload(QuestionModel.regular_user),
                    selectinload(QuestionModel.current_support_user),
                    selectinload(QuestionModel.answers),
                )
            )

            return (await session.execute(q)).scalars().first()

    async def get_all_questions_with_question_id(
        self, question_id: UUID
    ) -> Iterable[QuestionModel]:
        async with self._session() as session:

            q = (
                select(QuestionModel)
                .where(QuestionModel.question_id == question_id)
                .options(
                    selectinload(QuestionModel.regular_user),
                    selectinload(QuestionModel.current_support_user),
                    selectinload(QuestionModel.answers),
                )
            )

            return (await session.execute(q)).scalars().all()

    async def get_all_unbinded_questions(self) -> Iterable[QuestionModel]:
        async with self._session() as session:

            q = (
                select(QuestionModel)
                .where(QuestionModel.current_support_user == None)
                .options(
                    selectinload(QuestionModel.regular_user),
                    selectinload(QuestionModel.current_support_user),
                    selectinload(QuestionModel.answers),
                )
            )

            return (await session.execute(q)).scalars().all()

    async def get_all_unanswered_questions(self) -> Iterable[QuestionModel]:
        async with self._session() as session:

            q = (
                select(QuestionModel)
                .where(
                    QuestionModel.current_support_user == None
                    and QuestionModel.answers == []
                )
                .options(
                    selectinload(QuestionModel.regular_user),
                    selectinload(QuestionModel.current_support_user),
                    selectinload(QuestionModel.answers),
                )
            )

            return (await session.execute(q)).scalars().all()

    async def delete_question_with_id(self, answer_id: UUID):
        async with self._session() as session:

            q = delete(QuestionModel).where(QuestionModel.id == answer_id)

            await session.execute(q)

            await session.commit()

    async def delete_all_questions(self):
        async with self._session() as session:

            q = delete(QuestionModel)

            await session.execute(q)

            await session.commit()

    async def delete_all_questions_with_question_id(self, question_id: UUID):
        async with self._session() as session:

            q = delete(QuestionModel).where(
                QuestionModel.question_id == question_id
            )

            await session.execute(q)

            await session.commit()

    async def add_question(
        self, question: QuestionModel, regular_user: RegularUserModel
    ):
        async with self._session() as session:

            session.add(question)
            regular_user.questions.append(question)

            await session.commit()

    async def count_all_questions(self) -> int:
        async with self._session() as session:

            q = select(func.count(QuestionModel.id))

            return (await session.execute(q)).scalar()
