from __future__ import annotations

import abc

from app.shared.db import DBConfig
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
from app.utils import ReadQuery


class StatisticsQueriesFactory(abc.ABC):
    @abc.abstractmethod
    def __init__(self, db_config: DBConfig) -> None:
        ...

    @abc.abstractmethod
    def create_regular_user_statistics_query(
        self,
    ) -> GetRegularUserStatisticsQuery:
        ...

    @abc.abstractmethod
    def create_support_user_statistics_query(
        self,
    ) -> GetSupportUserStatisticsQuery:
        ...

    @abc.abstractmethod
    def create_question_statistics_query(
        self,
    ) -> GetQuestionStatisticsQuery:
        ...

    @abc.abstractmethod
    def create_answer_statistics_query(
        self,
    ) -> GetAnswerStatisticsQuery:
        ...

    @abc.abstractmethod
    def create_role_statistics_query(
        self,
    ) -> GetRoleStatisticsQuery:
        ...

    @abc.abstractmethod
    def create_global_statistics_query(
        self,
    ) -> GetGlobalStatisticsQuery:
        ...


class GetRegularUserStatisticsQuery(ReadQuery[RegularUserStatistics]):
    @abc.abstractmethod
    async def execute(
        self, regular_user_id: RegularUserIdType
    ) -> RegularUserStatistics:
        ...


class GetSupportUserStatisticsQuery(ReadQuery[SupportUserStatistics]):
    @abc.abstractmethod
    async def execute(
        self, support_user_id: SupportUserIdType
    ) -> SupportUserStatistics:
        ...


class GetRoleStatisticsQuery(ReadQuery[RoleStatistics]):
    @abc.abstractmethod
    async def execute(self, role_id: RoleIdType) -> RoleStatistics:
        ...


class GetQuestionStatisticsQuery(ReadQuery[QuestionStatistics]):
    @abc.abstractmethod
    async def execute(self, question_id: QuestionIdType) -> QuestionStatistics:
        ...


class GetAnswerStatisticsQuery(ReadQuery[AnswerStatistics]):
    @abc.abstractmethod
    async def execute(self, answer_id: AnswerIdType) -> AnswerStatistics:
        ...


class GetGlobalStatisticsQuery(ReadQuery[GlobalStatistics]):
    @abc.abstractmethod
    async def execute(self) -> GlobalStatistics:
        ...
