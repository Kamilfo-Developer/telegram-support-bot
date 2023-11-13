from __future__ import annotations

from sqlalchemy import and_, func, select

from app.answers.infra.sa_models import AnswerAttachmentModel, AnswerModel
from app.questions.infra.sa_models import (
    QuestionAttachmentModel,
    QuestionModel,
)
from app.regular_users.infra.sa_models import RegularUserModel
from app.roles.infra.sa_models import RoleModel
from app.shared.db import SADBConfig
from app.shared.value_objects import (
    AnswerIdType,
    QuestionIdType,
    RegularUserIdType,
    RoleIdType,
    SupportUserIdType,
)
from app.statistics.dtos import (
    AnswerStatistics,
    GlobalStatistics,
    QuestionStatistics,
    RegularUserStatistics,
    RoleStatistics,
    SupportUserStatistics,
)
from app.statistics.queries import (
    GetAnswerStatisticsQuery,
    GetGlobalStatisticsQuery,
    GetQuestionStatisticsQuery,
    GetRegularUserStatisticsQuery,
    GetRoleStatisticsQuery,
    GetSupportUserStatisticsQuery,
    StatisticsQueriesFactory,
)
from app.support_users.infra.sa_models import SupportUserModel


class SAStatisticsQueriesFactory(StatisticsQueriesFactory):
    def __init__(self, db_config: SADBConfig) -> None:
        self.__db_config = db_config

    def create_regular_user_statistics_query(
        self,
    ) -> SAGetRegularUserStatisticsQuery:
        return SAGetRegularUserStatisticsQuery(self.__db_config)

    def create_support_user_statistics_query(
        self,
    ) -> SAGetSupportUserStatisticsQuery:
        return SAGetSupportUserStatisticsQuery(self.__db_config)

    def create_question_statistics_query(
        self,
    ) -> SAGetQuestionStatisticsQuery:
        return SAGetQuestionStatisticsQuery(self.__db_config)

    def create_answer_statistics_query(
        self,
    ) -> SAGetAnswerStatisticsQuery:
        return SAGetAnswerStatisticsQuery(self.__db_config)

    def create_role_statistics_query(
        self,
    ) -> SAGetRoleStatisticsQuery:
        return SAGetRoleStatisticsQuery(self.__db_config)

    def create_global_statistics_query(
        self,
    ) -> SAGetGlobalStatisticsQuery:
        return SAGetGlobalStatisticsQuery(self.__db_config)


class SAGetGlobalStatisticsQuery(GetGlobalStatisticsQuery):
    def __init__(self, config: SADBConfig) -> None:
        self.config = config

    async def execute(self) -> GlobalStatistics:
        async with self.config.connection_provider() as session:
            q_total_roles = select(func.count(RoleModel.id))

            q_total_regular_users = select(func.count(RegularUserModel.id))

            q_total_support_users = select(func.count(SupportUserModel.id))

            q_total_questions = select(func.count(QuestionModel.id))

            q_total_unanswered_questions = select(
                func.count(QuestionModel.id)
            ).where(QuestionModel.answers == None)

            q_total_answered_questions = select(
                func.count(QuestionModel.id)
            ).where(QuestionModel.answers != None)

            q_total_answers = select(func.count(AnswerModel.id))

            q_total_question_attachments = select(
                func.count(AnswerAttachmentModel.tg_file_id)
            )

            q_total_answer_attachments = select(
                func.count(AnswerAttachmentModel.tg_file_id)
            )

            q_total_useful_answers = select(func.count(AnswerModel.id)).where(
                AnswerModel.is_useful == True,  # noqa: E712
            )

            q_total_unuseful_answers = select(
                func.count(AnswerModel.id)
            ).where(
                AnswerModel.is_useful != True,  # noqa: E712
            )

            q_total_unestimated_answers = select(
                func.count(AnswerModel.id)
            ).where(
                AnswerModel.is_useful == None,  # noqa: E712
            )

            total_roles = await session.execute(q_total_roles)
            total_regular_users = await session.execute(q_total_regular_users)
            total_support_users = await session.execute(q_total_support_users)
            total_questions = await session.execute(q_total_questions)
            total_unanswered_questions = await session.execute(
                q_total_unanswered_questions
            )
            total_answered_questions = await session.execute(
                q_total_answered_questions
            )
            total_answers = await session.execute(q_total_answers)
            total_question_attachments = await session.execute(
                q_total_question_attachments
            )
            total_answer_attachments = await session.execute(
                q_total_answer_attachments
            )
            total_useful_answers = await session.execute(
                q_total_useful_answers
            )
            total_unuseful_answers = await session.execute(
                q_total_unuseful_answers
            )
            total_unestimated_answers = await session.execute(
                q_total_unestimated_answers
            )

            return GlobalStatistics(
                total_roles=total_roles.scalar() or 0,
                total_regular_users=total_regular_users.scalar() or 0,
                total_support_users=total_support_users.scalar() or 0,
                total_questions=total_questions.scalar() or 0,
                total_unanswered_questions=total_unanswered_questions.scalar()
                or 0,
                total_answers=total_answers.scalar() or 0,
                total_answered_questions=total_answered_questions.scalar()
                or 0,
                total_question_attachments=total_question_attachments.scalar()
                or 0,
                total_answer_attachments=total_answer_attachments.scalar()
                or 0,
                total_useful_answers=total_useful_answers.scalar() or 0,
                total_unuseful_answers=total_unuseful_answers.scalar() or 0,
                total_unestimated_answers=total_unestimated_answers.scalar()
                or 0,
            )


class SAGetRegularUserStatisticsQuery(GetRegularUserStatisticsQuery):
    def __init__(self, config: SADBConfig) -> None:
        self.config = config

    async def execute(
        self, regular_user_id: RegularUserIdType
    ) -> RegularUserStatistics:
        async with self.config.connection_provider() as session:
            q_asked_questions = select(func.count(QuestionModel.id)).where(
                QuestionModel.regular_user_id == regular_user_id
            )

            q_answered_questions = select(func.count(QuestionModel.id)).where(
                and_(
                    QuestionModel.regular_user_id == regular_user_id,
                    QuestionModel.answers != None,
                )
            )

            q_unanswered_questions = select(
                func.count(QuestionModel.id)
            ).where(
                and_(
                    QuestionModel.regular_user_id == regular_user_id,
                    QuestionModel.answers == None,
                )
            )

            q_answers_for_questions = select(func.count(AnswerModel.id)).where(
                AnswerModel.question.and_(
                    QuestionModel.regular_user_id == regular_user_id
                )
            )

            q_unestimated_answers = select(func.count(AnswerModel.id)).where(
                and_(
                    AnswerModel.question.and_(
                        QuestionModel.regular_user_id == regular_user_id
                    ),
                    AnswerModel.is_useful == None,
                )
            )

            q_useful_answers = select(func.count(AnswerModel.id)).where(
                and_(
                    AnswerModel.question.and_(
                        QuestionModel.regular_user_id == regular_user_id
                    ),
                    AnswerModel.is_useful == True,  # noqa: 712
                )
            )

            q_unuseful_answers = select(func.count(AnswerModel.id)).where(
                and_(
                    AnswerModel.question.and_(
                        QuestionModel.regular_user_id == regular_user_id
                    ),
                    AnswerModel.is_useful == False,  # noqa: 712
                )
            )

            asked_questions = await session.execute(q_asked_questions)

            answered_questions = await session.execute(q_answered_questions)

            unanswered_questions = await session.execute(
                q_unanswered_questions
            )

            answers_for_questions = await session.execute(
                q_answers_for_questions
            )

            unestimated_answers = await session.execute(q_unestimated_answers)

            useful_answers = await session.execute(q_useful_answers)

            unuseful_answers = await session.execute(q_unuseful_answers)

            return RegularUserStatistics(
                asked_questions.scalar() or 0,
                answered_questions.scalar() or 0,
                unanswered_questions.scalar() or 0,
                answers_for_questions.scalar() or 0,
                unestimated_answers.scalar() or 0,
                useful_answers.scalar() or 0,
                unuseful_answers.scalar() or 0,
            )


class SAGetSupportUserStatisticsQuery(GetSupportUserStatisticsQuery):
    def __init__(self, config: SADBConfig) -> None:
        self.config = config

    async def execute(
        self, support_user_id: SupportUserIdType
    ) -> SupportUserStatistics:
        async with self.config.connection_provider() as session:
            q_useful_answers = select(func.count(AnswerModel.id)).where(
                and_(
                    AnswerModel.support_user_id == support_user_id,
                    AnswerModel.is_useful == True,  # noqa: E712
                )
            )

            q_unuseful_answers = select(func.count(AnswerModel.id)).where(
                and_(
                    AnswerModel.support_user_id == support_user_id,
                    AnswerModel.is_useful == False,  # noqa: E712
                )
            )

            q_unestimated_answers = select(func.count(AnswerModel.id)).where(
                and_(
                    AnswerModel.support_user_id == support_user_id,
                    AnswerModel.is_useful == None,  # noqa: E712
                )
            )

            q_total_answers = select(func.count(AnswerModel.id)).where(
                and_(
                    AnswerModel.support_user_id == support_user_id,
                )
            )

            useful_answers = await session.execute(q_useful_answers)

            unuseful_answers = await session.execute(q_unuseful_answers)

            unestimated_answers = await session.execute(q_unestimated_answers)

            total_answers = await session.execute(q_total_answers)

            return SupportUserStatistics(
                useful_answers=useful_answers.scalar() or 0,
                unuseful_answers=unuseful_answers.scalar() or 0,
                unestimated_answers=unestimated_answers.scalar() or 0,
                total_answers=total_answers.scalar() or 0,
            )


class SAGetRoleStatisticsQuery(GetRoleStatisticsQuery):
    def __init__(self, config: SADBConfig) -> None:
        self.config = config

    async def execute(self, role_id: RoleIdType) -> RoleStatistics:
        async with self.config.connection_provider() as session:
            q_total_users = select(func.count(SupportUserModel.id)).where(
                SupportUserModel.role_id == role_id
            )

            total_users = await session.execute(q_total_users)

            return RoleStatistics(
                total_users.scalar() or 0,
            )


class SAGetAnswerStatisticsQuery(GetAnswerStatisticsQuery):
    def __init__(self, config: SADBConfig) -> None:
        self.config = config

    async def execute(self, answer_id: AnswerIdType) -> AnswerStatistics:
        async with self.config.connection_provider() as session:
            async with self.config.connection_provider() as session:
                q_total_attachments = select(
                    func.count(AnswerAttachmentModel.tg_file_id)
                ).where(AnswerAttachmentModel.answer_id == answer_id)

                total_attachments = await session.execute(q_total_attachments)

                return AnswerStatistics(
                    total_attachments.scalar() or 0,
                )


class SAGetQuestionStatisticsQuery(GetQuestionStatisticsQuery):
    def __init__(self, config: SADBConfig) -> None:
        self.config = config

    async def execute(self, question_id: QuestionIdType) -> QuestionStatistics:
        async with self.config.connection_provider() as session:
            async with self.config.connection_provider() as session:
                q_total_answers = select(func.count(AnswerModel.id)).where(
                    AnswerModel.question_id == question_id
                )

                q_total_attachments = select(
                    func.count(QuestionAttachmentModel.tg_file_id)
                ).where(QuestionAttachmentModel.question_id == question_id)

                total_answers = await session.execute(q_total_answers)

                total_attachments = await session.execute(q_total_attachments)

                return QuestionStatistics(
                    total_answers.scalar() or 0,
                    total_attachments.scalar() or 0,
                )
