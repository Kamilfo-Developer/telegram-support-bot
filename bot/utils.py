from telegram import Update
from telegram.error import BadRequest
from uuid import UUID


async def send_text_messages(
    messages: list[str],
    update: Update,
    parse_mode="MarkDown",
    chat_id: int | None = None,
    reply_to_message_id: int | None = None,
    *args,
    **kwargs
):
    if chat_id:
        for message in messages:
            await update.get_bot().send_message(
                chat_id,
                message,
                *args,
                **kwargs,
                parse_mode=parse_mode,
                reply_to_message_id=reply_to_message_id,  # type: ignore
            )

        return

    for message in messages:
        await update.message.reply_text(  # type: ignore
            message, *args, **kwargs, parse_mode=parse_mode
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
