from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Dependency, Singleton

from app.bot.bot import Bot
from app.bot.bot_handlers import BotHandlers
from app.bot.bot_messages import MessagesToSendFactory
from app.bot.infra.ptb_bot import PTBBot
from app.bot.infra.ptb_messages import PTBMessagesToSendFactory
from app.bot.markup import MarkupProvider
from app.config.app_config import AppSettings
from app.localization.messages_content_factory import MessagesContentFactory
from app.loggers.logger import AppLogger
from app.regular_users.controller import RegularUserController
from app.support_users.controller import SupportUserController


def get_messages_content_factory(
    app_settings: AppSettings,
) -> MessagesContentFactory:
    return MessagesContentFactory(
        tz=app_settings.TIMEZONE,  # type: ignore
        default_lang_code=app_settings.DEFAULT_LANGUAGE_CODE,
    )


# Why this methods? Well, maybe I am gonna add aiogram support or something.
# You say: YAGNI, I say: YEP! BUT NOPE!
def get_bot(
    bot_handlers: BotHandlers, app_settings: AppSettings, app_logger: AppLogger
) -> Bot:
    return PTBBot(bot_handlers, app_settings, app_logger)


def get_messages_to_send_factory(
    app_settings: AppSettings,
) -> MessagesToSendFactory:
    return PTBMessagesToSendFactory()


def get_markup_provider(app_settings: AppSettings) -> MarkupProvider:
    return MarkupProvider()


class BotContainer(DeclarativeContainer):
    app_settings = Dependency(AppSettings)

    app_logger = Dependency(AppLogger)  # type: ignore

    support_user_controller = Dependency(SupportUserController)

    regular_user_controller = Dependency(RegularUserController)

    messages_content_factory: Singleton[MessagesContentFactory] = Singleton(
        get_messages_content_factory, app_settings=app_settings
    )

    messages_to_send_factory: Singleton[MessagesToSendFactory] = Singleton(
        get_messages_to_send_factory, app_settings=app_settings
    )

    markup_provider: Singleton[MarkupProvider] = Singleton(
        get_markup_provider, app_settings=app_settings
    )

    bot_handlers = Singleton(
        BotHandlers,
        msgs_content_factory=messages_content_factory,
        support_user_controller=support_user_controller,
        regular_user_controller=regular_user_controller,
        markup_provider=markup_provider,
        msgs_to_send_factory=messages_to_send_factory,
        app_settings=app_settings,
        app_logger=app_logger,
    )

    bot = Singleton(
        get_bot,
        bot_handlers=bot_handlers,
        app_settings=app_settings,
        app_logger=app_logger,
    )
