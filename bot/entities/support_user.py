from __future__ import annotations
from datetime import datetime
from uuid import UUID, uuid4
from bot.typing import RepoType
from bot.entities.answer import Answer
from bot.entities.question import Question
from bot.entities.role import Role


class SupportUser:
    id: UUID
    current_question_id: UUID | None
    role_id: UUID | None
    tg_bot_user_id: int
    descriptive_name: str
    join_date: datetime = datetime.now()
    is_owner: bool = False

    def __init__(
        self,
        id: UUID,
        role_id: UUID | None,
        descriptive_name: str,
        tg_bot_user_id: int,
        current_question_id: UUID | None = None,
        join_date: datetime = datetime.now(),
        is_owner=False,
    ):
        self.id = id
        self.current_question_id = current_question_id
        self.role_id = role_id
        self.tg_bot_user_id = tg_bot_user_id
        self.descriptive_name = descriptive_name
        self.join_date = join_date
        self.is_owner = is_owner

    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, SupportUser) and self.id == __o.id

    async def answer_current_question(
        self, message: str, tg_message_id: int, repo: RepoType
    ) -> Answer | None:
        if self.current_question_id:
            answer = Answer(
                uuid4(),
                self.id,
                self.current_question_id,
                message,
                tg_message_id,
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

    async def get_current_question(self, repo: RepoType) -> Question | None:
        if self.current_question_id:
            return await repo.get_question_by_id(self.current_question_id)

        return None

    async def get_anwers(self, repo: RepoType) -> list[Answer]:
        return await repo.get_support_user_answers_with_id(self.id)

    async def get_role(self, repo: RepoType) -> Role | None:
        if self.role_id:
            return await repo.get_role_by_id(self.role_id)

        return None

    async def change_role(self, new_role_id: UUID, repo: RepoType) -> None:

        await repo.change_support_user_role(self.id, new_role_id)

        self.role_id = new_role_id

    async def bind_question(self, question_id: UUID, repo: RepoType) -> None:
        if question_id == self.current_question_id:
            return

        await repo.bind_question_to_support_user(self.id, question_id)

        self.current_question_id = question_id

    async def unbind_question(self, repo: RepoType) -> None:
        if not self.current_question_id:
            return

        await repo.unbind_question_from_support_user(self.id)

        self.current_question_id = None

    @classmethod
    async def add_support_user(
        cls,
        tg_bot_user_id: int,
        descriptive_name: str,
        repo: RepoType,
        role_id: UUID | None = None,
        is_owner: bool = False,
    ) -> SupportUser:

        support_user = SupportUser(
            id=uuid4(),
            role_id=role_id,
            tg_bot_user_id=tg_bot_user_id,
            descriptive_name=descriptive_name,
            is_owner=is_owner,
        )

        await repo.add_support_user(support_user)

        return support_user
