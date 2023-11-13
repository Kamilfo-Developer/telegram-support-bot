from __future__ import annotations

from app.shared.db import DBConfig
from app.shared.value_objects import (
    RoleIdType,
    TgMessageIdType,
    TgUserId,
)
from app.support_users.dtos import (
    AnswerInfo,
    QuestionInfo,
    RegularUserInfo,
    RoleInfo,
    SupportUserInfo,
)
from app.utils import ReadQuery
import abc


class SupportUsersQueriesFactory(abc.ABC):
    @abc.abstractmethod
    def __init__(self, db_config: DBConfig) -> None:
        ...

    @abc.abstractmethod
    def create_get_regular_user_info_by_tg_user_id_query(
        self,
    ) -> GetRegularUserInfoByTgUserIdQuery:
        ...

    @abc.abstractmethod
    def create_get_support_user_info_by_tg_user_id_query(
        self,
    ) -> GetSupportUserInfoByTgUserIdQuery:
        ...

    @abc.abstractmethod
    def create_get_role_info_by_id_query(self) -> GetRoleInfoByIdQuery:
        ...

    @abc.abstractmethod
    def create_get_question_info_by_tg_message_id_query(
        self,
    ) -> GetQuestionInfoByTgMessageIdQuery:
        ...

    @abc.abstractmethod
    def create_get_answer_info_by_tg_message_id_query(
        self,
    ) -> GetAnswerInfoByTgMessageIdQuery:
        ...

    @abc.abstractmethod
    def create_get_question_to_answer_query(
        self,
    ) -> GetQuestionToAnswerInfoByTgMessageIdQuery:
        ...


class GetRegularUserInfoByTgUserIdQuery(ReadQuery[RegularUserInfo | None]):
    @abc.abstractmethod
    def __init__(self, config: DBConfig) -> None:
        ...

    @abc.abstractmethod
    async def execute(
        self, regular_user_tg_id: TgUserId
    ) -> RegularUserInfo | None:
        ...


class GetSupportUserInfoByTgUserIdQuery(ReadQuery[SupportUserInfo | None]):
    @abc.abstractmethod
    def __init__(self, config: DBConfig) -> None:
        ...

    @abc.abstractmethod
    async def execute(
        self, support_user_tg_id: TgUserId
    ) -> SupportUserInfo | None:
        ...


class GetRoleInfoByIdQuery(ReadQuery[RoleInfo | None]):
    @abc.abstractmethod
    def __init__(self, config: DBConfig) -> None:
        ...

    @abc.abstractmethod
    async def execute(self, role_id: RoleIdType) -> RoleInfo | None:
        ...


class GetQuestionInfoByTgMessageIdQuery(ReadQuery[QuestionInfo | None]):
    @abc.abstractmethod
    def __init__(self, config: DBConfig) -> None:
        ...

    @abc.abstractmethod
    async def execute(
        self, question_tg_id: TgMessageIdType
    ) -> QuestionInfo | None:
        ...


class GetQuestionToAnswerInfoByTgMessageIdQuery(
    ReadQuery[QuestionInfo | None]
):
    @abc.abstractmethod
    def __init__(self, config: DBConfig) -> None:
        ...

    @abc.abstractmethod
    async def execute(self) -> QuestionInfo | None:
        ...


class GetAnswerInfoByTgMessageIdQuery(ReadQuery[AnswerInfo | None]):
    @abc.abstractmethod
    def __init__(self, config: DBConfig) -> None:
        ...

    @abc.abstractmethod
    async def execute(
        self, answer_tg_id: TgMessageIdType
    ) -> AnswerInfo | None:
        ...
