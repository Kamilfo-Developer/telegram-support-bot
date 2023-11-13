from __future__ import annotations
from datetime import timezone

from typing import TypeVar
from uuid import UUID

from pytz.tzinfo import BaseTzInfo, DstTzInfo, StaticTzInfo

from app.utils import ConvertationCheckable, StrWithMaxLength, ValueObject

# Value Objects


class RolePermissions(ValueObject):
    can_answer_questions: bool
    can_manage_support_users: bool

    def __init__(
        self, can_answer_questions: bool, can_manage_support_users: bool
    ) -> None:
        self.can_answer_questions = can_answer_questions
        self.can_manage_support_users = can_manage_support_users


class TgCaption(StrWithMaxLength):
    MAX_LENGTH = 1024


class TgMessageText(StrWithMaxLength):
    MAX_LENGTH = 4096


class UUIDUniversalTypeConvertable(UUID):
    def __init__(self, obj: object):
        if isinstance(obj, UUID):
            UUID.__init__(self, obj.hex)

            return

        if isinstance(obj, str):
            UUID.__init__(self, obj)

            return

        raise ValueError("Unsupported type for UUID")


class IntUniversalTypeConvertable(int):
    def __init__(self, obj: object):
        int.__init__(obj)  # type: ignore


class StrUniversalTypeConvertable(str):
    def __init__(self, obj: object):
        str.__init__(obj)  # type: ignore


class TgFileIdType(StrUniversalTypeConvertable, ConvertationCheckable):
    pass


class TgMessageType(IntUniversalTypeConvertable, ConvertationCheckable):
    pass


class TgMessageIdType(IntUniversalTypeConvertable, ConvertationCheckable):
    pass


class RoleIdType(IntUniversalTypeConvertable, ConvertationCheckable):
    def is_initialized(self) -> bool:
        return True


class NullRoleId(RoleIdType):
    def __init__(self) -> None:
        pass

    def __eq__(self, __value: object) -> bool:
        return False

    def is_initialized(self) -> bool:
        return False


class QuestionIdType(UUIDUniversalTypeConvertable, ConvertationCheckable):
    pass


class AnswerIdType(UUIDUniversalTypeConvertable, ConvertationCheckable):
    pass


class RegularUserIdType(UUIDUniversalTypeConvertable, ConvertationCheckable):
    pass


class SupportUserIdType(UUIDUniversalTypeConvertable, ConvertationCheckable):
    pass


class TgUserId(IntUniversalTypeConvertable, ConvertationCheckable):
    pass


TimezoneType = TypeVar(
    "TimezoneType", timezone, DstTzInfo, BaseTzInfo, StaticTzInfo
)
