from uuid import UUID
from sqlalchemy import delete, func
from sqlalchemy.orm import selectinload
from sqlalchemy.future import select
from bot.entities.answer import Answer
from bot.entities.question import Question
from bot.entities.regular_user import RegularUser
from bot.entities.role import Role
from bot.entities.support_user import SupportUser
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
    async def add_role(self, role: Role) -> None:
        async with self._session() as session:
            role_model = RoleModel(
                id=role.id,
                name=role.name,
                description=role.description,
                can_answer_questions=role.can_answer_questions,
                can_manage_support_users=role.can_manage_support_users,
                created_date=role.created_date,
            )

            session.add(role_model)

            await session.commit()

    async def change_support_user_role(
        self, support_user_id: UUID, new_role_id: UUID
    ) -> None:
        async with self._session() as session:
            q = (
                select(SupportUserModel)
                .where(SupportUserModel.id == support_user_id)
                .options(selectinload(SupportUserModel.role))
            )

            support_user = (await session.execute(q)).scalars().first()

            q = select(RoleModel).where(RoleModel.id == new_role_id)

            role = (await session.execute(q)).scalars().first()

            support_user.role = role

            session.commit()

    async def get_role_by_id(self, id: UUID) -> Role:
        async with self._session() as session:
            q = (
                select(RoleModel)
                .where(RoleModel.id == id)
                .options(selectinload(RoleModel.users))
            )

            result = (await session.execute(q)).scalars().first()

            return result and result.as_role_entity()

    async def get_role_by_name(self, name: str) -> Role:
        async with self._session() as session:
            q = (
                select(RoleModel)
                .where(RoleModel.name == name)
                .options(selectinload(RoleModel.users))
            )

            result = (await session.execute(q)).scalars().first()

            return result and result.as_role_entity()

    async def get_all_roles(self) -> list[Role]:
        async with self._session() as session:
            q = select(RoleModel).options(selectinload(RoleModel.users))

            result = (await session.execute(q)).scalars().all()

            return [elem.as_role_entity() for elem in result]

    async def get_all_roles_sorted_by_date(
        self, desc_order: bool = False
    ) -> list[RoleModel]:
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

            result = (await session.execute(q)).scalars().all()

            return [elem.as_role_entity() for elem in result]

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
    async def add_regular_user(self, regular_user: RegularUser) -> None:
        async with self._session() as session:
            regular_user_model = RegularUserModel(
                id=regular_user.id,
                tg_bot_user_id=regular_user.tg_bot_user_id,
                join_date=regular_user.join_date,
            )

            session.add(regular_user_model)

            await session.commit()

    async def get_regular_user_by_id(self, id: UUID) -> RegularUser:
        async with self._session() as session:
            q = (
                select(RegularUserModel)
                .where(RegularUserModel.id == id)
                .options(selectinload(RegularUserModel.questions))
            )

            result = (await session.execute(q)).scalars().first()

            return result and result.as_regular_user_entity()

    async def get_regular_user_by_tg_bot_user_id(
        self, tg_bot_user_id: int
    ) -> RegularUser:
        async with self._session() as session:
            q = (
                select(RegularUserModel)
                .where(RegularUserModel.tg_bot_user_id == tg_bot_user_id)
                .options(
                    selectinload(RegularUserModel.questions),
                )
            )

            result = (await session.execute(q)).scalars().first()

            return result and result.as_regular_user_entity()

    async def get_all_regular_users(self) -> list[RegularUser]:
        async with self._session() as session:
            q = select(RegularUserModel).options(
                selectinload(RegularUserModel.questions)
            )

            result = (await session.execute(q)).scalars().all()

            return [elem.as_regular_user_entity() for elem in result]

    async def get_all_regular_users_sorted_by_date(
        self, desc_order: bool = False
    ) -> list[RegularUser]:
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

            result = (await session.execute(q)).scalars().all()

            return [elem.as_regular_user_entity() for elem in result]

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
    async def add_support_user(self, support_user: SupportUser) -> None:
        async with self._session() as session:
            support_user_model = SupportUserModel(
                id=support_user.id,
                current_question_id=support_user.current_question_id,
                role_id=support_user.role_id,
                descriptive_name=support_user.descriptive_name,
                tg_bot_user_id=support_user.tg_bot_user_id,
                join_date=support_user.join_date,
                is_owner=support_user.is_owner,
            )

            session.add(support_user_model)

            await session.commit()

    async def bind_question_to_support_user(
        self, support_user_id: UUID, question_id: UUID
    ) -> None:
        async with self._session() as session:
            q = (
                select(SupportUserModel)
                .where(SupportUserModel.id == support_user_id)
                .options(selectinload(SupportUserModel.role))
            )

            support_user = (await session.execute(q)).scalars().first()

            support_user.current_question_id = question_id

            await session.commit()

    async def unbind_question_from_support_user(
        self, support_user_id: UUID
    ) -> None:
        async with self._session() as session:
            q = select(SupportUserModel).where(
                SupportUserModel.id == support_user_id
            )

            support_user: SupportUserModel = (
                (await session.execute(q)).scalars().first()
            )

            support_user.current_question = None

            await session.commit()

    async def make_support_user_owner(self, support_user_id: UUID) -> None:
        async with self._session() as session:
            q = select(SupportUserModel).where(
                SupportUserModel.id == support_user_id
            )

            support_user: SupportUserModel = (
                (await session.execute(q)).scalars().first()
            )

            support_user.is_owner = True

            await session.commit()

    async def remove_owner_rights_from_support_user(
        self, support_user_id: UUID
    ) -> None:
        async with self._session() as session:
            q = select(SupportUserModel).where(
                SupportUserModel.id == support_user_id
            )

            support_user: SupportUserModel = (
                (await session.execute(q)).scalars().first()
            )

            support_user.is_owner = False

            await session.commit()

    async def get_support_user_by_id(self, id: UUID) -> SupportUser:
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

            result = (await session.execute(q)).scalars().first()

            return result and result.as_support_user_entity()

    async def get_support_user_by_tg_bot_user_id(
        self, tg_bot_user_id: int
    ) -> SupportUser:
        async with self._session() as session:
            q = (
                select(SupportUserModel)
                .where(SupportUserModel.tg_bot_user_id == tg_bot_user_id)
                .options(
                    selectinload(SupportUserModel.answers),
                    selectinload(SupportUserModel.current_question),
                    selectinload(SupportUserModel.role),
                )
            )

            result = (await session.execute(q)).scalars().first()

            return result and result.as_support_user_entity()

    async def get_support_users_with_role_id(
        self, role_id: UUID
    ) -> list[SupportUser]:
        async with self._session() as session:
            q = (
                select(SupportUserModel)
                .where(SupportUserModel.role_id == role_id)
                .options(
                    selectinload(SupportUserModel.answers),
                    selectinload(SupportUserModel.current_question),
                    selectinload(SupportUserModel.role),
                )
            )

            result = (await session.execute(q)).scalars().all()

            return [elem.as_support_user_entity() for elem in result]

    async def get_all_support_users(self) -> list[SupportUser]:
        async with self._session() as session:
            q = select(SupportUserModel).options(
                selectinload(SupportUserModel.answers),
                selectinload(SupportUserModel.current_question),
                selectinload(SupportUserModel.role),
            )

            result = (await session.execute(q)).scalars().all()

            return [elem.as_support_user_entity() for elem in result]

    async def get_all_support_users_sorted_by_date(
        self, desc_order: bool = False
    ) -> list[SupportUser]:
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

            result = (await session.execute(q)).scalars().all()

            return [elem.as_support_user_entity() for elem in result]

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
    async def get_random_unbinded_question(self) -> Question:
        async with self._session() as session:

            q = select(QuestionModel).options(
                selectinload(QuestionModel.regular_user),
                selectinload(QuestionModel.current_support_user),
                selectinload(QuestionModel.answers),
            )

            result = (await session.execute(q)).scalars().first()

            return result and result.as_question_entity()

    async def get_all_questions(self) -> list[Question]:
        async with self._session() as session:

            q = select(QuestionModel).options(
                selectinload(QuestionModel.regular_user),
                selectinload(QuestionModel.current_support_user),
                selectinload(QuestionModel.answers),
            )

            result = (await session.execute(q)).scalars().all()

            return [elem.as_question_entity() for elem in result]

    async def get_question_by_id(self, question_id: UUID) -> Question:
        async with self._session() as session:

            q = (
                select(QuestionModel)
                .where(QuestionModel.id == question_id)
                .options(
                    selectinload(QuestionModel.regular_user),
                    selectinload(QuestionModel.current_support_user),
                    selectinload(QuestionModel.answers),
                )
            )

            result = (await session.execute(q)).scalars().first()

            return result and result.as_question_entity()

    async def get_question_by_tg_message_id(
        self, tg_message_id: int
    ) -> Question:
        async with self._session() as session:

            q = (
                select(QuestionModel)
                .where(QuestionModel.tg_message_id == tg_message_id)
                .options(
                    selectinload(QuestionModel.regular_user),
                    selectinload(QuestionModel.current_support_user),
                    selectinload(QuestionModel.answers),
                )
            )

            result = (await session.execute(q)).scalars().first()

            return result and result.as_question_entity()

    async def get_questions_with_regular_user_id(
        self, regular_user_id: UUID
    ) -> list[Question]:
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

            result = (await session.execute(q)).scalars().all()

            return [elem.as_question_entity() for elem in result]

    async def get_unbinded_questions(self) -> list[Question]:
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

            result = (await session.execute(q)).scalars().all()

            return [elem.as_question_entity() for elem in result]

    async def get_unanswered_questions(self) -> list[Question]:
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

            result = (await session.execute(q)).scalars().all()

            return [elem.as_question_entity() for elem in result]

    async def delete_question_with_id(self, question_id: UUID):
        async with self._session() as session:

            q = delete(QuestionModel).where(QuestionModel.id == question_id)

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

    async def add_question(self, question: Question):
        async with self._session() as session:
            question_model = QuestionModel(
                id=question.id,
                regular_user_id=question.regular_user_id,
                message=question.message,
                tg_message_id=question.tg_message_id,
                date=question.date,
            )

            session.add(question_model)

            await session.commit()

    async def count_all_questions(self) -> int:
        async with self._session() as session:

            q = select(func.count(QuestionModel.id))

            return (await session.execute(q)).scalar()

    async def count_unanswered_questions(self) -> int:
        async with self._session() as session:

            q = select(func.count(QuestionModel.id)).where(
                QuestionModel.answers == None
            )

            return (await session.execute(q)).scalar()

    async def count_answered_questions(self) -> int:
        async with self._session() as session:
            q = select(func.count(QuestionModel.id)).where(
                QuestionModel.answers != None
            )

            return (await session.execute(q)).scalar()

    # Answers Methods
    async def get_all_answers(self) -> list[Answer]:
        async with self._session() as session:
            q = select(AnswerModel).options(
                selectinload(AnswerModel.support_user),
                selectinload(AnswerModel.question),
            )

            result = (await session.execute(q)).scalars().all()

            return [elem.as_answer_entity() for elem in result]

    async def get_answer_by_id(self, answer_id: UUID) -> Answer:
        async with self._session() as session:

            q = (
                select(AnswerModel)
                .where(AnswerModel.id == answer_id)
                .options(
                    selectinload(AnswerModel.support_user),
                    selectinload(AnswerModel.question),
                )
            )

            result = (await session.execute(q)).scalars().first()

            return result and result.as_answer_entity()

    async def get_support_user_answers_with_id(
        self, support_user_id: UUID
    ) -> list[Answer]:
        async with self._session() as session:
            q = (
                select(AnswerModel)
                .where(AnswerModel.support_user_id == support_user_id)
                .options(
                    selectinload(AnswerModel.support_user),
                    selectinload(AnswerModel.question),
                )
            )

            result = (await session.execute(q)).scalars().all()

            return [elem.as_answer_entity() for elem in result]

    async def get_answers_with_question_id(
        self, question_id: UUID
    ) -> list[Answer]:
        async with self._session() as session:

            q = (
                select(AnswerModel)
                .where(AnswerModel.question_id == question_id)
                .options(
                    selectinload(AnswerModel.support_user),
                    selectinload(AnswerModel.question),
                )
            )

            result = (await session.execute(q)).scalars().all()

            return [elem.as_answer_entity() for elem in result]

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

    async def add_answer(
        self,
        answer: Answer,
    ) -> None:
        async with self._session() as session:
            answer_model = AnswerModel(
                id=answer.id,
                support_user_id=answer.support_user_id,
                question_id=answer.question_id,
                message=answer.message,
                tg_message_id=answer.tg_message_id,
                date=answer.date,
            )

            session.add(answer_model)

            await session.commit()

    async def count_all_answers(self) -> int:
        async with self._session() as session:

            q = select(func.count(AnswerModel.id))

            return (await session.execute(q)).scalar()
