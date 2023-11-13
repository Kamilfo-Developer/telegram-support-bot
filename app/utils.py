from __future__ import annotations
from abc import ABC, abstractmethod


from datetime import datetime, timezone
from enum import Enum
from typing import Any, Callable, Generic, Self, Type, TypeVar
from uuid import UUID

from telegram import Message


class TgFileType(Enum):
    IMAGE = "IMAGE"
    VIDEO = "VIDEO"
    AUDIO = "AUDIO"
    VOICE = "VOICE"
    DOCUMENT = "DOCUMENT"


class ValueObject:
    def __eq__(self, __value: object) -> bool:
        return isinstance(__value, self.__class__) and vars(self) == vars(
            __value
        )


T = TypeVar("T")


class ReadQuery(ABC, Generic[T]):
    @abstractmethod
    async def execute(self, *args, **kwargs) -> T:
        ...


class StrWithMaxLength(str):
    """When an instance of this class inited,
    checks whether length of the string greater
    MAX_LENGTH class property

    If so, throws ValueError

    WARNING!!!
    When inherited from this class,
    MAX_LENGTH class property must be specified
    otherwise an AttributeError instance will be raised
    """

    MAX_LENGTH: int

    def __init__(self, string: str) -> None:
        super(str, string).__init__()

        if not self.MAX_LENGTH:
            raise AttributeError(
                "MAX_LENGTH class attribute must be specified"
                "when inerited from this class"
            )

        if len(self) > self.MAX_LENGTH:
            raise ValueError(
                f"Length of the string must be less "
                f"or equal to {self.MAX_LENGTH}"
            )


class ConvertationCheckable:
    """A mixin with class method, which allows to check
    whether an object can be converted to the child class"""

    @classmethod
    def can_be_converted_to_this_type(cls, obj: Any) -> bool:
        """Checks whether ```obj``` can be converted to the type


        Args:
            obj (Any): obj for checking

        Returns:
            bool: True if ```obj``` can be converted, False otherwise
        """

        try:
            cls(obj)  # type: ignore

            return True

        except Exception:
            return False


class ArgumentsValidator:
    def __init__(self, arguments: list[Any]) -> None:
        self.__is_valid = True
        self.__arguments = arguments
        self.__curr_arg_index = 0

    def next(self) -> Self:
        if len(self.__arguments) < self.__curr_arg_index + 1:
            self.__is_valid = False

            return self

        self.__curr_arg_index += 1

        return self

    def convertable(
        self, type_to_check: Type[Any | ConvertationCheckable]
    ) -> Self:
        if not self.__is_valid:
            return self

        try:
            curr_argument = self.__arguments[self.__curr_arg_index]
        except IndexError:
            self.__is_valid = False

            return self

        if type_to_check is ConvertationCheckable:
            self.__is_valid = type_to_check.can_be_converted_to_this_type(
                curr_argument
            )

            return self

        try:
            type_to_check(curr_argument)  # type: ignore

        except Exception:
            self.__is_valid = False

        return self

    def satisfies(self, callback: Callable[[str], bool]) -> Self:
        if not self.__is_valid:
            return self

        self.__is_valid = callback(self.__arguments[self.__curr_arg_index])

        return self

    def is_valid(self) -> bool:
        if self.__curr_arg_index + 1 != len(self.__arguments):
            return False

        return self.__is_valid


def get_file_type_and_file_id(
    message: Message,
) -> tuple[TgFileType | None, str | None]:
    if not message:
        raise ValueError("Update doesn't contain any file")

    if message.photo:
        return (TgFileType.IMAGE, message.photo[-1].file_id)

    if message.video:
        return (TgFileType.VIDEO, message.video.file_id)

    if message.document:
        return (TgFileType.DOCUMENT, message.document.file_id)

    if message.audio:
        return (TgFileType.AUDIO, message.audio.file_id)

    if message.voice:
        return (TgFileType.VOICE, message.voice.file_id)

    return (None, None)


def is_string_uuid(string: str) -> bool:
    try:
        UUID(string)

        return True

    except ValueError:
        return False


def is_string_int(string: str) -> bool:
    try:
        int(string)

        return True

    except ValueError:
        return False


def is_sub_list(a: list[Any], b: list[Any]) -> bool:
    """Checks if each element of a is in b
    without considering the order of the elements

    Args:
        a (list[Any]): list of comparable elements
        b (list[Any]): list of comparable elements

    Returns:
        bool: True if each element of a is in b, otherwise False
    """
    return all([x in b for x in a])


def get_eu_formated_datetime(dt: datetime, tz: timezone) -> str:
    return (
        dt.replace(tzinfo=timezone.utc)
        .astimezone(tz)
        .strftime("%m.%d.%Y, %H:%M:%S")
    )


def get_us_formated_datetime(dt: datetime, tz: timezone) -> str:
    return (
        dt.replace(tzinfo=timezone.utc)
        .astimezone(tz)
        .strftime("%d.%m.%Y, %H:%M:%S")
    )


# Mixins


class IdComparable:
    """This mixin allows comparing two different entities
    with the same `_id` attribute
    """

    _id: Any

    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, IdComparable) and self._id == __o._id
