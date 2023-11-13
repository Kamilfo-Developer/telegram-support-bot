from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from app.localization.messages_content import MessagesContent


class MarkupProvider:
    def __init__(self) -> None:
        pass

    def get_question_info_buttons_markup(
        self,
        bind_button_callback_data: str,
        unbind_button_callback_data: str,
        show_attachments_button_callback_data: str,
        messages_content: MessagesContent,
    ) -> InlineKeyboardMarkup:
        inline_keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        messages_content.bind_question_button_text,
                        callback_data=bind_button_callback_data,
                    ),
                    InlineKeyboardButton(
                        messages_content.unbind_question_button_text,
                        callback_data=unbind_button_callback_data,
                    ),
                ],
                [
                    InlineKeyboardButton(
                        messages_content.show_attachments_button_text,
                        callback_data=show_attachments_button_callback_data,
                    ),
                ],
            ]
        )

        return inline_keyboard

    def get_answer_estimation_buttons_markup(
        self,
        useful_answer_button_callback_data: str,
        unuseful_answer_button_callback_data: str,
        messages_content: MessagesContent,
    ) -> InlineKeyboardMarkup:
        inline_keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        messages_content.estimate_answer_as_useful_button_text,
                        callback_data=useful_answer_button_callback_data,
                    ),
                ],
                [
                    InlineKeyboardButton(
                        messages_content.estimate_answer_as_unuseful_button_text,  # noqa: E501
                        callback_data=unuseful_answer_button_callback_data,
                    ),
                ],
            ]
        )

        return inline_keyboard
