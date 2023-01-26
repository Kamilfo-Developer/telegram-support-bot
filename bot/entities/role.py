from __future__ import annotations
from datetime import datetime
from bot.typing import RepoType


class Role:
    id: int

    name: str

    description: str

    date: datetime

    can_answer_questions: bool

    can_manage_support_users: bool

    created_date: datetime = datetime.now()

    def __init__(
        self,
        id: int,
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
        can_answer_questions: bool,
        can_manage_support_users: bool,
        repo: RepoType,
        description: str = "",
        adding_date: datetime = datetime.now(),
    ):
        role = Role(
            # If id equals to zero, it means that
            # the id must be created on the DB side
            id=0,
            name=name,
            description=description,
            can_answer_questions=can_answer_questions,
            can_manage_support_users=can_manage_support_users,
            created_date=adding_date,
        )

        return await repo.add_role(role)
