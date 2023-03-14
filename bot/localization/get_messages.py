from bot.localization.messages_content import MessagesContent
from bot.localization.en_messages_content import ENMessagesContent
from bot.localization.ru_messages_content import RUMessagesContent
from datetime import timezone
from pytz.tzinfo import DstTzInfo, BaseTzInfo, StaticTzInfo
from typing import Type


def get_messages(
    lang_code: str,
    timezone: timezone | DstTzInfo | BaseTzInfo | StaticTzInfo,
    default_lang_code: str = "en",
) -> MessagesContent:
    all_messages: dict[str, Type[MessagesContent]] = {
        "ru": RUMessagesContent,
        "en": ENMessagesContent,
    }

    MessagesContentClass: Type[MessagesContent] | None = all_messages.get(
        lang_code
    )

    if MessagesContentClass:
        return MessagesContentClass(timezone)  # type: ignore

    MessagesContentClass = all_messages.get(default_lang_code)

    if not MessagesContentClass:
        raise ValueError(
            f"No messages for this DEFAULT_LANGUAGE_CODE: {default_lang_code}"
        )

    return MessagesContentClass(timezone)
