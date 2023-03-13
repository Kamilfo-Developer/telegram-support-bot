from bot.settings import DEFAULT_LANGUAGE_CODE, TIMEZONE
from bot.localization.messages import Messages
from bot.localization.en_messages import ENMessages
from bot.localization.ru_messages import RUMessages


def get_messages(lang_code: str) -> Messages:
    all_messages = {"ru": RUMessages, "en": ENMessages}

    MessagesClass = all_messages.get(lang_code)

    if MessagesClass:
        return MessagesClass(TIMEZONE)  # type: ignore

    MessagesClass = all_messages.get(DEFAULT_LANGUAGE_CODE)

    if not MessagesClass:
        raise ValueError(
            f"No messages for this DEFAULT_LANGUAGE_CODE: {DEFAULT_LANGUAGE_CODE}"
        )

    return MessagesClass(TIMEZONE)  # type: ignore
