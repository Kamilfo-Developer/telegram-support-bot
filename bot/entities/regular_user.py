from __future__ import annotations
from datetime import datetime
from typing import Iterable
from uuid import UUID, uuid4
from bot.entities.question import Question
from bot.typing import RepoType


class RegularUser:
    id: UUID
    tg_bot_user_id: int
    join_date: datetime

    def __init__(
        self,
        id: UUID,
        tg_bot_user_id: int,
        join_date: datetime = datetime.now(),
    ):
        self.id = id
        self.tg_bot_user_id = tg_bot_user_id
        self.join_date = join_date

    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, RegularUser) and self.id == __o.id

    async def ask_question(
        self,
        message: str,
        tg_message_id: int,
        repo: RepoType,
        question_date: datetime = datetime.now(),
    ) -> Question:
        question = Question(
            uuid4(), self, message, tg_message_id, date=question_date
        )

        await repo.add_question(question)

        return question

    async def get_asked_questions(self, repo: RepoType) -> Iterable[Question]:
        return await repo.get_questions_with_regular_user_id(self.id)

    @classmethod
    async def add_regular_user(
        cls, tg_bot_user_id: int, repo: RepoType
    ) -> RegularUser:
        regular_user = RegularUser(uuid4(), tg_bot_user_id, datetime.now())

        await repo.add_regular_user(regular_user)

        return regular_user
