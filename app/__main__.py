from app.containers import AppContainer
import asyncio

app_container = AppContainer()

loop = asyncio.new_event_loop()

loop.create_task(app_container.bot_container().bot().run())

loop.run_forever()
