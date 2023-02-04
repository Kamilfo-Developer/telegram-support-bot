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
import abc

if TYPE_CHECKING:
    from bot.entities.attachment import Attachment


class MessageToSend:
    def __init__(
        self,
        messages: list[str],
        markup: ReplyKeyboardMarkup
        | ReplyKeyboardRemove
        | InlineKeyboardMarkup
        | None = None,
        chat_id: int | None = None,
        reply_to: int | None = None,
        parse_mode: str | None = "Markdown",
    ):
        self.messages = messages
        self.markup = markup
        self.chat_id = chat_id
        self.reply_to = reply_to
        self.parse_mode = parse_mode


class FileToSend(abc.ABC):
    file_id: str
    chat_id: int | None
    reply_to: int | None

    @abc.abstractmethod
    async def send(self, update: Update):
        raise NotImplementedError


class ImageToSend(FileToSend):
    def __init__(
        self,
        file_id: str,
        chat_id: int | None = None,
        reply_to: int | None = None,
        caption: str | None = None,
    ):
        self.file_id = file_id
        self.caption = caption
        self.chat_id = chat_id
        self.reply_to = reply_to

    async def send(self, update: Update):
        await update.get_bot().send_photo(
            self.chat_id or update.effective_chat.id,  # type: ignore
            photo=self.file_id,
            caption=self.caption,  # type: ignore
            reply_to_message_id=self.reply_to,  # type: ignore
        )


class VideoToSend(FileToSend):
    def __init__(
        self,
        file_id: str,
        chat_id: int | None = None,
        reply_to: int | None = None,
        caption: str | None = None,
    ):
        self.file_id = file_id
        self.caption = caption
        self.chat_id = chat_id
        self.reply_to = reply_to

    async def send(self, update: Update):
        await update.get_bot().send_video(
            self.chat_id or update.effective_chat.id,  # type: ignore
            video=self.file_id,
            caption=self.caption,  # type: ignore
            reply_to_message_id=self.reply_to,  # type: ignore
        )


class AudioToSend(FileToSend):
    def __init__(
        self,
        file_id: str,
        chat_id: int | None = None,
        reply_to: int | None = None,
        caption: str | None = None,
    ):
        self.file_id = file_id
        self.caption = caption
        self.chat_id = chat_id
        self.reply_to = reply_to

    async def send(self, update: Update):
        await update.get_bot().send_audio(
            self.chat_id or update.effective_chat.id,  # type: ignore
            audio=self.file_id,
            caption=self.caption,  # type: ignore
            reply_to_message_id=self.reply_to,  # type: ignore
        )


class DocumentToSend(FileToSend):
    def __init__(
        self,
        file_id: str,
        chat_id: int | None = None,
        reply_to: int | None = None,
        caption: str | None = None,
    ):
        self.file_id = file_id
        self.chat_id = chat_id
        self.reply_to = reply_to
        self.caption = caption

    async def send(self, update: Update):
        await update.get_bot().send_document(
            self.chat_id or update.effective_chat.id,  # type: ignore
            document=self.file_id,
            reply_to_message_id=self.reply_to,  # type: ignore
        )


class VoiceToSend(FileToSend):
    def __init__(
        self,
        file_id: str,
        chat_id: int | None = None,
        reply_to: int | None = None,
    ):
        self.file_id = file_id
        self.chat_id = chat_id
        self.reply_to = reply_to

    async def send(self, update: Update):
        await update.get_bot().send_voice(
            self.chat_id or update.effective_chat.id,  # type: ignore
            voice=self.file_id,
            reply_to_message_id=self.reply_to,  # type: ignore
        )


def get_file_to_send_from_attachment_entity(
    attachment: Attachment,
    chat_id: int | None = None,
    reply_to: int | None = None,
    caption: str | None = None,
) -> FileToSend:
    match attachment.attachment_type:
        case AttachmentType.IMAGE:
            return ImageToSend(
                attachment.tg_file_id,
                chat_id=chat_id,
                reply_to=reply_to,
                caption=caption,
            )

        case AttachmentType.VIDEO:
            return VideoToSend(  # type: ignore
                attachment.tg_file_id,
                chat_id=chat_id,
                reply_to=reply_to,
                caption=caption,
            )

        case AttachmentType.AUDIO:
            return AudioToSend(  # type: ignore
                attachment.tg_file_id,
                chat_id=chat_id,
                reply_to=reply_to,
                caption=caption,
            )

        case AttachmentType.VOICE:
            return VoiceToSend(
                attachment.tg_file_id,
                chat_id=chat_id,
                reply_to=reply_to,
            )

        case AttachmentType.DOCUMENT:
            return DocumentToSend(  # type: ignore
                attachment.tg_file_id,
                chat_id=chat_id,
                reply_to=reply_to,
            )

    raise ValueError("Incorrect type of attachment")


async def send_text_messages(
    message_to_send: MessageToSend, update: Update, *args, **kwargs
):
    messages = message_to_send.messages

    if len(messages) > 1:
        for message in messages[:-1]:
            await update.get_bot().send_message(
                message_to_send.chat_id
                or update.effective_chat.id,  # type: ignore
                message,
                *args,
                **kwargs,
                parse_mode=message_to_send.parse_mode,
                reply_to_message_id=message_to_send.reply_to,  # type: ignore
            )

        await update.get_bot().send_message(
            message_to_send.chat_id
            or update.effective_chat.id,  # type: ignore
            messages[-1],
            *args,
            **kwargs,
            parse_mode=message_to_send.parse_mode,
            reply_to_message_id=message_to_send.reply_to,  # type: ignore
            reply_markup=message_to_send.markup,  # type: ignore
        )

        return

    for message in messages:
        await update.get_bot().send_message(
            message_to_send.chat_id
            or update.effective_chat.id,  # type: ignore
            message,
            *args,
            **kwargs,
            parse_mode=message_to_send.parse_mode,
            reply_to_message_id=message_to_send.reply_to,  # type: ignore
            reply_markup=message_to_send.markup,  # type: ignore
        )


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
