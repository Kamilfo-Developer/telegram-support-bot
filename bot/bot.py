from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler
from telegram.ext.filters import Text, ALL
import bot.handlers as handlers
from bot.settings import BOT_TOKEN
import logging

if not BOT_TOKEN:
    raise ValueError(
        "You must provide Telegram bot token. "
        + "You can get a token using this bot: https://t.me/botfather"
    )

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", handlers.handle_start))

app.add_handler(CommandHandler("getid", handlers.handle_get_id))

app.add_handler(CommandHandler("initowner", handlers.handle_init_owner))

app.add_handler(CommandHandler("getsupuser", handlers.handle_get_support_user))

app.add_handler(
    CommandHandler("getallsupusers", handlers.handle_get_all_suppurt_users)
)

app.add_handler(CommandHandler("getquestion", handlers.handle_get_question))

app.add_handler(CommandHandler("initowner", handlers.handle_init_owner))

app.add_handler(MessageHandler(Text(), handlers.handle_message))

app.add_handler(MessageHandler(ALL, handlers.handle_unsuppported_message_type))
