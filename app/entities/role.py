from __future__ import annotations
from datetime import datetime
from typing import Self
from app.utils import IdComparable, RoleIdType


class Role(IdComparable):
    _id: RoleIdType | None

    name: str

    description: str

    permissions: RolePermissions

    created_date: datetime

    def __init__(
        self,
        role_id: RoleIdType | None,
        name: str,
        description: str,
        permissions: RolePermissions,
        created_date: datetime,
    ) -> None:
        self._id = role_id

        self.name = name

        self.description = description

        self.permissions = permissions

        self.created_date = created_date

    @classmethod
    def create(
        cls,
        name: str,
        description: str,
        permissions: RolePermissions,
    ) -> Self:
        """Factory method which creates a new Role.

        The role's id is None unless it's added to a repository

        Args:
            name (str): name
            description (str): role description
            permissions (RolePermissions): role permissions

        Returns:
            Role: an instance of the class with id equal to None
        """
        return cls(
            role_id=None,
            name=name,
            description=description,
            permissions=permissions,
            created_date=datetime.now(),
        )


class RolePermissions:
    can_answer_questions: bool
    can_manage_support_users: bool

    def __init__(
        self, can_answer_questions: bool, can_manage_support_users: bool
    ) -> None:
        self.can_answer_questions = can_answer_questions
        self.can_manage_support_users = can_manage_support_users
