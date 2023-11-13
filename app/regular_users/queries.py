from __future__ import annotations

import abc

from app.regular_users.dtos import AnswerEstimationInfo
from app.shared.db import DBConfig
from app.shared.value_objects import (
    AnswerIdType,
)
from app.utils import ReadQuery


class RegularUsersQueriesFactory(abc.ABC):
    @abc.abstractmethod
    def __init__(self, db_config: DBConfig) -> None:
        ...

    @abc.abstractmethod
    def create_answer_estimation_info_query(
        self,
    ) -> GetAnswerEstimationInfo:
        ...


class GetAnswerEstimationInfo(ReadQuery[AnswerEstimationInfo | None]):
    @abc.abstractmethod
    async def execute(
        self, answer_id: AnswerIdType
    ) -> AnswerEstimationInfo | None:
        ...
