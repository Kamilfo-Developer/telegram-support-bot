from typing import Type
from app.localization.en_messages_content import ENMessagesContent

#  from app.localization.en_messages_content import ENMessagesContent
from app.localization.messages_content import MessagesContent
from app.localization.ru_messages_content import RUMessagesContent
from app.shared.value_objects import TimezoneType


class MessagesContentFactory:
    def __init__(
        self,
        tz: TimezoneType,
        default_lang_code: str,
    ) -> None:
        self.default_lang_code = default_lang_code
        self.timezone = tz  # type: ignore
        self.__all_messages: dict[str, Type[MessagesContent]] = {
            "ru": RUMessagesContent,
            "en": ENMessagesContent,
        }

    def get_messages_content(self, lang_code: str) -> MessagesContent:
        MessagesContentClass: Type[
            MessagesContent
        ] | None = self.__all_messages.get(lang_code)

        if MessagesContentClass:
            return MessagesContentClass(self.timezone)  # type: ignore

        MessagesContentClass = self.__all_messages.get(self.default_lang_code)

        if not MessagesContentClass:
            raise ValueError(
                f"No messages for this DEFAULT_LANGUAGE_CODE: "
                f"{self.default_lang_code}"
            )

        return MessagesContentClass(self.timezone)  # type: ignore
