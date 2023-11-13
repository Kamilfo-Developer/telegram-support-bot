from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.answers.infra.sa_models import AnswerModel
from app.questions.infra.sa_models import QuestionModel
from app.regular_users.dtos import AnswerEstimationInfo
from app.regular_users.queries import (
    GetAnswerEstimationInfo,
    RegularUsersQueriesFactory,
)
from app.shared.db import SADBConfig
from app.shared.value_objects import AnswerIdType


class SARegularUsersQueriesFactory(RegularUsersQueriesFactory):
    def __init__(self, db_config: SADBConfig) -> None:
        self.__db_config = db_config

    def create_answer_estimation_info_query(
        self,
    ) -> SAGetAnswerEstimationInfo:
        return SAGetAnswerEstimationInfo(self.__db_config)


class SAGetAnswerEstimationInfo(GetAnswerEstimationInfo):
    def __init__(self, config: SADBConfig) -> None:
        self.config = config

    async def execute(
        self, answer_id: AnswerIdType
    ) -> AnswerEstimationInfo | None:
        async with self.config.connection_provider() as session:
            q = (
                select(AnswerModel)
                .where(AnswerModel.id == answer_id)
                .options(
                    selectinload(
                        AnswerModel.support_user, AnswerModel.question
                    ).selectinload(QuestionModel.regular_user)
                )
            )

            answer = (await session.execute(q)).scalars().first()

            if not answer:
                return None

            return AnswerEstimationInfo(
                answer.as_dto(),
                answer.question.as_dto(),
                answer.support_user.as_dto(),
                answer.question.regular_user.as_dto(),
            )
