from bot.localization.messages import Messages
from bot.entities.support_user import SupportUser
from bot.entities.regular_user import RegularUser
from bot.entities.question_attachment import QuestionAttachment
from bot.entities.question import Question
from bot.markup import Markup
from bot.typing import Repo
from telegram import User
from datetime import datetime
from bot.utils import MessageToSend, AttachmentType, ImageToSend, VideoToSend


class RegularUserManager:
    def __init__(
        self,
        tg_user: User,
        regular_user: RegularUser | None,
        messages: Messages,
        repo: Repo,
    ):
        self.tg_user = tg_user
        self.regular_user = regular_user
        self.messages = messages
        self.repo = repo
        self.markup = Markup(messages)

    async def ask_question(
        self, question_text: str, message_id: int, message_date: datetime
    ) -> MessageToSend:
        if not self.is_regular_user_authorized():
            return MessageToSend(
                await self.messages.get_regular_user_not_authorized_message()
            )

        question = await self.regular_user.ask_question(  # type: ignore
            question_text, message_id, self.repo, message_date
        )

        return MessageToSend(
            await self.messages.get_successful_asking_message(question),
            reply_to=message_id,
        )

    async def estimate_answer_as_useful(
        self, answer_tg_message_id: int
    ) -> MessageToSend:
        if not self.is_regular_user_authorized():
            return MessageToSend(
                await self.messages.get_regular_user_not_authorized_message()
            )

        answer = await self.repo.get_answer_by_tg_message_id(
            answer_tg_message_id
        )

        if not answer:
            return MessageToSend(
                await self.messages.get_no_object_with_this_id_message(
                    str(answer_tg_message_id)
                )
            )

        if answer.is_useful is not None:
            return MessageToSend(
                await self.messages.get_answer_already_estimated_message(
                    answer
                )
            )

        await answer.estimate_as_useful(self.repo)

        return MessageToSend(
            await self.messages.get_answer_estimated_as_useful_message(answer)
        )

    async def estimate_answer_as_unuseful(
        self, answer_tg_message_id: int
    ) -> MessageToSend:
        if not self.is_regular_user_authorized():
            return MessageToSend(
                await self.messages.get_regular_user_not_authorized_message()
            )

        answer = await self.repo.get_answer_by_tg_message_id(
            answer_tg_message_id
        )

        if not answer:
            return MessageToSend(
                await self.messages.get_no_object_with_this_id_message(
                    str(answer_tg_message_id)
                )
            )

        if answer.is_useful is not None:
            return MessageToSend(
                await self.messages.get_answer_already_estimated_message(
                    answer
                )
            )

        await answer.estimate_as_unuseful(self.repo)

        return MessageToSend(
            await self.messages.get_answer_estimated_as_unuseful_message(
                answer
            )
        )

    async def add_attachment_to_last_asked_question(
        self, tg_file_id: str, attachment_type: AttachmentType, date: datetime
    ) -> MessageToSend:
        if not self.is_regular_user_authorized():
            return MessageToSend(
                await self.messages.get_regular_user_not_authorized_message()
            )

        last_question = await self.repo.get_regular_user_last_asked_question(
            self.regular_user.id
        )

        if not last_question:
            return MessageToSend(
                await self.messages.get_no_last_asked_question_message(
                    self.regular_user
                )
            )

        await last_question.add_attachment(
            tg_file_id, attachment_type, date, self.repo
        )

        return MessageToSend(
            await self.messages.get_question_attachment_addition_message(
                self.regular_user
            )
        )

    def is_regular_user_authorized(self) -> bool:
        if not self.regular_user:
            return False

        return True
