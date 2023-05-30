from __future__ import annotations
from uuid import UUID
from sqlalchemy import delete, func, Select, select, and_
from sqlalchemy.orm import selectinload
from app.entities.answer import Answer
from app.entities.question import Question
from app.entities.regular_user import RegularUser
from app.entities.role import Role
from app.entities.support_user import SupportUser
from app.infra.models.sa_models import (
    QuestionModel,
    AnswerModel,
    AnswerAttachmentModel,
    RegularUserModel,
    SupportUserModel,
    RoleModel,
)
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Callable
from app.infra.repos.abc_repos import (
    AnswersRepo,
    QuestionsRepo,
    RegularUsersRepo,
    Repo,
    RepoConfig,
    SupportUsersRepo,
)


class SARepoConfig(RepoConfig):
    connection_provider: Callable[..., AsyncSession]

    def __init__(self, connection_povider: Callable[..., AsyncSession]):
        self.connection_provider = connection_povider


class RolesRepo(abc.ABC):
    def __init__(self, repo_config: RepoConfig) -> None:
        self._session = repo_config.connection_provider

    async def add(self, role: Role) -> Role:
        async with self._session() as session:
            role_model = RoleModel(role)

            session.add(role_model)

            await session.commit()

            role.id = role_model.id  # type: ignore

            return role

    async def update(self, role: Role) -> Role:
        async with self._session() as session:
            role_model = RoleModel.from_entity(role)

            await session.merge(role_model)

            await session.commit()

            return role

    async def get_by_id(self, id: int) -> Role | None:
        async with self._session() as session:
            q = self._get_role_query_with_options(
                select(RoleModel).where(RoleModel.id == id)
            )

            result = (await session.execute(q)).scalars().first()

            return result and result.as_role_entity()

    async def get_by_name(self, name: str) -> Role | None:
        async with self._session() as session:
            q = self._get_role_query_with_options(
                select(RoleModel).where(RoleModel.name == name)
            )

            result = (await session.execute(q)).scalars().first()

            return result and result.as_role_entity()

    async def get_all(self) -> list[Role]:
        async with self._session() as session:
            q = select(RoleModel).options(selectinload(RoleModel.users))

            result = (await session.execute(q)).scalars().all()

            return [elem.as_role_entity() for elem in result]

    async def delete(self, role_id: int) -> None:
        async with self._session() as session:
            q = delete(RoleModel).where(RoleModel.id == id)

            await session.execute(q)

            await session.commit()

    async def delete_all(self) -> None:
        async with self._session() as session:
            q = delete(RoleModel)

            await session.execute(q)

            await session.commit()

    async def count_all(self) -> int:
        async with self._session() as session:
            q = select(func.count(RoleModel.id))

            return (await session.execute(q)).scalar()

    def _get_role_query_with_options(self, q: Select):
        return q.options(selectinload(RoleModel.users))


class SASupportUsersRepo(SupportUsersRepo):
    def __init__(self, repo_config: RepoConfig) -> None:
        self._session = repo_config.connection_provider

    async def add(self, support_user: SupportUser) -> SupportUser:
        async with self._session() as session:
            support_user_model = SupportUserModel.from_entity(
                support_user_entity=support_user
            )

            session.add(support_user_model)

            await session.commit()

            return support_user

    async def update(self, support_user: SupportUser) -> SupportUser:
        async with self._session() as session:
            support_user_model = SupportUserModel.from_entity(
                support_user_entity=support_user
            )

            await session.merge(support_user_model)

            await session.commit()

            return support_user

    async def get_by_id(self, id: UUID) -> SupportUser | None:
        async with self._session() as session:
            q = self._get_support_user_query_with_options(
                select(SupportUserModel).where(SupportUserModel.id == id)
            )

            result = (await session.execute(q)).scalars().first()

            return result and result.as_support_user_entity()

    async def get_by_tg_bot_user_id(
        self, tg_bot_user_id: int
    ) -> SupportUser | None:
        async with self._session() as session:
            q = self._get_support_user_query_with_options(
                select(SupportUserModel).where(
                    SupportUserModel.tg_bot_user_id == tg_bot_user_id
                )
            )

            result = (await session.execute(q)).scalars().first()

            return result and result.as_support_user_entity()

    async def get_owner(self) -> SupportUser | None:
        async with self._session() as session:
            q = self._get_support_user_query_with_options(
                select(SupportUserModel).where(
                    SupportUserModel.is_owner == True  # noqa: E712
                )
            )

            result = (await session.execute(q)).scalars().first()

            return result and result.as_support_user_entity()

    async def get_by_role_id(self, role_id: int) -> list[SupportUser]:
        async with self._session() as session:
            q = self._get_support_user_query_with_options(
                select(SupportUserModel).where(
                    SupportUserModel.role_id == role_id
                )
            )

            result = (await session.execute(q)).scalars().all()

            return [elem.as_support_user_entity() for elem in result]

    async def get_all(self) -> list[SupportUser]:
        async with self._session() as session:
            q = self._get_support_user_query_with_options(
                select(SupportUserModel)
            )

            result = (await session.execute(q)).scalars().all()

            return [elem.as_support_user_entity() for elem in result]

    async def delete(self, support_user_id: UUID) -> None:
        async with self._session() as session:
            q = self._get_support_user_query_with_options(
                select(SupportUserModel).where(
                    SupportUserModel.id == support_user_id
                )
            )

            result = (await session.execute(q)).scallar()

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

            return (await session.execute(q)).scalar()

    async def count_by_role_id(self, role_id: int) -> int:
        async with self._session() as session:
            q = select(func.count(SupportUserModel.id)).where(
                SupportUserModel.role_id == role_id
            )

            return (await session.execute(q)).scalar()

    async def count_activated(self) -> int:
        async with self._session() as session:
            q = select(func.count(SupportUserModel.id)).where(
                SupportUserModel.is_active == True  # noqa: E712
            )

            return (await session.execute(q)).scalar()

    async def count_deactivated(self) -> int:
        async with self._session() as session:
            q = select(func.count(SupportUserModel.id)).where(
                SupportUserModel.is_active == False  # noqa: E712
            )

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


class SARegularUsersRepo(RegularUsersRepo):
    def __init__(self, repo_config: RepoConfig) -> None:
        self._session = repo_config.connection_provider

    async def add(self, regular_user: RegularUser) -> RegularUser:
        async with self._session() as session:
            regular_user_model = RegularUserModel.from_entity(regular_user)

            session.add(regular_user_model)

            await session.commit()

            return regular_user

    async def update(self, regular_user: RegularUser) -> RegularUser:
        async with self._session() as session:
            regular_user_model = RegularUserModel.from_entity(regular_user)

            await session.merge(regular_user_model)

            await session.commit()

            return regular_user

    async def get_by_id(self, id: UUID) -> RegularUser | None:
        async with self._session() as session:
            q = self._get_regular_user_query_with_options(
                select(RegularUserModel).where(RegularUserModel.id == id)
            )

            result = (await session.execute(q)).scalar()

            return result and result.as_regular_user_entity()

    async def get_by_tg_bot_user_id(
        self, tg_bot_user_id: int
    ) -> RegularUser | None:
        async with self._session() as session:
            q = self._get_regular_user_query_with_options(
                select(RegularUserModel).where(
                    RegularUserModel.tg_bot_user_id == tg_bot_user_id
                )
            )

            await session.execute(q)

            await session.commit()

    async def get_all(self) -> list[RegularUser]:
        async with self._session() as session:
            q = self._get_regular_user_query_with_options(
                select(RegularUserModel)
            )

            result = (await session.execute(q)).scalars().all()

            return [elem.as_regular_user_entity() for elem in result]

    async def delete(self, regular_user_id: UUID) -> None:
        async with self._session() as session:
            q = self._get_regular_user_query_with_options(
                select(RegularUserModel).where(
                    RegularUserModel.id == regular_user_id
                )
            )

            result = (await session.execute(q)).scallar()

            await session.delete(result)

            await session.commit()

    async def delete_all(self) -> None:
        async with self._session() as session:
            q = delete(RegularUserModel)

            await session.execute(q)

            await session.commit()

    async def count_all(self) -> int:
        async with self._session() as session:
            q = select(func.count(RegularUserModel.id))

            return (await session.execute(q)).scalar()

    def _get_regular_user_query_with_options(self, q: Select):
        return q.options(selectinload(RegularUserModel.questions))


class SAQuestionsRepo(QuestionsRepo):
    def __init__(self, repo_config: RepoConfig) -> None:
        self._session = repo_config.connection_provider

    async def add(self, question: Question) -> Question:
        async with self._session() as session:
            question_model = QuestionModel.from_entity(question)

            session.add(question_model)

            await session.commit()

            return question

    async def update(self, question: Question) -> Question:
        async with self._session() as session:
            question_model = QuestionModel.from_entity(question)

            await session.merge(question_model)

            await session.commit()

            return question_model

    async def get_random_unbinded(self) -> Question | None:
        async with self._session() as session:
            q = self._get_question_query_with_options(
                select(QuestionModel).where(
                    QuestionModel.current_support_user == None
                )
            )

            result = (await session.execute(q)).scalars().first()

            return result and result.as_question_entity()

    async def get_random_unanswered_unbinded(self) -> Question | None:
        async with self._session() as session:
            q = self._get_question_query_with_options(
                select(QuestionModel)
                .where(QuestionModel.current_support_user == None)
                .where(QuestionModel.answers == None)
            )

            result = (await session.execute(q)).scalars().first()

            return result and result.as_question_entity()

    async def get_all(self) -> list[Question]:
        async with self._session() as session:
            q = self._get_question_query_with_options(select(QuestionModel))

            result = (await session.execute(q)).scalars().all()

            return [elem.as_question_entity() for elem in result]

    async def get_by_id(self, question_id: UUID) -> Question | None:
        async with self._session() as session:
            q = self._get_question_query_with_options(
                select(QuestionModel).where(QuestionModel.id == question_id)
            )

            result = (await session.execute(q)).scalars().first()

            return result and result.as_question_entity()

    async def get_last_asked(self, regular_user_id: UUID) -> Question | None:
        async with self._session() as session:
            q = self._get_question_query_with_options(
                select(QuestionModel)
                .where(QuestionModel.regular_user_id == regular_user_id)
                .order_by(QuestionModel.date.desc())
            )

            result = (await session.execute(q)).scalars().first()

            return result and result.as_question_entity()

    async def get_by_tg_message_id(
        self, tg_message_id: int
    ) -> Question | None:
        async with self._session() as session:
            q = self._get_question_query_with_options(
                select(QuestionModel).where(
                    QuestionModel.tg_message_id == tg_message_id
                )
            )

            result = (await session.execute(q)).scalars().first()

            return result and result.as_question_entity()

    async def get_by_regular_user_id(
        self, regular_user_id: UUID
    ) -> list[Question]:
        async with self._session() as session:
            q = self._get_question_query_with_options(
                select(QuestionModel).where(
                    QuestionModel.regular_user_id == regular_user_id
                )
            )

            result = (await session.execute(q)).scalars().all()

            return [elem.as_question_entity() for elem in result]

    async def get_unbinded(self) -> list[Question]:
        async with self._session() as session:
            q = self._get_question_query_with_options(
                select(QuestionModel).where(
                    QuestionModel.current_support_user == None
                )
            )

            result = (await session.execute(q)).scalars().all()

            return [elem.as_question_entity() for elem in result]

    async def get_unanswered(self) -> list[Question]:
        async with self._session() as session:
            q = self._get_question_query_with_options(
                select(QuestionModel).where(
                    QuestionModel.current_support_user == None
                    and QuestionModel.answers == []
                )
            )

            result = (await session.execute(q)).scalars().all()

            return [elem.as_question_entity() for elem in result]

    async def delete(self, question_id: UUID) -> None:
        async with self._session() as session:
            q = self._get_question_query_with_options(
                select(QuestionModel).where(QuestionModel.id == question_id)
            )

            result = (await session.execute(q)).scallar()

            await session.delete(result)

            await session.commit()

    async def delete_by_regular_user_id(self, regular_user_id: UUID) -> None:
        async with self._session() as session:
            q = delete(QuestionModel).where(QuestionModel.id == reguar_user_id)

            await session.execute(q)

            await session.commit()

    async def delete_all(self) -> None:
        async with self._session() as session:
            q = delete(QuestionModel)

            await session.execute(q)

            await session.commit()

    async def count_all(self) -> int:
        async with self._session() as session:
            q = select(func.count(QuestionModel.id))

            return (await session.execute(q)).scalar()

    async def count_for_regular_users(self, regular_user_id: UUID) -> int:
        async with self._session() as session:
            q = select(func.count(QuestionModel.id)).where(
                QuestionModel.regular_user_id == regular_user_id
            )

            return (await session.execute(q)).scalar()

    async def count_unanswered(self) -> int:
        async with self._session() as session:
            q = select(func.count(QuestionModel.id)).where(
                QuestionModel.answers == None
            )

            return (await session.execute(q)).scalar()

    async def count_answered(self) -> int:
        async with self._session() as session:
            q = select(func.count(QuestionModel.id)).where(
                QuestionModel.answers != None
            )

            return (await session.execute(q)).scalar()

    async def count_answered_questions(self, regular_user_id: UUID) -> int:
        async with self._session() as session:
            q = select(func.count(QuestionModel.id)).where(
                and_(
                    QuestionModel.regular_user_id == regular_user_id,
                    QuestionModel.answers != None,  # noqa: 712
                )
            )

            return (await session.execute(q)).scalar()

    def _get_question_query_with_options(self, q: Select):
        return q.options(
            selectinload(QuestionModel.regular_user),
            selectinload(QuestionModel.current_support_user),
            selectinload(QuestionModel.question_attachments),
        )


class SAAnswersRepo(AnswersRepo):
    def __init__(self, repo_config: RepoConfig) -> None:
        self._session = repo_config.connection_provider

    async def add(
        self,
        answer: Answer,
    ) -> Answer:
        async with self._session() as session:
            answer_model = AnswerModel.from_entity(answer)

            session.add(answer_model)

            await session.commit()

            return answer

    async def update(self, answer: Answer) -> Answer:
        async with self._session() as session:
            answer_model = AnswersModel.from_entity(answer)

            await session.merge(answer_model)

            await session.commit()

            return answer

    async def get_all(self) -> list[Answer]:
        async with self._session() as session:
            q = self._get_answer_query_with_options(select(AnswerModel))

            result = (await session.execute(q)).scalars().all()

            return [elem.as_answer_entity() for elem in result]

    async def get_by_id(self, answer_id: UUID) -> Answer | None:
        async with self._session() as session:
            q = self._get_answer_query_with_options(
                select(AnswerModel).where(AnswerModel.id == answer_id)
            )

            result = (await session.execute(q)).scalars().first()

            return result and result.as_answer_entity()

    async def get_question_last_answer(
        self, question_id: UUID
    ) -> Answer | None:
        async with self._session() as session:
            q = self._get_answer_query_with_options(
                select(AnswerModel)
                .where(AnswerModel.question_id == question_id)
                .order_by(AnswerModel.date.desc())
            )

            result = (await session.execute(q)).scalars().first()

            return result and result.as_answer_entity()

    async def get_by_support_user_id(
        self, support_user_id: UUID
    ) -> list[Answer]:
        async with self._session() as session:
            q = self._get_answer_query_with_options(
                select(AnswerModel).where(
                    AnswerModel.support_user_id == support_user_id
                )
            )

            result = (await session.execute(q)).scalars().all()

            return [elem.as_answer_entity() for elem in result]

    async def get_by_question_id(self, question_id: UUID) -> list[Answer]:
        async with self._session() as session:
            q = self._get_answer_query_with_options(
                select(AnswerModel).where(
                    AnswerModel.question_id == question_id
                )
            )

            result = (await session.execute(q)).scalars().all()

            return [elem.as_answer_entity() for elem in result]

    async def get_by_tg_message_id(self, tg_mesage_id: int) -> Answer | None:
        async with self._session() as session:
            q = self._get_answer_query_with_options(
                select(AnswerModel).where(
                    AnswerModel.tg_message_id == tg_mesage_id
                )
            )

            result = (await session.execute(q)).scalars().first()

            return result and result.as_answer_entity()

    async def delete(self, answer_id: UUID) -> None:
        async with self._session() as session:
            q = self._get_answer_attachment_query_with_options(
                select(AnswerAttachmentModel).where(
                    AnswerAttachmentModel.id == id
                )
            )

            result = (await session.execute(q)).scallar()

            await session.delete(result)

            await session.commit()

    async def delete_by_support_user_id(self, support_user_id: UUID) -> None:
        async with self._session() as session:
            q = delete(AnswerModel).where(
                AnswerModel.support_user_id == support_user_id
            )

            await session.execute(q)

            await session.commit()

    async def delete_all_answers(self) -> None:
        async with self._session() as session:
            q = delete(AnswerModel)

            await session.execute(q)

            await session.commit()

    async def delete_by_question_id(self, question_id: UUID) -> None:
        async with self._session() as session:
            q = delete(AnswerModel).where(
                AnswerModel.question_id == question_id
            )

            await session.execute(q)

            await session.commit()

    async def count_all(self) -> int:
        async with self._session() as session:
            q = select(func.count(AnswerModel.id))

            return (await session.execute(q)).scalar()

    async def count_useful(self) -> int:
        async with self._session() as session:
            q = select(func.count(AnswerModel.id)).where(
                AnswerModel.is_useful == True  # noqa: 712
            )

            return (await session.execute(q)).scalar()

    async def count_unuseful_answers(self) -> int:
        async with self._session() as session:
            q = select(func.count(AnswerModel.id)).where(
                AnswerModel.is_useful == False  # noqa: 712
            )

            return (await session.execute(q)).scalar()

    async def count_by_question_id(self, question_id: UUID) -> int:
        async with self._session() as session:
            q = select(func.count(AnswerModel.id)).where(
                AnswerModel.question_id == question_id
            )

            return (await session.execute(q)).scalar()

    async def count_by_support_user_id(self, support_user_id: UUID) -> int:
        async with self._session() as session:
            q = select(func.count(AnswerModel.id)).where(
                AnswerModel.support_user_id == support_user_id
            )

            return (await session.execute(q)).scalar()

    async def count_useful_by_support_user_id(
        self, support_user_id: UUID
    ) -> int:
        async with self._session() as session:
            q = select(func.count(AnswerModel.id)).where(
                and_(
                    AnswerModel.is_useful == True,  # noqa: 712
                    AnswerModel.support_user_id == support_user_id,
                )
            )

            return (await session.execute(q)).scalar()

    async def count_unuseful_by_support_user_id(
        self, support_user_id: UUID
    ) -> int:
        async with self._session() as session:
            q = select(func.count(AnswerModel.id)).where(
                and_(
                    AnswerModel.is_useful == False,  # noqa: 712
                    AnswerModel.support_user_id == support_user_id,
                )
            )

            return (await session.execute(q)).scalar()

    async def count_for_regular_user(self, regular_user_id: UUID) -> int:
        async with self._session() as session:
            q = select(func.count(AnswerModel.id)).where(
                and_(
                    AnswerModel.question.and_(
                        QuestionModel.regular_user_id == regular_user_id
                    ),
                )
            )

            return (await session.execute(q)).scalar()

    async def count_useful_for_regular_user(
        self, regular_user_id: UUID
    ) -> int:
        async with self._session() as session:
            q = select(func.count(AnswerModel.id)).where(
                and_(
                    AnswerModel.question.and_(
                        QuestionModel.regular_user_id == regular_user_id
                    ),
                    AnswerModel.is_useful == True,  # noqa: 712
                )
            )

            return (await session.execute(q)).scalar()

    async def count_unuseful_for_regular_user(
        self, regular_user_id: UUID
    ) -> int:
        async with self._session() as session:
            q = select(func.count(AnswerModel.id)).where(
                and_(
                    AnswerModel.question.and_(
                        QuestionModel.regular_user_id == regular_user_id
                    ),
                    AnswerModel.is_useful == False,  # noqa: 712
                )
            )

            return (await session.execute(q)).scalar()

    async def count_usestimated_for_regular_user(
        self, regular_user_id: UUID
    ) -> int:
        async with self._session() as session:
            q = select(func.count(AnswerModel.id)).where(
                and_(
                    AnswerModel.question.and_(
                        QuestionModel.regular_user_id == regular_user_id
                    ),
                    AnswerModel.is_useful == None,  # noqa: 712
                )
            )

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

    def _get_answer_attachment_query_with_options(self, q: Select):
        return q.options(selectinload(AnswerAttachmentModel.answer))


class SARepo(Repo):
    def __init__(self, repo_config: RepoConfig) -> None:
        self._session = repo_config.connection_provider

    # ROLES METHODS

    async def add_role(self, role: Role) -> Role:
        async with self._session() as session:
            role_model = RoleModel(role)

            session.add(role_model)

            await session.commit()

            role.id = role_model.id  # type: ignore

            return role

    async def change_support_user_role(
        self, support_user_id: UUID, new_role_id: int
    ) -> None:
        async with self._session() as session:
            q = select(SupportUserModel).where(
                SupportUserModel.id == support_user_id
            )

            support_user = (await session.execute(q)).scalars().first()

            role_q = select(RoleModel).where(RoleModel.id == new_role_id)

            role = (await session.execute(role_q)).scalars().first()

            support_user.role = role

            session.commit()

    async def get_role_by_id(self, id: int) -> Role | None:
        async with self._session() as session:
            q = self._get_role_query_with_options(
                select(RoleModel).where(RoleModel.id == id)
            )

            result = (await session.execute(q)).scalars().first()

            return result and result.as_role_entity()

    async def get_role_by_name(self, name: str) -> Role | None:
        async with self._session() as session:
            q = self._get_role_query_with_options(
                select(RoleModel).where(RoleModel.name == name)
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
    ) -> list[Role]:
        async with self._session() as session:
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
            q = select(func.count(RoleModel.id))

            return (await session.execute(q)).scalar()

    def _get_role_query_with_options(self, q: Select):
        return q.options(selectinload(RoleModel.users))
