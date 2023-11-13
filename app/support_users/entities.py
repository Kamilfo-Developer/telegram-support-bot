from __future__ import annotations
from datetime import datetime
from typing import Self
from uuid import uuid4
from app.errors import (
    IncorrectActionError,
    SameValueAssigningError,
)
from app.support_users.value_objects import DescriptiveName
from app.shared.value_objects import (
    QuestionIdType,
    RoleIdType,
    RolePermissions,
    SupportUserIdType,
    TgUserId,
)
from app.utils import IdComparable


class SupportUser(IdComparable):
    _id: SupportUserIdType
    current_question_id: QuestionIdType | None
    role: SupportUserRole | None
    tg_bot_user_id: TgUserId
    descriptive_name: DescriptiveName
    join_date: datetime
    is_active: bool
    is_owner: bool

    def __init__(
        self,
        id: SupportUserIdType,
        descriptive_name: DescriptiveName,
        tg_bot_user_id: TgUserId,
        role: SupportUserRole | None,
        current_question_id: QuestionIdType | None,
        join_date: datetime,
        is_active: bool,
        is_owner: bool,
    ) -> None:
        """This method should not be called directly.
        Use ```SupportUser.create(...)``` instead."""

        self._id = id
        self.current_question_id = current_question_id
        self.role = role
        self.tg_bot_user_id = tg_bot_user_id
        self.descriptive_name = descriptive_name
        self.join_date = join_date
        self.is_owner = is_owner
        self.is_active = is_active

    def promote_to_owner(self) -> None:
        """Promotes this user to owner.

        Raises:
            IncorrectActionError: raised if the user already is an Owner
        """

        if self.is_owner:
            raise IncorrectActionError("An Owner cannot be promoted to owner")

        self.is_owner = True
        self.role = None

    def remove_owner_rights(self) -> None:
        """Removes owner rigts from the support user.

        Raises:
            IncorrectActionError: raise if the user have no Owner rights
        """

        if not self.is_owner:
            raise IncorrectActionError(
                "Can remove Owner's rights only from an owner"
            )

        self.is_owner = False

    def assign_role(self, new_role: SupportUserRole) -> None:
        """Assignes a new role to the support user.

        Args:
            new_role (SupportUserRole): new role to be assigned

        Raises:
            IncorrectActionError: raise if this support user has Owner rights
            SameValueAssigningError: raised if tried to assign the same role
        """

        if self.is_owner:
            raise IncorrectActionError("Cannot assign role to owner")

        if self.role == new_role:
            raise SameValueAssigningError()

        self.role = new_role

        if not new_role.permissions.can_answer_questions:
            self.current_question_id = None

    def remove_role(self) -> None:
        """Removes role from the support user.

        Raises:
            IncorrectActionError: raised if tried to remove role from an owner
            SameValueAssigningError: raised if the support useralready has
            no role
        """

        if self.is_owner:
            raise IncorrectActionError(
                "Cannot remove roles from owners since they don't have any"
            )

        if self.role is None:
            raise SameValueAssigningError(
                "This Support User already has no role"
            )

        self.role = None
        self.current_question_id = None

    def bind_question(self, question_id: QuestionIdType) -> None:
        """Binds question with ```question_id``` to this support_user.

        Args:
            question_id (QuestionIdType): id of the question to bind

        Raises:
            IncorrectActionError: raised if the support user has
            no rights to answer questions
            SameValueAssigningError: raised if tried to bind the same question
        """

        if not self.can_answer_questions():
            raise IncorrectActionError("Not enough rights to answer questions")

        if self.current_question_id == question_id:
            raise SameValueAssigningError(
                "Cannot bind the same question twice"
            )

        self.current_question_id = question_id

    def unbind_question(self) -> None:
        """Unbinds question.

        Raises:
            IncorrectActionError: raised if the support user has
            no rights to answer questions.
            SameValueAssigningError: raised if tried to unbind question
            when there is no bound question
        """
        if not self.can_answer_questions():
            raise IncorrectActionError(
                "This Support User cannot unbind question since "
                "they are not allowed to answer questions"
            )

        if not self.current_question_id:
            raise SameValueAssigningError(
                "Cannot unbind question if there is no bound question"
            )

        self.current_question_id = None

    def deactivate(self) -> None:
        """Deactivates the support user.

        Raises:
            IncorrectActionError: raised if tried to deactivate an Owner
            SameValueAssigningError: raised when this support user
            was already deactivated
        """

        if self.is_owner:
            raise IncorrectActionError("Owner cannot be deactivated")

        if not self.is_active:
            raise SameValueAssigningError(
                "This Support User has already been deactivated"
            )

        self.current_question_id = None

        self.is_active = False

    def activate(self) -> None:
        """Activates the support user.

        Raises:
            SameValueAssigningError: raised if the support user
            is already active
        """

        if self.is_active:
            raise SameValueAssigningError(
                "This Support User is already active"
            )

        self.is_active = True

    def can_answer_questions(self) -> bool:
        """This method is used when you want to find out
        whether the support user can answer questions.

        Returns:
            bool: True if the support user can answer questions,
            False otherwise
        """
        if self.role is None:
            return False

        return (
            bool(self.role) and self.role.permissions.can_answer_questions
        ) or self.is_owner

    def can_manage_support_users(self) -> bool:
        """This method is used when you want to find out
        whether the support user can manage support users.

        Returns:
            bool: True if the support user can manage support users,
            False otherwise
        """
        if self.role is None:
            return False

        return (
            bool(self.role) and self.role.permissions.can_manage_support_users
        ) or self.is_owner

    @classmethod
    def create(
        cls,
        descriptive_name: DescriptiveName,
        tg_bot_user_id: TgUserId,
        role: SupportUserRole | None = None,
    ) -> Self:
        """Creates a new ```SupportUser``` entity.

        Args:
            descriptive_name (DescriptiveName): support user descriptive name
            tg_bot_user_id (TgUserId): Telegram bot user id of the user
            role (SupportUserRole | None, optional): role for the support user.
            Defaults to None

        Returns:
            Self: a new ```SupportUser``` entity
        """

        support_user = cls(
            id=SupportUserIdType(uuid4()),
            descriptive_name=descriptive_name,
            tg_bot_user_id=tg_bot_user_id,
            role=role,
            current_question_id=None,
            join_date=datetime.utcnow(),
            is_owner=False,
            is_active=True,
        )

        return support_user

    @classmethod
    def create_owner(
        cls,
        descriptive_name: DescriptiveName,
        tg_bot_user_id: TgUserId,
    ) -> Self:
        """Creates a new ```SupportUser``` entity with Owner rights.

        Args:
            descriptive_name (DescriptiveName): support user descriptive name
            tg_bot_user_id (TgUserId): Telegram bot user id of the user

        Returns:
            Self: a new ```SupportUser``` entity with Owner rights
        """

        support_user = cls(
            id=SupportUserIdType(uuid4()),
            descriptive_name=descriptive_name,
            tg_bot_user_id=tg_bot_user_id,
            role=None,
            current_question_id=None,
            join_date=datetime.utcnow(),
            is_owner=True,
            is_active=True,
        )

        return support_user


class SupportUserRole(IdComparable):
    _id: RoleIdType

    permissions: RolePermissions

    def __init__(
        self, role_id: RoleIdType, permissions: RolePermissions
    ) -> None:
        self._id = role_id
        self.permissions = permissions
