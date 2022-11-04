from __future__ import annotations
from datetime import datetime
from typing import Iterable, Type
from uuid import UUID
from bot.db.repositories.repository import Repo

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bot.entities.answer import Answer
    from bot.entities.regular_user import RegularUser


class Question:
    id: UUID

    regular_user_id: UUID

    message: str

    tg_message_id: int

    date: datetime

    def __init__(
        self,
        id: UUID,
        regular_user_id: UUID,
        message: str,
        tg_message_id: int,
        date: datetime = datetime.now(),
    ):
        self.id = id
        self.regular_user_id = regular_user_id
        self.message = message
        self.tg_message_id = tg_message_id
        self.date = date

    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, Question) and self.id == __o.id

    async def get_regular_user_asked(
        self, repo_class: Type[Repo]
    ) -> RegularUser:
        repo = repo_class()

        return await repo.get_regular_user_by_id(self.regular_user_id)

    async def get_question_answers(
        self, repo_class: Type[Repo]
    ) -> Iterable[Answer]:
        repo = repo_class()

        return await repo.get_answers_with_question_id(self.id)
