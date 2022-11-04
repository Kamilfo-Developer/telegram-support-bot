from __future__ import annotations
from datetime import datetime
from typing import Type
from uuid import UUID
from bot.db.repositories.repository import Repo

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bot.entities.question import Question
    from bot.entities.support_user import SupportUser


class Answer:
    id: UUID
    support_user_id: UUID
    question_id: UUID
    message: str
    tg_message_id: int
    date: datetime

    def __init__(
        self,
        id: UUID,
        support_user_id: UUID,
        question_id: UUID,
        message: str,
        tg_message_id: int,
        date: datetime = datetime.now(),
    ):
        self.id = id
        self.support_user_id = support_user_id
        self.question_id = question_id
        self.message = message
        self.tg_message_id = tg_message_id
        self.date = date

    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, Answer) and self.id == __o.id

    async def get_support_user(self, repo_class: Type[Repo]) -> SupportUser:
        repo = repo_class()

        return await repo.get_support_user_by_id(self.support_user_id)

    async def get_question(self, repo_class: Type[Repo]) -> Question:
        repo = repo_class()

        return await repo.get_question_by_id(self.question_id)
