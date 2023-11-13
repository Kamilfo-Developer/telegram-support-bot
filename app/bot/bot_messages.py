from __future__ import annotations

import abc

from telegram import (
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    Update,
)


class MessagesToSendFactory(abc.ABC):
    @abc.abstractmethod
    def __init__(self) -> None:
        ...

    @abc.abstractmethod
    def get_text_to_send(
        self,
        messages: list[str],
        markup: ReplyKeyboardMarkup
        | ReplyKeyboardRemove
        | InlineKeyboardMarkup
        | None = None,
        chat_id: int | None = None,
        reply_to: int | None = None,
        parse_mode: str | None = "Markdown",
    ) -> TextToSend:
        ...

    @abc.abstractmethod
    def get_image_to_send(
        self,
        file_id: str,
        chat_id: int | None = None,
        reply_to: int | None = None,
        caption: str | None = None,
    ) -> ImageToSend:
        ...

    @abc.abstractmethod
    def get_video_to_send(
        self,
        file_id: str,
        chat_id: int | None = None,
        reply_to: int | None = None,
        caption: str | None = None,
    ) -> VideoToSend:
        ...

    @abc.abstractmethod
    def get_audio_to_send(
        self,
        file_id: str,
        chat_id: int | None = None,
        reply_to: int | None = None,
        caption: str | None = None,
    ) -> AudioToSend:
        ...

    @abc.abstractmethod
    def get_document_to_send(
        self,
        file_id: str,
        chat_id: int | None = None,
        reply_to: int | None = None,
        caption: str | None = None,
    ) -> DocumentToSend:
        ...

    @abc.abstractmethod
    def get_voice_to_send(
        self,
        file_id: str,
        chat_id: int | None = None,
        reply_to: int | None = None,
        caption: str | None = None,
    ) -> VoiceToSend:
        ...


class MessageToSend(abc.ABC):
    chat_id: int | None
    reply_to: int | None

    @abc.abstractmethod
    async def send(self, update: Update) -> None:
        ...


class TextToSend(MessageToSend):
    @abc.abstractmethod
    def __init__(
        self,
        message_content: list[str],
        markup: ReplyKeyboardMarkup
        | ReplyKeyboardRemove
        | InlineKeyboardMarkup
        | None = None,
        chat_id: int | None = None,
        reply_to: int | None = None,
        parse_mode: str | None = "Markdown",
    ) -> None:
        ...

    @abc.abstractmethod
    async def send(self, update: Update):
        ...


class FileToSend(MessageToSend):
    file_id: str


class ImageToSend(FileToSend):
    @abc.abstractmethod
    def __init__(
        self,
        file_id: str,
        chat_id: int | None = None,
        reply_to: int | None = None,
        caption: str | None = None,
    ):
        ...

    @abc.abstractmethod
    async def send(self, update: Update):
        ...


class VideoToSend(FileToSend):
    @abc.abstractmethod
    def __init__(
        self,
        file_id: str,
        chat_id: int | None = None,
        reply_to: int | None = None,
        caption: str | None = None,
    ):
        ...

    @abc.abstractmethod
    async def send(self, update: Update):
        ...


class AudioToSend(FileToSend):
    @abc.abstractmethod
    def __init__(
        self,
        file_id: str,
        chat_id: int | None = None,
        reply_to: int | None = None,
        caption: str | None = None,
    ):
        ...

    @abc.abstractmethod
    async def send(self, update: Update):
        ...


class DocumentToSend(FileToSend):
    @abc.abstractmethod
    def __init__(
        self,
        file_id: str,
        chat_id: int | None = None,
        reply_to: int | None = None,
        caption: str | None = None,
    ):
        ...

    @abc.abstractmethod
    async def send(self, update: Update):
        ...


class VoiceToSend(FileToSend):
    @abc.abstractmethod
    def __init__(
        self,
        file_id: str,
        chat_id: int | None = None,
        reply_to: int | None = None,
        caption: str | None = None,
    ):
        ...

    @abc.abstractmethod
    async def send(self, update: Update):
        ...
