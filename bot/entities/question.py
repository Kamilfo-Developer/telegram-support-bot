from __future__ import annotations
from datetime import datetime
from uuid import UUID
from bot.typing import RepoType

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bot.entities.answer import Answer
    from bot.entities.regular_user import RegularUser


class Question:
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

    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, Question) and self.id == __o.id

    async def get_question_answers(self, repo: RepoType) -> list[Answer]:

        return await repo.get_answers_with_question_id(self.id)
