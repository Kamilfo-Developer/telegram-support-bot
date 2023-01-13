from __future__ import annotations
from datetime import datetime
from uuid import UUID, uuid4
from bot.typing import RepoType


class Role:
    id: UUID

    name: str

    description: str

    date: datetime

    can_answer_questions: bool

    can_manage_support_users: bool

    created_date: datetime = datetime.now()

    def __init__(
        self,
        id: UUID,
        name: str,
        description: str,
        can_answer_questions: bool,
        can_manage_support_users: bool,
        created_date: datetime = datetime.now(),
    ) -> None:
        self.id = id
        self.name = name
        self.description = description

        self.can_answer_questions = can_answer_questions
        self.can_manage_support_users = can_manage_support_users
        self.created_date = created_date

    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, Role) and self.id == __o.id

    async def get_support_users_with_this_role(self, repo: RepoType):
        return await repo.get_support_users_with_role_id(self.id)

    @classmethod
    async def add_role(
        cls,
        name: str,
        description: str,
        can_answer_questions: bool,
        can_manage_support_users: bool,
        repo: RepoType,
    ):
        role = Role(
            id=uuid4(),
            name=name,
            description=description,
            can_answer_questions=can_answer_questions,
            can_manage_support_users=can_manage_support_users,
        )

        await repo.add_role(role)

        return role
