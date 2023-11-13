from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.orm import selectinload

from app.answers.infra.sa_models import AnswerModel
from app.questions.infra.sa_models import QuestionModel
from app.regular_users.infra.sa_models import RegularUserModel
from app.roles.infra.sa_models import RoleModel
from app.shared.db import SADBConfig
from app.shared.value_objects import RoleIdType, TgMessageIdType, TgUserId
from app.statistics.infra.sa_queries import (
    SAGetAnswerStatisticsQuery,
    SAGetQuestionStatisticsQuery,
    SAGetRegularUserStatisticsQuery,
    SAGetRoleStatisticsQuery,
    SAGetSupportUserStatisticsQuery,
)
from app.support_users.dtos import (
    AnswerInfo,
    QuestionInfo,
    RegularUserInfo,
    RoleInfo,
    SupportUserInfo,
)
from app.support_users.infra.sa_models import SupportUserModel
from app.support_users.queries import (
    GetAnswerInfoByTgMessageIdQuery,
    GetQuestionInfoByTgMessageIdQuery,
    GetQuestionToAnswerInfoByTgMessageIdQuery,
    GetRegularUserInfoByTgUserIdQuery,
    GetRoleInfoByIdQuery,
    GetSupportUserInfoByTgUserIdQuery,
    SupportUsersQueriesFactory,
)


class SASupportUsersQueriesFactory(SupportUsersQueriesFactory):
    def __init__(self, db_config: SADBConfig) -> None:
        self.__db_config = db_config

    def create_get_regular_user_info_by_tg_user_id_query(
        self,
    ) -> SAGetRegularUserInfoByTgUserIdQuery:
        return SAGetRegularUserInfoByTgUserIdQuery(self.__db_config)

    def create_get_support_user_info_by_tg_user_id_query(
        self,
    ) -> SAGetSupportUserInfoByTgUserIdQuery:
        return SAGetSupportUserInfoByTgUserIdQuery(self.__db_config)

    def create_get_role_info_by_id_query(self) -> SAGetRoleInfoByIdQuery:
        return SAGetRoleInfoByIdQuery(self.__db_config)

    def create_get_question_info_by_tg_message_id_query(
        self,
    ) -> SAGetQuestionInfoByTgMessageIdQuery:
        return SAGetQuestionInfoByTgMessageIdQuery(self.__db_config)

    def create_get_answer_info_by_tg_message_id_query(
        self,
    ) -> SAGetAnswerInfoByTgMessageIdQuery:
        return SAGetAnswerInfoByTgMessageIdQuery(self.__db_config)

    def create_get_question_to_answer_query(
        self,
    ) -> GetQuestionToAnswerInfoByTgMessageIdQuery:
        return SAGetQuestionToAnswerInfoByTgMessageIdQuery(self.__db_config)


class SAGetRegularUserInfoByTgUserIdQuery(GetRegularUserInfoByTgUserIdQuery):
    def __init__(self, config: SADBConfig) -> None:
        self.config = config

    async def execute(
        self, regular_user_tg_id: TgUserId
    ) -> RegularUserInfo | None:
        async with self.config.connection_provider() as session:
            q = select(RegularUserModel).where(
                RegularUserModel.tg_bot_user_id == regular_user_tg_id
            )

            regular_user = (await session.execute(q)).scalars().first()

            if not regular_user:
                return None

            stats_query = SAGetRegularUserStatisticsQuery(self.config)

            return RegularUserInfo(
                regular_user_dto=regular_user.as_dto(),
                statistics=await stats_query.execute(regular_user.id),
            )


class SAGetSupportUserInfoByTgUserIdQuery(GetSupportUserInfoByTgUserIdQuery):
    def __init__(self, config: SADBConfig) -> None:
        self.config = config

    async def execute(
        self, support_user_tg_id: TgUserId
    ) -> SupportUserInfo | None:
        async with self.config.connection_provider() as session:
            q = select(SupportUserModel).where(
                SupportUserModel.tg_bot_user_id == support_user_tg_id
            )

            support_user = (await session.execute(q)).scalars().first()

            if not support_user:
                return None

            stats_query = SAGetSupportUserStatisticsQuery(self.config)

            return SupportUserInfo(
                support_user_dto=support_user.as_dto(),
                statistics=await stats_query.execute(support_user.id),
            )


class SAGetRoleInfoByIdQuery(GetRoleInfoByIdQuery):
    def __init__(self, config: SADBConfig) -> None:
        self.config = config

    async def execute(self, role_id: RoleIdType) -> RoleInfo | None:
        async with self.config.connection_provider() as session:
            q = select(RoleModel).where(RoleModel.id == role_id)

            role = (await session.execute(q)).scalars().first()

            if not role:
                return None

            stats_query = SAGetRoleStatisticsQuery(self.config)

            return RoleInfo(
                role_dto=role.as_dto(),
                statistics=await stats_query.execute(role.id),
            )


class SAGetQuestionInfoByTgMessageIdQuery(GetQuestionInfoByTgMessageIdQuery):
    def __init__(self, config: SADBConfig) -> None:
        self.config = config

    async def execute(
        self, question_tg_id: TgMessageIdType
    ) -> QuestionInfo | None:
        async with self.config.connection_provider() as session:
            q = (
                select(QuestionModel)
                .where(QuestionModel.tg_message_id == question_tg_id)
                .options(selectinload(QuestionModel.regular_user))
            )

            question = (await session.execute(q)).scalars().first()

            if not question:
                return None

            stats_query = SAGetQuestionStatisticsQuery(self.config)

            return QuestionInfo(
                question_dto=question.as_dto(),
                regular_user_asked_dto=question.regular_user.as_dto(),
                statistics=await stats_query.execute(question.id),
            )


class SAGetQuestionToAnswerInfoByTgMessageIdQuery(
    GetQuestionToAnswerInfoByTgMessageIdQuery
):
    def __init__(self, config: SADBConfig) -> None:
        self.config = config

    async def execute(self) -> QuestionInfo | None:
        async with self.config.connection_provider() as session:
            q = (
                select(QuestionModel)
                .where(QuestionModel.current_support_user == None)
                .where(QuestionModel.answers == None)
                .order_by(func.random())
                .limit(1)
                .options(selectinload(QuestionModel.regular_user))
            )

            question = (await session.execute(q)).scalars().first()

            if not question:
                return None

            stats_query = SAGetQuestionStatisticsQuery(self.config)

            return QuestionInfo(
                question_dto=question.as_dto(),
                regular_user_asked_dto=question.regular_user.as_dto(),
                statistics=await stats_query.execute(question.id),
            )


class SAGetAnswerInfoByTgMessageIdQuery(GetAnswerInfoByTgMessageIdQuery):
    def __init__(self, config: SADBConfig) -> None:
        self.config = config

    async def execute(
        self, answer_tg_id: TgMessageIdType
    ) -> AnswerInfo | None:
        async with self.config.connection_provider() as session:
            q = (
                select(AnswerModel)
                .where(AnswerModel.tg_message_id == answer_tg_id)
                .options(
                    selectinload(AnswerModel.support_user),
                    selectinload(AnswerModel.question),
                )
            )

            answer = (await session.execute(q)).scalars().first()

            if not answer:
                return None

            stats_query = SAGetAnswerStatisticsQuery(self.config)

            return AnswerInfo(
                answer_dto=answer.as_dto(),
                answered_quetsion_dto=answer.question.as_dto(),
                support_user_answered_dto=answer.support_user.as_dto(),
                statistics=await stats_query.execute(answer.id),
            )
