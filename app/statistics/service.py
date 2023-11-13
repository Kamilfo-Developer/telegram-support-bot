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
    StatisticsQueriesFactory,
)


class StatisticsService:
    def __init__(
        self, statistics_queries_factory: StatisticsQueriesFactory
    ) -> None:
        self.__query_factory = statistics_queries_factory

    async def get_regular_user_statistics(
        self,
        regular_user_id: RegularUserIdType,
    ) -> RegularUserStatistics:
        query = self.__query_factory.create_regular_user_statistics_query()

        return await query.execute(regular_user_id)

    async def get_support_user_statistics(
        self,
        support_user_id: SupportUserIdType,
    ) -> SupportUserStatistics:
        query = self.__query_factory.create_support_user_statistics_query()

        return await query.execute(support_user_id)

    async def get_role_statistics(
        self,
        role_id: RoleIdType,
    ) -> RoleStatistics:
        query = self.__query_factory.create_role_statistics_query()

        return await query.execute(role_id)

    async def get_question_statistics(
        self,
        question_id: QuestionIdType,
    ) -> QuestionStatistics:
        query = self.__query_factory.create_question_statistics_query()

        return await query.execute(question_id)

    async def get_answer_statistics(
        self,
        answer_id: AnswerIdType,
    ) -> AnswerStatistics:
        query = self.__query_factory.create_answer_statistics_query()

        return await query.execute(answer_id)

    async def get_global_statistics(
        self,
    ) -> GlobalStatistics:
        query = self.__query_factory.create_global_statistics_query()

        return await query.execute()
