from uuid import UUID
from sqlalchemy import delete, func, Select
from sqlalchemy.orm import selectinload
from sqlalchemy.future import select
from bot.entities.answer import Answer
from bot.entities.answer_attachment import AnswerAttachment
from bot.entities.question import Question
from bot.entities.question_attachment import QuestionAttachment
from bot.entities.regular_user import RegularUser
from bot.entities.role import Role
from bot.entities.support_user import SupportUser
from bot.db.db_sa_settings import async_session
from bot.db.models.sa_models import (
    QuestionModel,
    QuestionAttachmentModel,
    AnswerModel,
    AnswerAttachmentModel,
    RegularUserModel,
    SupportUserModel,
    RoleModel,
)
from bot.db.repositories.repository import Repo


class SARepo(Repo):
    def __init__(self) -> None:
        self._session = async_session

    # ROLES METHODS

    async def add_role(self, role: Role) -> Role:
        async with self._session() as session:  # type: ignore
            role_model = (
                RoleModel(
                    id=role.id,
                    name=role.name,
                    description=role.description,
                    can_answer_questions=role.can_answer_questions,
                    can_manage_support_users=role.can_manage_support_users,
                    created_date=role.created_date,
                )
                # If role.id equals to zero.
                # It means that a new id will be created on the DB's side
                if role.id
                else RoleModel(
                    name=role.name,
                    description=role.description,
                    can_answer_questions=role.can_answer_questions,
                    can_manage_support_users=role.can_manage_support_users,
                    created_date=role.created_date,
                )
            )

            session.add(role_model)

            await session.commit()

            role.id = role_model.id  # type: ignore

            return role

    async def change_support_user_role(
        self, support_user_id: UUID, new_role_id: int
    ) -> None:
        async with self._session() as session:  # type: ignore
            q = select(SupportUserModel).where(
                SupportUserModel.id == support_user_id
            )

            support_user = (await session.execute(q)).scalars().first()

            role_q = select(RoleModel).where(RoleModel.id == new_role_id)

            role = (await session.execute(role_q)).scalars().first()

            support_user.role = role

            session.commit()

    async def get_role_by_id(self, id: int) -> Role | None:
        async with self._session() as session:  # type: ignore
            q = self._get_role_query_with_options(
                select(RoleModel).where(RoleModel.id == id)
            )

            result = (await session.execute(q)).scalars().first()

            return result and result.as_role_entity()

    async def get_role_by_name(self, name: str) -> Role | None:
        async with self._session() as session:  # type: ignore
            q = self._get_role_query_with_options(
                select(RoleModel).where(RoleModel.name == name)
            )

            result = (await session.execute(q)).scalars().first()

            return result and result.as_role_entity()

    async def get_all_roles(self) -> list[Role]:
        async with self._session() as session:  # type: ignore
            q = select(RoleModel).options(selectinload(RoleModel.users))

            result = (await session.execute(q)).scalars().all()

            return [elem.as_role_entity() for elem in result]

    async def get_all_roles_sorted_by_date(
        self, desc_order: bool = False
    ) -> list[Role]:
        async with self._session() as session:  # type: ignore
            q = self._get_role_query_with_options(
                select(RoleModel).order_by(
                    RoleModel.created_date.desc()
                    if desc_order
                    else RoleModel.created_date.asc()
                )
            )

            result = (await session.execute(q)).scalars().all()

            return [elem.as_role_entity() for elem in result]

    async def delete_role_with_id(self, id: int) -> None:
        async with self._session() as session:  # type: ignore
            q = delete(RoleModel).where(RoleModel.id == id)

            await session.execute(q)

            await session.commit()

    async def delete_all_roles(self) -> None:
        async with self._session() as session:  # type: ignore
            q = delete(RoleModel)

            await session.execute(q)

            await session.commit()

    async def count_all_roles(self) -> int:
        async with self._session() as session:  # type: ignore

            q = select(func.count(QuestionModel.id))

            return (await session.execute(q)).scalar()

    def _get_role_query_with_options(self, q: Select):
        return q.options(selectinload(RoleModel.users))

    # REGULAR USERS METHODS

    async def add_regular_user(self, regular_user: RegularUser) -> RegularUser:
        async with self._session() as session:  # type: ignore
            regular_user_model = RegularUserModel(
                id=regular_user.id,
                tg_bot_user_id=regular_user.tg_bot_user_id,
                join_date=regular_user.join_date,
            )

            session.add(regular_user_model)

            await session.commit()

            return regular_user

    async def get_regular_user_by_id(self, id: UUID) -> RegularUser | None:
        async with self._session() as session:  # type: ignore
            q = self._get_regular_user_query_with_options(
                select(RegularUserModel).where(RegularUserModel.id == id)
            )

            result = (await session.execute(q)).scalars().first()

            return result and result.as_regular_user_entity()

    async def get_regular_user_by_tg_bot_user_id(
        self, tg_bot_user_id: int
    ) -> RegularUser | None:
        async with self._session() as session:  # type: ignore
            q = self._get_regular_user_query_with_options(
                select(RegularUserModel).where(
                    RegularUserModel.tg_bot_user_id == tg_bot_user_id
                )
            )

            result = (await session.execute(q)).scalars().first()

            return result and result.as_regular_user_entity()

    async def get_all_regular_users(self) -> list[RegularUser]:
        async with self._session() as session:  # type: ignore
            q = self._get_regular_user_query_with_options(
                select(RegularUserModel)
            )

            result = (await session.execute(q)).scalars().all()

            return [elem.as_regular_user_entity() for elem in result]

    async def get_all_regular_users_sorted_by_date(
        self, desc_order: bool = False
    ) -> list[RegularUser]:
        async with self._session() as session:  # type: ignore
            q = self._get_regular_user_query_with_options(
                select(RegularUserModel).order_by(
                    RegularUserModel.join_date.desc()
                    if desc_order
                    else RegularUserModel.join_date.asc()
                )
            )

            result = (await session.execute(q)).scalars().all()

            return [elem.as_regular_user_entity() for elem in result]

    async def delete_regular_user_with_id(self, id: UUID) -> None:
        async with self._session() as session:  # type: ignore
            q = delete(RegularUserModel).where(RegularUserModel.id == id)

            await session.execute(q)

            await session.commit()

    async def delete_all_regular_users(self) -> None:
        async with self._session() as session:  # type: ignore
            q = delete(RegularUserModel)

            await session.execute(q)

            await session.commit()

    async def count_all_regular_users(self) -> int:
        async with self._session() as session:  # type: ignore

            q = select(func.count(QuestionModel.id))

            return (await session.execute(q)).scalar()

    def _get_regular_user_query_with_options(self, q: Select):
        return q.options(selectinload(RegularUserModel.questions))

    # SUPPORT USERS METHODS

    async def add_support_user(self, support_user: SupportUser) -> SupportUser:
        async with self._session() as session:  # type: ignore

            support_user_model = SupportUserModel(
                id=support_user.id,
                current_question_id=(
                    support_user.current_question
                    and support_user.current_question.id
                ),
                role_id=(support_user.role and support_user.role.id),
                descriptive_name=support_user.descriptive_name,
                tg_bot_user_id=support_user.tg_bot_user_id,
                join_date=support_user.join_date,
                is_owner=support_user.is_owner,
            )

            session.add(support_user_model)

            await session.commit()

            return support_user

    async def bind_question_to_support_user(
        self, support_user_id: UUID, question_id: UUID
    ) -> None:
        async with self._session() as session:  # type: ignore
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
        async with self._session() as session:  # type: ignore
            q = select(SupportUserModel).where(
                SupportUserModel.id == support_user_id
            )

            support_user: SupportUserModel = (
                (await session.execute(q)).scalars().first()
            )

            support_user.current_question = None  # type: ignore

            await session.commit()

    async def deactivate_support_user(self, support_user_id: UUID) -> None:
        async with self._session() as session:  # type: ignore
            q = select(SupportUserModel).where(
                SupportUserModel.id == support_user_id
            )

            support_user: SupportUserModel = (
                (await session.execute(q)).scalars().first()
            )

            support_user.is_active = False  # type: ignore

            await session.commit()

    async def activate_support_user(self, support_user_id: UUID) -> None:
        async with self._session() as session:  # type: ignore
            q = select(SupportUserModel).where(
                SupportUserModel.id == support_user_id
            )

            support_user: SupportUserModel = (
                (await session.execute(q)).scalars().first()
            )

            support_user.is_active = True  # type: ignore

            await session.commit()

    async def make_support_user_owner(self, support_user_id: UUID) -> None:
        async with self._session() as session:  # type: ignore
            q = select(SupportUserModel).where(
                SupportUserModel.id == support_user_id
            )

            support_user: SupportUserModel = (
                (await session.execute(q)).scalars().first()
            )

            support_user.is_owner = True  # type: ignore

            await session.commit()

    async def remove_owner_rights_from_support_user(
        self, support_user_id: UUID
    ) -> None:
        async with self._session() as session:  # type: ignore
            q = select(SupportUserModel).where(
                SupportUserModel.id == support_user_id
            )

            support_user: SupportUserModel = (
                (await session.execute(q)).scalars().first()
            )

            support_user.is_owner = False  # type: ignore

            await session.commit()

    async def get_support_user_by_id(self, id: UUID) -> SupportUser | None:
        async with self._session() as session:  # type: ignore
            q = self._get_support_user_query_with_options(
                select(SupportUserModel).where(SupportUserModel.id == id)
            )

            result = (await session.execute(q)).scalars().first()

            return result and result.as_support_user_entity()

    async def get_support_user_by_tg_bot_user_id(
        self, tg_bot_user_id: int
    ) -> SupportUser | None:
        async with self._session() as session:  # type: ignore
            q = self._get_support_user_query_with_options(
                select(SupportUserModel).where(
                    SupportUserModel.tg_bot_user_id == tg_bot_user_id
                )
            )

            result = (await session.execute(q)).scalars().first()

            return result and result.as_support_user_entity()

    async def get_support_users_with_role_id(
        self, role_id: int
    ) -> list[SupportUser]:
        async with self._session() as session:  # type: ignore
            q = self._get_support_user_query_with_options(
                select(SupportUserModel).where(
                    SupportUserModel.role_id == role_id
                )
            )

            result = (await session.execute(q)).scalars().all()

            return [elem.as_support_user_entity() for elem in result]

    async def get_all_support_users(self) -> list[SupportUser]:
        async with self._session() as session:  # type: ignore
            q = self._get_support_user_query_with_options(
                select(SupportUserModel)
            )

            result = (await session.execute(q)).scalars().all()

            return [elem.as_support_user_entity() for elem in result]

    async def get_all_support_users_sorted_by_date(
        self, desc_order: bool = False
    ) -> list[SupportUser]:
        async with self._session() as session:  # type: ignore
            q = self._get_support_user_query_with_options(
                select(SupportUserModel).order_by(
                    SupportUserModel.join_date.desc()
                    if desc_order
                    else SupportUserModel.join_date.asc()
                )
            )

            result = (await session.execute(q)).scalars().all()

            return [elem.as_support_user_entity() for elem in result]

    async def delete_support_user_with_id(self, id: UUID) -> None:
        async with self._session() as session:  # type: ignore
            q = delete(SupportUserModel).where(SupportUserModel.id == id)

            await session.execute(q)

            await session.commit()

    async def delete_all_support_users(self) -> None:
        async with self._session() as session:  # type: ignore
            q = delete(SupportUserModel)

            await session.execute(q)

            await session.commit()

    async def count_all_support_users(self) -> int:
        async with self._session() as session:  # type: ignore

            q = select(func.count(QuestionModel.id))

            return (await session.execute(q)).scalar()

    def _get_support_user_query_with_options(self, q: Select):
        return q.options(
            selectinload(SupportUserModel.current_question).selectinload(
                QuestionModel.regular_user
            ),
            selectinload(SupportUserModel.current_question).selectinload(
                QuestionModel.current_support_user
            ),
            selectinload(SupportUserModel.current_question).selectinload(
                QuestionModel.question_attachments
            ),
            selectinload(SupportUserModel.role),
            selectinload(SupportUserModel.current_question).selectinload(
                QuestionModel.regular_user
            ),
        )

    # QUESTIONS METHODS

    async def add_question(self, question: Question) -> Question:
        async with self._session() as session:  # type: ignore
            question_model = QuestionModel(
                id=question.id,
                regular_user_id=question.regular_user.id
                if question.regular_user
                else None,
                message=question.message,
                tg_message_id=question.tg_message_id,
                date=question.date,
            )

            session.add(question_model)

            await session.commit()

            return question

    async def get_random_unbinded_question(self) -> Question | None:
        async with self._session() as session:  # type: ignore

            q = self._get_question_query_with_options(
                select(QuestionModel).where(
                    QuestionModel.current_support_user == None
                )
            )

            result = (await session.execute(q)).scalars().first()

            return result and result.as_question_entity()

    async def get_random_unanswered_unbinded_question(self) -> Question | None:
        async with self._session() as session:  # type: ignore

            q = self._get_question_query_with_options(
                select(QuestionModel)
                .where(QuestionModel.current_support_user == None)
                .where(QuestionModel.answers == None)
            )

            result = (await session.execute(q)).scalars().first()

            return result and result.as_question_entity()

    async def get_all_questions(self) -> list[Question]:
        async with self._session() as session:  # type: ignore

            q = self._get_question_query_with_options(select(QuestionModel))

            result = (await session.execute(q)).scalars().all()

            return [elem.as_question_entity() for elem in result]

    async def get_question_by_id(self, question_id: UUID) -> Question | None:
        async with self._session() as session:  # type: ignore

            q = self._get_question_query_with_options(
                select(QuestionModel).where(QuestionModel.id == question_id)
            )

            result = (await session.execute(q)).scalars().first()

            return result and result.as_question_entity()

    async def get_regular_user_last_asked_question(
        self, regular_user_id: UUID
    ) -> Question | None:
        async with self._session() as session:  # type: ignore
            q = self._get_question_query_with_options(
                select(QuestionModel)
                .where(QuestionModel.regular_user_id == regular_user_id)
                .order_by(QuestionModel.date.desc())
            )

            result = (await session.execute(q)).scalars().first()

            return result and result.as_question_entity()

    async def get_question_by_tg_message_id(
        self, tg_message_id: int
    ) -> Question | None:
        async with self._session() as session:  # type: ignore

            q = self._get_question_query_with_options(
                select(QuestionModel).where(
                    QuestionModel.tg_message_id == tg_message_id
                )
            )

            result = (await session.execute(q)).scalars().first()

            return result and result.as_question_entity()

    async def get_questions_with_regular_user_id(
        self, regular_user_id: UUID
    ) -> list[Question]:
        async with self._session() as session:  # type: ignore

            q = self._get_question_query_with_options(
                select(QuestionModel).where(
                    QuestionModel.regular_user_id == regular_user_id
                )
            )

            result = (await session.execute(q)).scalars().all()

            return [elem.as_question_entity() for elem in result]

    async def get_unbinded_questions(self) -> list[Question]:
        async with self._session() as session:  # type: ignore

            q = self._get_question_query_with_options(
                select(QuestionModel).where(
                    QuestionModel.current_support_user == None
                )
            )

            result = (await session.execute(q)).scalars().all()

            return [elem.as_question_entity() for elem in result]

    async def get_unanswered_questions(self) -> list[Question]:
        async with self._session() as session:  # type: ignore

            q = self._get_question_query_with_options(
                select(QuestionModel).where(
                    QuestionModel.current_support_user == None
                    and QuestionModel.answers == []
                )
            )

            result = (await session.execute(q)).scalars().all()

            return [elem.as_question_entity() for elem in result]

    async def delete_question_with_id(self, question_id: UUID):
        async with self._session() as session:  # type: ignore

            q = delete(QuestionModel).where(QuestionModel.id == question_id)

            await session.execute(q)

            await session.commit()

    async def delete_questions_with_regular_user_id(
        self, reguar_user_id: UUID
    ):
        async with self._session() as session:  # type: ignore

            q = delete(QuestionModel).where(QuestionModel.id == reguar_user_id)

            await session.execute(q)

            await session.commit()

    async def delete_all_questions(self):
        async with self._session() as session:  # type: ignore

            q = delete(QuestionModel)

            await session.execute(q)

            await session.commit()

    async def count_all_questions(self) -> int:
        async with self._session() as session:  # type: ignore

            q = select(func.count(QuestionModel.id))

            return (await session.execute(q)).scalar()

    async def count_unanswered_questions(self) -> int:
        async with self._session() as session:  # type: ignore

            q = select(func.count(QuestionModel.id)).where(
                QuestionModel.answers == None
            )

            return (await session.execute(q)).scalar()

    async def count_answered_questions(self) -> int:
        async with self._session() as session:  # type: ignore
            q = select(func.count(QuestionModel.id)).where(
                QuestionModel.answers != None
            )

            return (await session.execute(q)).scalar()

    def _get_question_query_with_options(self, q: Select):
        return q.options(
            selectinload(QuestionModel.regular_user),
            selectinload(QuestionModel.current_support_user),
            selectinload(QuestionModel.question_attachments),
        )

    # ANSWERS METHODS

    async def add_answer(
        self,
        answer: Answer,
    ) -> Answer:
        async with self._session() as session:  # type: ignore
            answer_model = AnswerModel(
                id=answer.id,
                support_user_id=answer.support_user.id
                if answer.support_user
                else None,
                question_id=answer.question.id if answer.question else None,
                message=answer.message,
                tg_message_id=answer.tg_message_id,
                date=answer.date,
            )

            session.add(answer_model)

            await session.commit()

            return answer

    async def estimate_answer_as_useful(self, answer_id: UUID) -> None:
        async with self._session() as session:  # type: ignore
            q = (
                select(AnswerModel)
                .where(AnswerModel.id == answer_id)
                .options(selectinload(AnswerModel.support_user))
            )

            answer = (await session.execute(q)).scalars().first()

            answer.is_useful = True

            await session.commit()

    async def estimate_answer_as_unuseful(self, answer_id: UUID) -> None:
        async with self._session() as session:  # type: ignore
            q = (
                select(AnswerModel)
                .where(AnswerModel.id == answer_id)
                .options(selectinload(AnswerModel.support_user))
            )

            answer = (await session.execute(q)).scalars().first()

            answer.is_useful = False

            await session.commit()

    async def get_all_answers(self) -> list[Answer]:
        async with self._session() as session:  # type: ignore
            q = self._get_answer_query_with_options(select(AnswerModel))

            result = (await session.execute(q)).scalars().all()

            return [elem.as_answer_entity() for elem in result]

    async def get_answer_by_id(self, answer_id: UUID) -> Answer | None:
        async with self._session() as session:  # type: ignore

            q = self._get_answer_query_with_options(
                select(AnswerModel).where(AnswerModel.id == answer_id)
            )

            result = (await session.execute(q)).scalars().first()

            return result and result.as_answer_entity()

    async def get_support_user_last_answer(
        self, support_user_id: UUID
    ) -> Answer | None:
        async with self._session() as session:  # type: ignore
            q = self._get_answer_query_with_options(
                select(AnswerModel)
                .where(AnswerModel.support_user_id == support_user_id)
                .order_by(AnswerModel.date.desc())
            )

            result = (await session.execute(q)).scalars().first()

            return result and result.as_question_entity()

    async def get_support_user_answers_with_id(
        self, support_user_id: UUID
    ) -> list[Answer]:
        async with self._session() as session:  # type: ignore
            q = self._get_answer_query_with_options(
                select(AnswerModel).where(
                    AnswerModel.support_user_id == support_user_id
                )
            )

            result = (await session.execute(q)).scalars().all()

            return [elem.as_answer_entity() for elem in result]

    async def get_answers_with_question_id(
        self, question_id: UUID
    ) -> list[Answer]:
        async with self._session() as session:  # type: ignore

            q = self._get_answer_query_with_options(
                select(AnswerModel).where(
                    AnswerModel.question_id == question_id
                )
            )

            result = (await session.execute(q)).scalars().all()

            return [elem.as_answer_entity() for elem in result]

    async def get_answer_by_tg_message_id(
        self, tg_mesage_id: int
    ) -> Answer | None:
        async with self._session() as session:  # type: ignore
            q = self._get_answer_query_with_options(
                select(AnswerModel).where(
                    AnswerModel.tg_message_id == tg_mesage_id
                )
            )

            result = (await session.execute(q)).scalars().first()

            return result and result.as_answer_entity()

    async def delete_answer_with_id(self, answer_id: UUID) -> None:
        async with self._session() as session:  # type: ignore

            q = delete(AnswerModel).where(AnswerModel.id == answer_id)

            await session.execute(q)

            await session.commit()

    async def delete_all_answers(self) -> None:
        async with self._session() as session:  # type: ignore

            q = delete(AnswerModel)

            await session.execute(q)

            await session.commit()

    async def delete_support_user_answers_with_id(
        self, support_user_id: UUID
    ) -> None:
        async with self._session() as session:  # type: ignore

            q = delete(AnswerModel).where(
                AnswerModel.support_user_id == support_user_id
            )

            await session.execute(q)

            await session.commit()

    async def delete_answers_with_question_id(self, question_id: UUID) -> None:
        async with self._session() as session:  # type: ignore

            q = delete(AnswerModel).where(
                AnswerModel.question_id == question_id
            )

            await session.execute(q)

            await session.commit()

    async def count_all_answers(self) -> int:
        async with self._session() as session:  # type: ignore

            q = select(func.count(AnswerModel.id))

            return (await session.execute(q)).scalar()

    def _get_answer_query_with_options(self, q: Select):
        return q.options(
            selectinload(AnswerModel.question).selectinload(
                QuestionModel.regular_user
            ),
            selectinload(AnswerModel.question).selectinload(
                QuestionModel.question_attachments
            ),
            # SUPPORT USER AND ITS CURRENT QUESTIONS PROPERTIES
            selectinload(AnswerModel.support_user)
            .selectinload(SupportUserModel.current_question)
            .selectinload(QuestionModel.regular_user),
            selectinload(AnswerModel.support_user)
            .selectinload(SupportUserModel.current_question)
            .selectinload(QuestionModel.question_attachments),
            # SUPPORT USER ROLE
            selectinload(AnswerModel.support_user).selectinload(
                SupportUserModel.role
            ),
        )

    # QUESTION ATTACHMENTS METHODS
    async def add_question_attachment(
        self, question_attachment: QuestionAttachment
    ) -> QuestionAttachment:
        async with self._session() as session:  # type: ignore
            question_attachment_model = QuestionAttachmentModel(
                id=question_attachment.id,
                question_id=question_attachment.question_id,
                tg_file_id=question_attachment.tg_file_id,
                attachment_type=question_attachment.attachment_type,
                date=question_attachment.date,
            )

            session.add(question_attachment_model)

            await session.commit()

            return question_attachment

    async def get_question_attachment_by_id(
        self, id: UUID
    ) -> QuestionAttachment:
        async with self._session() as session:  # type: ignore
            q = self._get_question_attachment_query_with_options(
                select(QuestionAttachmentModel).where(
                    QuestionAttachmentModel.id == id
                )
            )

            result = (await session.execute(q)).scalars().first()

            return result and result.as_question_attachment_entity()

    async def get_question_attachments(
        self, question_id: UUID
    ) -> list[QuestionAttachment]:
        async with self._session() as session:  # type: ignore
            q = self._get_question_attachment_query_with_options(
                select(QuestionAttachmentModel).where(
                    QuestionAttachmentModel.question_id == question_id
                )
            )

            result = (await session.execute(q)).scalars().all()

            return [elem.as_question_attachment_entity() for elem in result]

    async def get_all_questions_attachments(self) -> list[QuestionAttachment]:
        async with self._session() as session:  # type: ignore
            q = self._get_question_attachment_query_with_options(
                select(QuestionAttachmentModel)
            )

            result = (await session.execute(q)).scalars().first()

            return [elem.as_question_attachment_entity() for elem in result]

    async def delete_question_attachment_with_id(
        self, answer_attachment_id: UUID
    ) -> None:
        async with self._session() as session:  # type: ignore

            q = delete(QuestionAttachmentModel).where(
                QuestionAttachmentModel.id == answer_attachment_id
            )

            await session.execute(q)

            await session.commit()

    async def delete_question_attachment_with_question_id(
        self, question_id: UUID
    ) -> None:
        async with self._session() as session:  # type: ignore

            q = delete(QuestionAttachmentModel).where(
                QuestionAttachmentModel.question_id == question_id
            )

            await session.execute(q)

            await session.commit()

    async def delete_all_questions_attachments(self) -> None:
        async with self._session() as session:  # type: ignore

            q = delete(QuestionAttachmentModel)

            await session.execute(q)

            await session.commit()

    def _get_question_attachment_query_with_options(self, q: Select):
        return q.options(selectinload(QuestionAttachmentModel.question))

    # ANSWERS ATTACHMENTS METHODS

    async def add_answer_attachment(
        self, answer_attachment: AnswerAttachment
    ) -> AnswerAttachment:
        async with self._session() as session:  # type: ignore
            answer_attachment_model = AnswerAttachmentModel(
                id=answer_attachment.id,
                answer_id=answer_attachment.answer_id,
                tg_file_id=answer_attachment.tg_file_id,
                attachment_type=answer_attachment.attachment_type,
                date=answer_attachment.date,
            )

            session.add(answer_attachment_model)

            await session.commit()

            return answer_attachment

    async def get_answer_attachment_by_id(self, id: UUID) -> AnswerAttachment:
        async with self._session() as session:  # type: ignore
            q = self._get_answer_attachment_query_with_options(
                select(AnswerAttachmentModel)
                .where(AnswerAttachmentModel.id == id)
                .options(selectinload(AnswerAttachmentModel.answer))
            )

            result = (await session.execute(q)).scalars().first()

            return result and result.as_answer_attachment_entity()

    async def get_answer_attachments(
        self, answer_id: UUID
    ) -> list[AnswerAttachment]:
        async with self._session() as session:  # type: ignore
            q = self._get_answer_attachment_query_with_options(
                select(AnswerAttachmentModel)
                .where(AnswerAttachmentModel.answer_id == answer_id)
                .options(selectinload(AnswerAttachmentModel.answer))
            )

            result = (await session.execute(q)).scalars().first()

            return result and result.as_answer_attachment_entity()

    async def get_all_answers_attachments(self) -> list[AnswerAttachment]:
        async with self._session() as session:  # type: ignore
            q = self._get_answer_attachment_query_with_options(
                select(AnswerAttachmentModel).options(
                    selectinload(AnswerAttachmentModel.answer)
                )
            )

            result = (await session.execute(q)).scalars().first()

            return result and result.as_answer_attachment_entity()

    async def delete_answer_attachment_with_id(
        self, answer_attachment_id: UUID
    ) -> None:
        async with self._session() as session:  # type: ignore

            q = delete(AnswerAttachmentModel).where(
                AnswerAttachmentModel.id == answer_attachment_id
            )

            await session.execute(q)

            await session.commit()

    async def delete_answer_attachment_with_answer_id(
        self, answer_id: UUID
    ) -> None:
        async with self._session() as session:  # type: ignore

            q = delete(AnswerAttachmentModel).where(
                AnswerAttachmentModel.answer_id == answer_id
            )

            await session.execute(q)

            await session.commit()

    async def delete_all_answer_attachments(self) -> None:
        async with self._session() as session:  # type: ignore

            q = delete(AnswerAttachmentModel)

            await session.execute(q)

            await session.commit()

    def _get_answer_attachment_query_with_options(self, q: Select):
        return q.options(selectinload(QuestionAttachmentModel.question))
