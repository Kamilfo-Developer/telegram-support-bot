from telegram import Update


async def send_text_messages(
    messages: list[str],
    update: Update,
    parse_mode="html",
    chat_id: int | None = None,
    *args,
    **kwargs
):
    if chat_id:
        for message in messages:
            await update.get_bot().send_message(
                chat_id, message, *args, **kwargs, parse_mode="html"
            )
        return

    for message in messages:
        await update.message.reply_text(  # type: ignore
            message, *args, **kwargs, parse_mode="html"
        )
