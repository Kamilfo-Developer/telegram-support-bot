from dataclasses import dataclass
from app.shared.value_objects import (
    TgCaption,
    TgFileIdType,
    TgMessageIdType,
    TgMessageText,
    TgUserId,
)
from app.utils import TgFileType


@dataclass(frozen=True)
class TgUser:
    tg_user_id: TgUserId
    first_name: str
    last_name: str
    language_code: str


@dataclass(frozen=True)
class TgMessage:
    tg_message_id: TgMessageIdType
    message_text: TgMessageText


@dataclass(frozen=True)
class TgFile:
    file_id: TgFileIdType
    file_type: TgFileType
    caption: TgCaption | None


@dataclass(frozen=True)
class BindQuestionCallbackData:
    question_tg_id: TgMessageIdType
