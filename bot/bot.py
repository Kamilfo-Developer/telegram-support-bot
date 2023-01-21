from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler
from telegram.ext.filters import Text, ALL, Command
import bot.handlers as handlers
from bot.settings import BOT_TOKEN
import logging

if not BOT_TOKEN:
    raise ValueError(
        "You must provide a Telegram bot token. "
        + "You can get a token using this bot: https://t.me/botfather"
    )

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", handlers.handle_start))

app.add_handler(CommandHandler("help", handlers.handle_help_command))

app.add_handler(CommandHandler("getid", handlers.handle_get_id))

app.add_handler(CommandHandler("initowner", handlers.handle_init_owner))

app.add_handler(CommandHandler("getsupuser", handlers.handle_get_support_user))

app.add_handler(
    CommandHandler("allsupusers", handlers.handle_get_all_suppurt_users)
)

app.add_handler(CommandHandler("question", handlers.handle_get_question))

app.add_handler(CommandHandler("initowner", handlers.handle_init_owner))

app.add_handler(CommandHandler("bind", handlers.handle_bind_question))

app.add_handler(CommandHandler("unbind", handlers.handle_unbind_question))

app.add_handler(CommandHandler("addsupuser", handlers.handle_add_support_user))

app.add_handler(
    CommandHandler("getallsups", handlers.handle_get_all_suppurt_users)
)

app.add_handler(CommandHandler("answer", handlers.handle_get_answer))

app.add_handler(CommandHandler("addrole", handlers.handle_add_role))

app.add_handler(CommandHandler("role", handlers.handle_get_role))

app.add_handler(
    MessageHandler(Command(False), handlers.handle_unknown_command)
)


app.add_handler(MessageHandler(Text(), handlers.handle_message))

app.add_handler(MessageHandler(ALL, handlers.handle_unsuppported_message_type))
