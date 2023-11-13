import abc
from typing import NoReturn
from app.bot.bot_handlers import BotHandlers
from app.config.app_config import AppSettings
from app.loggers.logger import AppLogger


class Bot(abc.ABC):
    @abc.abstractmethod
    def __init__(
        self,
        bot_handlers: BotHandlers,
        app_settings: AppSettings,
        app_logger: AppLogger,
    ):
        ...

    @abc.abstractmethod
    def run(self) -> NoReturn:
        """Runs the bot.

        Returns:
            NoReturn: this method will run forever
        """
        ...
