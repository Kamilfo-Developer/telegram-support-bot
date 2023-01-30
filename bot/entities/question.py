from __future__ import annotations
from datetime import datetime
from uuid import UUID
from bot.entities.question_attachment import QuestionAttachment
from bot.typing import Repo
from bot.utils import IdComparable

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bot.entities.answer import Answer
    from bot.entities.regular_user import RegularUser


class Question(IdComparable):
    id: UUID

    regular_user: RegularUser

    message: str

    tg_message_id: int

    date: datetime

    def __init__(
        self,
        id: UUID,
        regular_user: RegularUser,
        message: str,
        tg_message_id: int,
        date: datetime = datetime.now(),
    ):
        self.id = id
        self.regular_user = regular_user
        self.message = message
        self.tg_message_id = tg_message_id
        self.date = date

    async def get_attachments(self, repo: Repo) -> list[QuestionAttachment]:
        return await repo.get_question_attachments(self.id)

    async def get_answers(self, repo: Repo) -> list[Answer]:
        return await repo.get_answers_with_question_id(self.id)
