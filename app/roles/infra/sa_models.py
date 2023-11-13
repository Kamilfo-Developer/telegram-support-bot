from __future__ import annotations
from datetime import datetime
from typing import TYPE_CHECKING, Self
from sqlalchemy.orm import (
    relationship,
    Mapped,
    mapped_column,
)
from sqlalchemy import (
    DateTime,
    String,
    Boolean,
    Integer,
    Text,
)

from app.config.db_sa_config import ModelBase
from app.shared.dtos import RoleDTO


from app.roles.entities import Role
from app.roles.value_objects import RoleDescription, RoleName
from app.shared.value_objects import RoleIdType, RolePermissions


if TYPE_CHECKING:
    from app.support_users.infra.sa_models import SupportUserModel


class RoleModel(ModelBase):
    __tablename__ = "roles"

    # RELATIONSHIPS

    # Users relationship
    users = relationship("SupportUserModel", back_populates="role")

    # PROPERTIES

    id: Mapped[RoleIdType] = mapped_column(Integer, primary_key=True)

    name: Mapped[RoleName] = mapped_column(
        String(255), nullable=False, unique=True
    )

    description: Mapped[RoleDescription] = mapped_column(
        Text, nullable=False, default=""
    )

    created_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=datetime.utcnow
    )

    # If False a support user cannot use answering
    # questions interface
    can_answer_questions: Mapped[bool] = mapped_column(Boolean, default=True)

    # If False a support user cannot manage other support users and roles
    # Also they won't be able to get information about other support users
    can_manage_support_users: Mapped[bool] = mapped_column(
        Boolean, default=False
    )

    # METHODS

    @classmethod
    def from_entity(cls, role_entity: Role) -> Self:
        result = cls()

        if role_entity._id:
            result.id = role_entity._id

        result.name = role_entity.name
        result.description = role_entity.description
        result.can_answer_questions = (
            role_entity.permissions.can_answer_questions
        )
        result.can_manage_support_users = (
            role_entity.permissions.can_manage_support_users
        )
        result.created_date = role_entity.created_date

        return result

    def add_user(self, support_user: SupportUserModel):
        """Binds question to the support_user

        Should be commited using session.commit()

        Args:
            support_user (SupportUserModel): a user, which will be added
            to users with this role
        """
        self.users.append(support_user)

    def as_entity(self) -> Role:
        permissions = RolePermissions(
            self.can_answer_questions, self.can_manage_support_users
        )

        return Role(
            role_id=self.id,
            name=self.name,
            description=self.description,
            permissions=permissions,
            created_date=self.created_date,
        )

    def as_dto(self) -> RoleDTO:
        permissions = RolePermissions(
            self.can_answer_questions, self.can_manage_support_users
        )

        return RoleDTO(
            id=self.id,
            name=self.name,
            description=self.description,
            permissions=permissions,
            created_date=self.created_date,
        )
