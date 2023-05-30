from __future__ import annotations
from datetime import datetime
from typing import Self
from uuid import UUID, uuid4
from app.entities.question import Question
from app.entities.role import Role
from app.utils import IdComparable


class SupportUser(IdComparable):
    _id: UUID
    current_question_id: UUID | None
    role: Role | None
    tg_bot_user_id: int
    descriptive_name: str
    join_date: datetime
    is_owner: bool = False

    def __init__(
        self,
        id: UUID,
        descriptive_name: str,
        tg_bot_user_id: int,
        role: Role | None,
        current_question: Question | None,
        join_date: datetime,
        is_active: bool,
        is_owner: bool,
    ) -> None:
        self._id = id
        self.current_question = current_question
        self.role = role
        self.tg_bot_user_id = tg_bot_user_id
        self.descriptive_name = descriptive_name
        self.join_date = join_date
        self.is_owner = is_owner
        self.is_active = is_active

    def make_owner(self) -> None:
        self.is_owner = True

    def remove_owner_rights(self) -> None:
        self.is_owner = False

    def change_role(self, new_role: Role) -> None:
        self.role = new_role

    def bind_question(self, question_id: UUID) -> None:
        if not self.role or self.role.permissions.can_answer_questions:
            raise PermissionError

        self.current_question_id = question_id

    def unbind_question(self) -> None:
        self.current_question = None

    def deactivate(self) -> None:
        self.current_question = None

        self.is_active = False

    def activate(self) -> None:
        self.is_active = True

    @classmethod
    def create(
        cls,
        descriptive_name: str,
        tg_bot_user_id: int,
        role: Role | None = None,
        is_owner: bool = False,
    ) -> Self:
        support_user = cls(
            id=uuid4(),
            descriptive_name=descriptive_name,
            tg_bot_user_id=tg_bot_user_id,
            role=role,
            current_question=None,
            join_date=datetime.utcnow(),
            is_owner=is_owner,
            is_active=True,
        )

        return support_user
