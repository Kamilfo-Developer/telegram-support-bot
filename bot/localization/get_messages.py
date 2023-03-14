from bot.localization.messages import Messages
from bot.localization.en_messages import ENMessages
from bot.localization.ru_messages import RUMessages
from datetime import timezone
from pytz.tzinfo import DstTzInfo, BaseTzInfo, StaticTzInfo
from typing import Type


def get_messages(
    lang_code: str,
    timezone: timezone | DstTzInfo | BaseTzInfo | StaticTzInfo,
    default_lang_code: str = "en",
) -> Messages:
    all_messages = {"ru": RUMessages, "en": ENMessages}

    MessagesClass: Type[Messages] | None = all_messages.get(lang_code)

    if MessagesClass:
        return MessagesClass(timezone)  # type: ignore

    MessagesClass = all_messages.get(default_lang_code)

    if not MessagesClass:
        raise ValueError(
            f"No messages for this DEFAULT_LANGUAGE_CODE: {default_lang_code}"
        )

    return MessagesClass(timezone)
