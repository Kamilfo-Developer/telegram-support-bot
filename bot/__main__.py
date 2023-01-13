from bot.init_db import init_sa_db
from bot.bot import app
from bot.db.db_sa_settings import engine, Base

import asyncio

loop = asyncio.new_event_loop()

loop.run_until_complete(init_sa_db(engine, Base))

loop.close()

app.run_polling()
