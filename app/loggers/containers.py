from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Dependency, Singleton

from app.config.app_config import AppSettings
from app.loggers.infra.logging_logger import LoggingAppLogger
from app.loggers.logger import AppLogger


def get_logger(app_settings: AppSettings) -> AppLogger:
    return LoggingAppLogger()


class LoggersContainer(DeclarativeContainer):
    app_settings = Dependency(AppSettings)

    app_logger: Singleton[AppLogger] = Singleton(get_logger, app_settings)
