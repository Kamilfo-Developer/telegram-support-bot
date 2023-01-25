from telegram import (
    Update,
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    ReplyKeyboardRemove,
)
from uuid import UUID


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


async def send_text_messages(
    message_to_send: MessageToSend, update: Update, *args, **kwargs
):
    messages = message_to_send.messages

    if len(messages) > 1:
        for message in messages[:-1]:
            await update.get_bot().send_message(
                message_to_send.chat_id or update.effective_chat.id,
                message,
                *args,
                **kwargs,
                parse_mode=message_to_send.parse_mode,
                reply_to_message_id=message_to_send.reply_to,  # type: ignore
            )

        await update.get_bot().send_message(
            message_to_send.chat_id or update.effective_chat.id,
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
            message_to_send.chat_id or update.effective_chat.id,
            message,
            *args,
            **kwargs,
            parse_mode=message_to_send.parse_mode,
            reply_to_message_id=message_to_send.reply_to,  # type: ignore
            reply_markup=message_to_send.markup,  # type: ignore
        )


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
