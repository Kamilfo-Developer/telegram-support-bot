from __future__ import annotations
from datetime import datetime
from typing import Iterable, Type
from uuid import UUID, uuid4
from bot.db.repositories.repository import Repo
from bot.entities.answer import Answer
from bot.entities.question import Question
from bot.entities.role import Role


class SupportUser:
    id: UUID
    current_question_id: UUID | None
    role_id: UUID
    tg_bot_user_id: int
    join_date: datetime = datetime.now()

    def __init__(
        self,
        id: UUID,
        role_id: UUID,
        tg_bot_user_id: int,
        current_question_id: UUID = None,
        join_date: datetime = datetime.now(),
    ):
        self.id = id
        self.current_question_id = current_question_id
        self.role_id = role_id
        self.tg_bot_user_id = tg_bot_user_id
        self.join_date = join_date

    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, SupportUser) and self.id == __o.id

    async def answer_current_question(
        self, message: str, tg_message_id: int, repo_class: Type[Repo]
    ) -> Answer | None:
        if self.current_question_id:
            answer = Answer(
                uuid4(),
                self.id,
                self.current_question_id,
                message,
                tg_message_id,
            )

            repo = repo_class()

            await repo.add_answer(answer)

            return answer

        return None

    async def get_current_question(
        self, repo_class: Type[Repo]
    ) -> Question | None:
        repo = repo_class()

        if self.current_question_id:
            return await repo.get_question_by_id(self.current_question_id)

        return None

    async def get_anwers(self, repo_class: Type[Repo]) -> Iterable[Answer]:
        repo = repo_class()

        return await repo.get_support_user_answers_with_id(self.id)

    async def get_role(self, repo_class: Type[Repo]) -> Role | None:
        repo = repo_class()

        if self.role_id:
            return await repo.get_role_by_id(self.role_id)

        return None

    async def change_role(
        self, new_role_id: UUID, repo_class: Type[Repo]
    ) -> None:
        repo = repo_class()

        await repo.change_support_user_role(self.id, new_role_id)

        self.role_id = new_role_id

    async def bind_question(
        self, question_id: UUID, repo_class: Type[Repo]
    ) -> None:
        repo = repo_class()

        await repo.bind_question_to_support_user(self.id, question_id)

        self.current_question_id = question_id

    async def unbind_question(self, repo_class: Type[Repo]) -> None:
        repo = repo_class()

        await repo.unbind_question_from_support_user(self.id)

        self.current_question_id = None

    @classmethod
    async def get_support_user_by_tg_bot_user_id(
        cls, tg_bot_user_id: int, repo_class: Type[Repo]
    ) -> SupportUser:
        repo = repo_class()

        return await repo.get_support_user_by_tg_bot_user_id(tg_bot_user_id)

    @classmethod
    async def add_support_user(
        cls, role_id: UUID, tg_bot_user_id: int, repo_class: Type[Repo]
    ) -> SupportUser:
        repo = repo_class()

        support_user = SupportUser(uuid4(), role_id, tg_bot_user_id)

        await repo.add_support_user(support_user)

        return support_user
