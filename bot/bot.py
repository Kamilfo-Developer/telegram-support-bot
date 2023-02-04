from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
)
from telegram.ext.filters import (
    Text,
    ALL,
    Command,
    PHOTO,
    VIDEO,
    AUDIO,
    VOICE,
    Document,
)
import bot.handlers as handlers
from bot.settings import BOT_TOKEN
from bot.states import States
import json
import logging

if not BOT_TOKEN:
    raise EnvironmentError(
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

app.add_handler(CommandHandler("supuser", handlers.handle_get_support_user))

app.add_handler(
    CommandHandler("supusers", handlers.handle_get_all_suppurt_users)
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

app.add_handler(
    CommandHandler("answers", handlers.handle_get_question_answers)
)

app.add_handler(CommandHandler("addrole", handlers.handle_add_role))

app.add_handler(CommandHandler("role", handlers.handle_get_role))

app.add_handler(CommandHandler("roles", handlers.handle_get_all_roles))

app.add_handler(
    CommandHandler("activatesupuser", handlers.handle_activate_support_user)
)

app.add_handler(
    CommandHandler(
        "deactivatesupuser", handlers.handle_deactivate_support_user
    )
)


app.add_handler(
    CallbackQueryHandler(
        handlers.handle_bind_question_button,
        lambda x: (
            json.loads(x)["action"] == States.BIND_ACTION  # type: ignore
        ),
    )
)

app.add_handler(
    CallbackQueryHandler(
        handlers.handle_unbind_question_button,
        lambda x: (
            json.loads(x)["action"] == States.UNBIND_ACTION  # type: ignore
        ),
    )
)

app.add_handler(
    CallbackQueryHandler(
        handlers.handle_estimate_question_as_useful_button,
        lambda x: (
            json.loads(x)["action"]  # type: ignore
            == States.ESTIMATE_AS_USEFUL_ACTION
        ),
    )
)

app.add_handler(
    CallbackQueryHandler(
        handlers.handle_estimate_question_as_unuseful_button,
        lambda x: (
            json.loads(x)["action"]  # type: ignore
            == States.ESTIMATE_AS_UNUSEFUL_ACTION
        ),
    )
)

app.add_handler(
    CallbackQueryHandler(
        handlers.handle_show_attachments_button,
        lambda x: (
            json.loads(x)["action"] == States.SHOW_ATTACHMENTS_ACTION  # type: ignore
        ),
    )
)

app.add_handler(
    MessageHandler(Command(False), handlers.handle_unknown_command)
)

app.add_handler(
    MessageHandler(
        PHOTO | VIDEO | AUDIO | VOICE | Document.ALL, handlers.handle_file
    )
)

app.add_handler(MessageHandler(Text(), handlers.handle_message))

app.add_handler(MessageHandler(ALL, handlers.handle_unsuppported_message_type))
