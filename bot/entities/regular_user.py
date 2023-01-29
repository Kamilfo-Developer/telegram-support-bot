from __future__ import annotations
from datetime import datetime
from typing import Iterable
from uuid import UUID, uuid4
from bot.entities.question import Question
from bot.utils import IdComparable
from bot.typing import RepoType


class RegularUser(IdComparable):
    id: UUID
    tg_bot_user_id: int
    last_asked_question: Question | None
    join_date: datetime

    def __init__(
        self,
        id: UUID,
        tg_bot_user_id: int,
        last_asked_question: Question | None,
        join_date: datetime = datetime.now(),
    ):
        self.id = id
        self.tg_bot_user_id = tg_bot_user_id
        self.last_asked_question = last_asked_question
        self.join_date = join_date

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

        # TODO: Add new method for reposetory to
        # handle last asked quesion update

        await repo.add_question(question)

        self.last_asked_question = question

        return question

    async def get_asked_questions(self, repo: RepoType) -> Iterable[Question]:
        return await repo.get_questions_with_regular_user_id(self.id)

    @classmethod
    async def add_regular_user(
        cls, tg_bot_user_id: int, repo: RepoType
    ) -> RegularUser:
        regular_user = RegularUser(
            id=uuid4(),
            tg_bot_user_id=tg_bot_user_id,
            last_asked_question=None,
            join_date=datetime.now(),
        )

        await repo.add_regular_user(regular_user)

        return regular_user
