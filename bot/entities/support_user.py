from __future__ import annotations
from datetime import datetime
from uuid import UUID, uuid4
from bot.typing import RepoType
from bot.entities.answer import Answer
from bot.entities.question import Question
from bot.entities.role import Role


class SupportUser:
    id: UUID
    current_question: Question | None
    role: Role | None
    tg_bot_user_id: int
    descriptive_name: str
    join_date: datetime = datetime.now()
    is_owner: bool = False

    def __init__(
        self,
        id: UUID,
        descriptive_name: str,
        tg_bot_user_id: int,
        role: Role | None = None,
        current_question: Question | None = None,
        join_date: datetime = datetime.now(),
        is_owner: bool = False,
        is_active: bool = True,
    ):
        self.id = id
        self.current_question = current_question
        self.role = role
        self.tg_bot_user_id = tg_bot_user_id
        self.descriptive_name = descriptive_name
        self.join_date = join_date
        self.is_owner = is_owner
        self.is_active = is_active

    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, SupportUser) and self.id == __o.id

    async def answer_current_question(
        self,
        message: str,
        tg_message_id: int,
        repo: RepoType,
        answer_date: datetime = datetime.now(),
    ) -> Answer | None:
        if self.current_question:
            answer = Answer(
                uuid4(),
                self,
                self.current_question,
                message,
                tg_message_id,
                date=answer_date,
            )

            await repo.add_answer(answer)

            return answer

        return None

    async def make_owner(self, repo: RepoType) -> None:
        if self.is_owner:
            return

        await repo.make_support_user_owner(self.id)

        self.is_owner = True

    async def remove_owner_rights(self, repo: RepoType) -> None:
        if not self.is_owner:
            return

        await repo.remove_owner_rights_from_support_user(self.id)

        self.is_owner = False

    async def get_anwers(self, repo: RepoType) -> list[Answer]:
        return await repo.get_support_user_answers_with_id(self.id)

    async def change_role(self, new_role: Role, repo: RepoType) -> None:

        await repo.change_support_user_role(self.id, new_role.id)

        self.role = new_role

    async def bind_question(self, question: Question, repo: RepoType) -> None:
        if question == self.current_question:
            return

        await repo.bind_question_to_support_user(self.id, question.id)

        self.current_question = question

    async def unbind_question(self, repo: RepoType) -> None:
        if not self.current_question:
            return

        await repo.unbind_question_from_support_user(self.id)

        self.current_question = None

    async def deactivate(self, repo: RepoType) -> None:
        if not self.is_active:
            return

        await self.unbind_question(repo)

        await repo.deactivate_support_user(self.id)

        self.is_active = False

    async def activate(self, repo: RepoType) -> None:
        if self.is_active:
            return

        await repo.activate_support_user(self.id)

        self.is_active = True

    @classmethod
    async def add_support_user(
        cls,
        tg_bot_user_id: int,
        descriptive_name: str,
        repo: RepoType,
        role: Role | None = None,
        is_owner: bool = False,
        addition_time: datetime = datetime.now(),
    ) -> SupportUser:

        support_user = SupportUser(
            id=uuid4(),
            role=role,
            tg_bot_user_id=tg_bot_user_id,
            descriptive_name=descriptive_name,
            is_owner=is_owner,
            join_date=addition_time,
            is_active=True,
        )

        await repo.add_support_user(support_user)

        return support_user
