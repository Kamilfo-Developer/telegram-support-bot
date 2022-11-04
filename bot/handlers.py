from bot.entities.regular_user import RegularUser
from bot.settings import repository

from bot.entities.support_user import SupportUser
from bot.localization.get_messages import get_messages


async def handle_start(update, context):

    user = update.effective_user
    repo = repository()

    messages = get_messages(user.language_code)

    regular_user = RegularUser.get_regular_user_by_tg_bot_user_id(
        user.id, repo
    )

    if regular_user:
        start_messages = await messages.get_start_reg_user_message(user, None)

        for message in start_messages:
            await update.message.reply_text(message, parse_mode="html")

        return

    support_user = SupportUser.get_support_user_by_tg_bot_user_id(
        user.id, repo
    )

    if support_user:
        start_messages = await messages.get_start_sup_user_message(user)

        for message in start_messages:
            await update.message.reply_text(message, parse_mode="html")

        return


async def handle_get_id(update, context):
    messages = get_messages(update.effective_user.language_code)

    get_id_messages = await messages.get_start_reg_user_message(
        update.effective_user, None
    )

    for message in get_id_messages:
        await update.message.reply_text(message, parse_mode="html")


async def get_sup_user(update, context):
    repo = repository()

    try:
        id = int(context.args[0])

        await SupportUser.get_support_user_by_tg_bot_user_id(id, repo)

    except ValueError:
        await update.message.reply_text(
            "Incorrect id. Value should be an integer.\nFor example 531673"
        )

    await update.message.reply_text()
