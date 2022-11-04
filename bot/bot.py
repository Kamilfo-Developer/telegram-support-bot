from telegram.ext import ApplicationBuilder, CommandHandler
from bot.handlers import handle_start, handle_get_id
import logging

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

app = ApplicationBuilder().token("").build()

app.add_handler(CommandHandler("start", handle_start))

app.add_handler(CommandHandler("getid", handle_get_id))
