from typing import Iterable
from uuid import UUID
from sqlalchemy import delete, func
from sqlalchemy.orm import selectinload
from sqlalchemy.future import select
from tests.db_test_config import async_session
from bot.db.models.sa.question_model import QuestionModel
from bot.db.models.sa.regular_user_model import RegularUserModel
from bot.db.models.sa.answer_model import AnswerModel
from bot.db.models.sa.support_user_model import SupportUserModel
from bot.db.models.sa.role_model import RoleModel
from bot.db.repositories.repository import Repo


class SARepo(Repo):
    def __init__(self) -> None:
        self._session = async_session

    # Roles Methods
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

    # Regular Users Methods
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

    # Regular Users Methods
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

    # Questions Methods
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

    async def get_questions_with_regular_user_id(
        self, regular_user_id: UUID
    ) -> Iterable[QuestionModel]:
        async with self._session() as session:

            q = (
                select(QuestionModel)
                .where(QuestionModel.regular_user_id == regular_user_id)
                .options(
                    selectinload(QuestionModel.regular_user),
                    selectinload(QuestionModel.current_support_user),
                    selectinload(QuestionModel.answers),
                )
            )

            return (await session.execute(q)).scalars().all()

    async def get_unbinded_questions(self) -> Iterable[QuestionModel]:
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

    async def get_unanswered_questions(self) -> Iterable[QuestionModel]:
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

    async def delete_questions_with_regular_user_id(
        self, reguar_user_id: UUID
    ):
        async with self._session() as session:

            q = delete(QuestionModel).where(QuestionModel.id == reguar_user_id)

            await session.execute(q)

            await session.commit()

    async def delete_all_questions(self):
        async with self._session() as session:

            q = delete(QuestionModel)

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

    async def count_unanswered_questions(self) -> int:
        async with self._session() as session:

            q = select(func.count(QuestionModel.id)).where(
                QuestionModel.current_support_user == None
            )

            return (await session.execute(q)).scalar()

    # Answers Methods
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

    async def get_support_user_answers_with_id(
        self, support_user_id: UUID
    ) -> Iterable[SupportUserModel]:
        async with self._session() as session:
            q = (
                select(AnswerModel)
                .where(AnswerModel.support_user_id == support_user_id)
                .options(
                    selectinload(AnswerModel.support_user),
                    selectinload(AnswerModel.question),
                )
            )

            return (await session.execute(q)).scalars().all()

    async def get_answers_with_question_id(
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

    async def delete_support_user_answers_with_id(
        self, support_user_id: UUID
    ) -> None:
        async with self._session() as session:

            q = delete(AnswerModel).where(
                AnswerModel.support_user_id == support_user_id
            )

            await session.execute(q)

            await session.commit()

    async def delete_answers_with_question_id(self, question_id: UUID) -> None:
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
