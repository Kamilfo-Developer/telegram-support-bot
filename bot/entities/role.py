from __future__ import annotations
from datetime import datetime
from typing import Type
from uuid import UUID

from bot.db.repositories.repository import Repo


class Role:
    id: UUID

    name: str

    description: str

    date: datetime

    can_answer_questions: bool

    can_create_roles: bool
    can_romove_roles: bool
    can_change_roles: bool
    can_assign_roles: bool

    created_date: datetime = datetime.now()

    def __init__(
        self,
        id: UUID,
        name: str,
        description: str,
        can_answer_questions: bool,
        can_create_roles: bool,
        can_romove_roles: bool,
        can_change_roles: bool,
        can_assign_roles: bool,
        created_date: datetime = datetime.now(),
    ) -> None:
        self.id = id
        self.name = name
        self.description = description

        self.can_answer_questions = can_answer_questions
        self.can_assign_roles = can_assign_roles
        self.can_change_roles = can_change_roles
        self.can_create_roles = can_create_roles
        self.can_romove_roles = can_romove_roles
        self.created_date = created_date

    def __eq__(self, __o: object) -> bool:
        return isinstance(__o, Role) and self.id == __o.id

    async def get_support_users_with_this_role(self, repo_class: Type[Repo]):
        repo = repo_class()

        return await repo.get_support_users_with_role_id(self.id)
