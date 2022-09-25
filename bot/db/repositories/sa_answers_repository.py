from typing import Iterable
from datetime import datetime
from uuid import UUID
from sqlalchemy import delete, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.future import select
from tests.test_db_config import engine, async_session
from bot.db.db_config import Base
from bot.db.models.answer_model import AnswerModel
from bot.db.models.question_model import QuestionModel
from bot.db.models.regular_user_model import RegularUserModel
from bot.db.models.role_model import RoleModel
from bot.db.models.support_user_model import SupportUserModel
from bot.db.repositories.answers_repository import AnswersRepository
from bot.db.db_config import async_session
from bot.utils import get_session


class SAAnswersRepo(AnswersRepository):
    def __init__(self) -> None:
        self.session = async_session()

    async def delete_all_answers(self):
        session = self.session

        q = delete(AnswerModel)

        await session.execute(q)

    async def get_all_answers(self) -> Iterable[AnswerModel]:
        session = self.session

        q = select(AnswerModel)

        return (await session.execute(q)).scalars().all()

    async def get_answer_by_id(self, answer_id: UUID) -> AnswerModel:
        session = self.session

        q = select(AnswerModel).where(AnswerModel.id == answer_id)

        return (await session.execute(q)).scalars().first()

    async def delete_answer_with_id(self, answer_id: UUID):
        session = self.session

        q = delete(AnswerModel).where(AnswerModel.id == answer_id)

        await session.execute(q)

    async def get_all_answers_with_question_id(
        self, question_id: UUID
    ) -> Iterable[AnswerModel]:
        session = self.session

        q = select(AnswerModel).where(AnswerModel.question_id == question_id)

        return (await session.execute(q)).scalars().all()

    async def delete_all_answers_with_question_id(self, question_id: UUID):
        session = self.session

        q = delete(AnswerModel).where(AnswerModel.question_id == question_id)

        await session.execute(q)

        await session.commit()

    async def add_answer_to_question(
        self,
        answer: AnswerModel,
        question: QuestionModel,
        support_user: SupportUserModel,
    ):
        session = self.session

        question.add_answer(answer=answer)
        support_user.add_answer(answer=answer)

        await session.commit()

    async def count_all_answers(self) -> int:
        with async_session() as session:

            q = select(func.count(AnswerModel.id))

            return (await session.execute(q)).scalar()

    async def commit(self):
        try:
            await self.session.commit()
        except Exception as err:
            await self.session.rollback()
            raise err
