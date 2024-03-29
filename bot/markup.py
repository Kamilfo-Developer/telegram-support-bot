from bot.localization.messages_content import MessagesContent
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


class Markup:
    def __init__(self, messages_content: MessagesContent):
        self.msgs = messages_content

    def get_question_info_buttons_markup(
        self,
        bind_button_callback_data: str,
        unbind_button_callback_data: str,
        show_attachments_button_callback_data: str,
    ) -> InlineKeyboardMarkup:
        inline_keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        self.msgs.bind_question_button_text,
                        callback_data=bind_button_callback_data,
                    ),
                    InlineKeyboardButton(
                        self.msgs.unbind_question_button_text,
                        callback_data=unbind_button_callback_data,
                    ),
                ],
                [
                    InlineKeyboardButton(
                        self.msgs.show_attachments_button_text,
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
    ) -> InlineKeyboardMarkup:
        inline_keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        self.msgs.estimate_answer_as_useful_button_text,
                        callback_data=useful_answer_button_callback_data,
                    ),
                ],
                [
                    InlineKeyboardButton(
                        self.msgs.estimate_answer_as_unuseful_button_text,
                        callback_data=unuseful_answer_button_callback_data,
                    ),
                ],
            ]
        )

        return inline_keyboard
