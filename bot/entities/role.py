from __future__ import annotations
from datetime import datetime
from bot.typing import Repo
from bot.utils import IdComparable
from bot.services.statistics import RoleStatistics


class Role(IdComparable):
    id: int

    name: str

    description: str

    permissions: RolePermissions

    created_date: datetime = datetime.now()

    def __init__(
        self,
        id: int,
        name: str,
        description: str,
        permissions: RolePermissions,
        created_date: datetime = datetime.now(),
    ) -> None:
        self.id = id
        self.name = name
        self.description = description

        self.permissions = permissions

        self.created_date = created_date

    async def get_support_users_with_this_role(self, repo: Repo):
        return await repo.get_support_users_with_role_id(self.id)

    async def get_statistics(self, repo: Repo) -> RoleStatistics:
        return await RoleStatistics.get_statistics(self.id, repo)

    @classmethod
    async def add_role(
        cls,
        name: str,
        permissions: RolePermissions,
        repo: Repo,
        description: str = "",
        adding_date: datetime = datetime.now(),
    ):
        role = Role(
            # If id equals to zero, it means that
            # the id must be created on the DB side
            id=0,
            name=name,
            description=description,
            permissions=permissions,
            created_date=adding_date,
        )

        return await repo.add_role(role)


class RolePermissions:
    can_answer_questions: bool
    can_manage_support_users: bool

    def __init__(
        self, can_answer_questions: bool, can_manage_support_users: bool
    ):
        self.can_answer_questions = can_answer_questions
        self.can_manage_support_users = can_manage_support_users
