from __future__ import annotations
from datetime import datetime
from typing import Iterable, Type
from uuid import UUID, uuid4
from bot.db.repositories.repository import Repo
from bot.entities.question import Question


class RegularUser:
    id: UUID
    tg_bot_user_id: int

    def __init__(self, id: UUID, tg_bot_user_id: int, join_date: datetime):
        self.id = id
        self.tg_bot_user_id = tg_bot_user_id
        self.join_date = join_date

    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, RegularUser) and self.id == __o.id

    async def ask_question(
        self, message: str, tg_message_id: int, repo_class: Type[Repo]
    ) -> Question:
        repo = repo_class()

        question = Question(uuid4(), self.id, message, tg_message_id)

        await repo.add_question(question)

        return question

    async def get_asked_questions(
        self, repo_class: Type[Repo]
    ) -> Iterable[Question]:
        repo = repo_class()

        return await repo.get_questions_with_regular_user_id(self.id)

    @classmethod
    async def get_regular_user_by_tg_bot_user_id(
        cls, tg_bot_user_id: int, repo_class: Type[Repo]
    ) -> RegularUser:
        repo = repo_class()

        return await repo.get_regular_user_by_tg_bot_user_id(tg_bot_user_id)
