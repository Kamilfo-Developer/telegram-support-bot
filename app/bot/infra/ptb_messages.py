from __future__ import annotations

from telegram import (
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    Update,
)

from app.bot.bot_messages import (
    AudioToSend,
    DocumentToSend,
    ImageToSend,
    MessagesToSendFactory,
    TextToSend,
    VideoToSend,
    VoiceToSend,
)


class PTBMessagesToSendFactory(MessagesToSendFactory):
    def __init__(self) -> None:
        pass

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
    ) -> PTBTextToSend:
        return PTBTextToSend(
            messages=messages,
            markup=markup,
            chat_id=chat_id,
            reply_to=reply_to,
            parse_mode=parse_mode,
        )

    def get_image_to_send(
        self,
        file_id: str,
        chat_id: int | None = None,
        reply_to: int | None = None,
        caption: str | None = None,
    ) -> PTBImageToSend:
        return PTBImageToSend(
            file_id=file_id,
            chat_id=chat_id,
            reply_to=reply_to,
            caption=caption,
        )

    def get_video_to_send(
        self,
        file_id: str,
        chat_id: int | None = None,
        reply_to: int | None = None,
        caption: str | None = None,
    ) -> PTBVideoToSend:
        return PTBVideoToSend(
            file_id=file_id,
            chat_id=chat_id,
            reply_to=reply_to,
            caption=caption,
        )

    def get_audio_to_send(
        self,
        file_id: str,
        chat_id: int | None = None,
        reply_to: int | None = None,
        caption: str | None = None,
    ) -> PTBAudioToSend:
        return PTBAudioToSend(
            file_id=file_id,
            chat_id=chat_id,
            reply_to=reply_to,
            caption=caption,
        )

    def get_document_to_send(
        self,
        file_id: str,
        chat_id: int | None = None,
        reply_to: int | None = None,
        caption: str | None = None,
    ) -> PTBDocumentToSend:
        return PTBDocumentToSend(
            file_id=file_id,
            chat_id=chat_id,
            reply_to=reply_to,
            caption=caption,
        )

    def get_voice_to_send(
        self,
        file_id: str,
        chat_id: int | None = None,
        reply_to: int | None = None,
        caption: str | None = None,
    ) -> PTBVoiceToSend:
        return PTBVoiceToSend(
            file_id=file_id,
            chat_id=chat_id,
            reply_to=reply_to,
            caption=caption,
        )


class PTBTextToSend(TextToSend):
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
    ) -> None:
        self.messages = messages
        self.markup = markup
        self.chat_id = chat_id
        self.reply_to = reply_to
        self.parse_mode = parse_mode

    async def send(self, update: Update):
        messages = self.messages

        if len(messages) > 1:
            for message in messages[:-1]:
                await update.get_bot().send_message(
                    self.chat_id or update.effective_chat.id,  # type: ignore
                    message,
                    parse_mode=self.parse_mode,
                    reply_to_message_id=self.reply_to,  # type: ignore
                )

            await update.get_bot().send_message(
                self.chat_id or update.effective_chat.id,  # type: ignore
                messages[-1],
                parse_mode=self.parse_mode,
                reply_to_message_id=self.reply_to,  # type: ignore
                reply_markup=self.markup,  # type: ignore
            )

            return

        for message in messages:
            await update.get_bot().send_message(
                self.chat_id or update.effective_chat.id,  # type: ignore
                message,
                parse_mode=self.parse_mode,
                reply_to_message_id=self.reply_to,  # type: ignore
                reply_markup=self.markup,  # type: ignore
            )


class PTBImageToSend(ImageToSend):
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


class PTBVideoToSend(VideoToSend):
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


class PTBAudioToSend(AudioToSend):
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


class PTBDocumentToSend(DocumentToSend):
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


class PTBVoiceToSend(VoiceToSend):
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
        await update.get_bot().send_voice(
            self.chat_id or update.effective_chat.id,  # type: ignore
            voice=self.file_id,
            reply_to_message_id=self.reply_to,  # type: ignore
        )
