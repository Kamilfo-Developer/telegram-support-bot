from logging import (
    LogRecord,
    Logger,
    getLogger,
    INFO,
    WARNING,
    StreamHandler,
    Formatter,
)
from logging.handlers import QueueHandler, QueueListener
from queue import Queue

from app.loggers.logger import AppLogger


class LoggingAppLogger(AppLogger):
    LOGGIN_FORMAT = "%(asctime)s - %(levelname)-8s - %(name)-20s- %(message)s"

    def __init__(self) -> None:
        self.__set_other_loggers_levels()

        self.__logger = self.__init_logger()

    def __init_logger(self) -> Logger:
        logs_queue: Queue[LogRecord] = Queue(-1)  # no limit on size

        handler = StreamHandler()

        formatter = Formatter(self.LOGGIN_FORMAT)

        handler.setFormatter(formatter)

        listener = QueueListener(logs_queue, handler)

        listener.start()

        logger = getLogger()

        queue_handler = QueueHandler(logs_queue)

        logger.addHandler(queue_handler)

        logger.setLevel(INFO)

        logger.name = "application logger"

        return logger

    def __set_other_loggers_levels(self) -> None:
        ptb_logger = getLogger("telegram.ext.Application")
        ptb_logger.setLevel(INFO)
        ptb_logger.name = "python-telegram-bot"

        getLogger("httpx").setLevel(WARNING)

    async def info(self, message: str) -> None:
        self.__logger.info(message)

    async def warning(self, message: str) -> None:
        self.__logger.warning(message)

    async def error(self, message: str) -> None:
        self.__logger.error(message)

    async def critical(self, message: str) -> None:
        self.__logger.critical(message)

    async def fatal(self, message: str) -> None:
        self.__logger.fatal(message)
