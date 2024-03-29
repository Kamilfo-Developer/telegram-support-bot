from __future__ import annotations
from datetime import datetime
from typing import Iterable
from uuid import UUID, uuid4
from bot.entities.question import Question
from bot.utils import IdComparable
from bot.typing import Repo
from bot.services.statistics import RegularUserStatistics


class RegularUser(IdComparable):
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

    async def ask_question(
        self,
        message: str,
        tg_message_id: int,
        repo: Repo,
        question_date: datetime = datetime.now(),
    ) -> Question:
        question = Question(
            uuid4(), self, message, tg_message_id, date=question_date
        )

        await repo.add_question(question)

        return question

    async def get_asked_questions(self, repo: Repo) -> Iterable[Question]:
        return await repo.get_questions_with_regular_user_id(self.id)

    async def get_last_asked_question(self, repo: Repo) -> Question | None:
        return await repo.get_regular_user_last_asked_question(self.id)

    async def get_statistics(self, repo: Repo) -> RegularUserStatistics:
        return await RegularUserStatistics.get_statistics(self.id, repo)

    @classmethod
    async def add_regular_user(
        cls, tg_bot_user_id: int, repo: Repo
    ) -> RegularUser:
        regular_user = RegularUser(
            id=uuid4(),
            tg_bot_user_id=tg_bot_user_id,
            join_date=datetime.now(),
        )

        await repo.add_regular_user(regular_user)

        return regular_user
