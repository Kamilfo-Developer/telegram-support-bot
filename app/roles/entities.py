from __future__ import annotations

from datetime import datetime
from typing import Self
from app.errors import SameValueAssigningError

from app.roles.value_objects import RoleDescription, RoleName
from app.shared.value_objects import NullRoleId, RoleIdType, RolePermissions
from app.utils import IdComparable


class Role(IdComparable):
    _id: RoleIdType

    name: RoleName

    description: RoleDescription

    permissions: RolePermissions

    created_date: datetime

    def __init__(
        self,
        role_id: RoleIdType,
        name: RoleName,
        description: RoleDescription,
        permissions: RolePermissions,
        created_date: datetime,
    ) -> None:
        """This method should not be called directly.
        Use ```Role.create(...)``` instead."""

        self._id = role_id

        self.name = name

        self.description = description

        self.permissions = permissions

        self.created_date = created_date

    def change_name(self, role_name: RoleName) -> None:
        """Changes name of the role.

        Args:
            role_name (RoleName): new role name

        Raises:
            SameValueAssigningError: raised if tried to assign the same name
        """

        if self.name == role_name:
            raise SameValueAssigningError()

        self.name = role_name

    def change_description(self, role_descrition: RoleDescription) -> None:
        """Changes description of the role.

        Args:
            role_descrition (RoleDescription): new role description

        Raises:
            SameValueAssigningError: raised if tried
            to assignd the same description
        """
        if self.description == role_descrition:
            raise SameValueAssigningError

        self.description = role_descrition

    def change_permissions(self, new_permissions: RolePermissions) -> None:
        """Changes permissions of the role.

        Args:
            new_permissions (RolePermissions): new role permissions

        Raises:
            SameValueAssigningError: raised if tried
            to assign the same permissions
        """

        if self.permissions == new_permissions:
            raise SameValueAssigningError()

        self.permissions = new_permissions

    @classmethod
    def create(
        cls,
        name: RoleName,
        description: RoleDescription,
        permissions: RolePermissions,
    ) -> Self:
        """A factory method which creates a new ```Role``` entity.

        The role's id is NullRoleId unless it's added to a repository.

        Args:
            name (str): role name
            description (str): role description
            permissions (RolePermissions): role permissions

        Returns:
            Self: new Role entity
        """
        return cls(
            role_id=NullRoleId(),
            name=name,
            description=description,
            permissions=permissions,
            created_date=datetime.now(),
        )
