from __future__ import annotations
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    ReplyKeyboardRemove,
)
from uuid import UUID
from enum import Enum
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from bot.entities.attachment import Attachment


def get_file_type_and_file_id(
    update: Update,
) -> tuple[AttachmentType | None, str | None]:
    if update.message.photo:
        return (AttachmentType.IMAGE, update.message.photo[-1].file_id)

    if update.message.video:
        return (AttachmentType.VIDEO, update.message.video.file_id)

    if update.message.document:
        return (AttachmentType.DOCUMENT, update.message.document.file_id)

    if update.message.audio:
        return (AttachmentType.AUDIO, update.message.audio.file_id)

    if update.message.voice:
        return (AttachmentType.VOICE, update.message.voice.file_id)

    return (None, None)


def is_string_uuid(string: str):
    try:
        UUID(string)

        return True

    except ValueError:
        return False


def is_string_int(string: str):
    try:
        int(string)

        return True

    except ValueError:
        return False


class AttachmentType(Enum):
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    VOICE = "voice"
    DOCUMENT = "document"


class IdComparable:
    id: Any

    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, self.__class__) and self.id == __o.id
