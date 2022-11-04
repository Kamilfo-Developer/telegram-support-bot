from bot.settings import default_language_code
from bot.localization.messages import Messages
from bot.localization.en_messages import ENMessages
from bot.localization.ru_messages import RUMessages


def get_messages(lang_code: str) -> Messages:
    all_messages = {"en": ENMessages, "ru": RUMessages}

    messages = all_messages.get(lang_code)

    if messages:
        return messages()

    return all_messages[default_language_code]()
