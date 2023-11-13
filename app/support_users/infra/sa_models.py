from __future__ import annotations

from datetime import datetime
from typing import Self
from uuid import uuid4

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import UUIDType

from app.answers.infra.sa_models import AnswerModel
from app.config.db_sa_config import ModelBase
from app.questions.infra.sa_models import QuestionModel
from app.roles.infra.sa_models import RoleModel
from app.shared.dtos import SupportUserDTO, SupportUserRoleDTO

from app.support_users.entities import SupportUser, SupportUserRole
from app.support_users.value_objects import DescriptiveName
from app.shared.value_objects import (
    QuestionIdType,
    RoleIdType,
    RolePermissions,
    SupportUserIdType,
    TgUserId,
)


class SupportUserModel(ModelBase):
    __tablename__ = "support_users"

    # User id
    id: Mapped[SupportUserIdType] = mapped_column(
        UUIDType(binary=False), primary_key=True, default=uuid4
    )

    # PROPERTIES
    descriptive_name: Mapped[DescriptiveName] = mapped_column(
        String(255), nullable=False, unique=False
    )

    # Unique telegram id that's given
    # to a user when chatting started
    tg_bot_user_id: Mapped[TgUserId] = mapped_column(Integer, unique=True)

    join_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=datetime.now
    )

    is_owner: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True
    )

    # RELATIONSHIPS

    # Current question relationship
    current_question_id: Mapped[QuestionIdType | None] = mapped_column(
        UUIDType(binary=False),
        ForeignKey("questions.id"),
        nullable=True,
        default=None,
    )

    current_question: Mapped[QuestionModel | None] = relationship(
        "QuestionModel", uselist=False, back_populates="current_support_user"
    )

    # Role relationship
    role_id: Mapped[RoleIdType | None] = mapped_column(
        Integer(),
        ForeignKey("roles.id", ondelete="SET DEFAULT"),
        nullable=True,
        default=None,
    )

    role: Mapped[RoleModel | None] = relationship(
        "RoleModel", back_populates="users"
    )

    # Answers relationship

    answers: Mapped[list[AnswerModel]] = relationship(
        "AnswerModel", passive_deletes="all", back_populates="support_user"
    )

    # METHODS

    @classmethod
    def from_entity(cls, support_user_entity: SupportUser) -> Self:
        result = cls()

        if support_user_entity._id:
            result.id = support_user_entity._id

        result.current_question_id = support_user_entity.current_question_id

        result.role_id = (
            support_user_entity.role._id if support_user_entity.role else None
        )

        result.descriptive_name = support_user_entity.descriptive_name

        result.tg_bot_user_id = support_user_entity.tg_bot_user_id

        result.join_date = support_user_entity.join_date
        result.is_active = support_user_entity.is_active
        result.is_owner = support_user_entity.is_owner

        return result

    def bind_question(self, question: QuestionModel):
        """Binds question to the support_user

        Must be commited using session.commit()

        Args:
            question (QuestionModel): a question that will be bound
        """
        self.current_question = question

    def add_answer(self, answer: AnswerModel):
        """Adds answer to this user's answers

        Must be commited using session.commit()

        Args:
            answer (AnswerModel): an answer that will be added to
            the user's answers
        """
        self.answers.append(answer)

    def as_entity(self) -> SupportUser:
        role = (
            SupportUserRole(
                self.role.id,
                RolePermissions(
                    self.role.can_answer_questions,
                    self.role.can_manage_support_users,
                ),
            )
            if self.role
            else None
        )

        return SupportUser(
            id=self.id,
            role=role,
            tg_bot_user_id=self.tg_bot_user_id,
            descriptive_name=self.descriptive_name,
            current_question_id=self.current_question_id,
            join_date=self.join_date,
            is_owner=self.is_owner,
            is_active=self.is_active,
        )

    def as_dto(self) -> SupportUserDTO:
        role = (
            SupportUserRoleDTO(
                id=self.role.id,
                permissions=RolePermissions(
                    self.role.can_answer_questions,
                    self.role.can_manage_support_users,
                ),
            )
            if self.role
            else None
        )

        return SupportUserDTO(
            id=self.id,
            role=role,
            tg_bot_id=self.tg_bot_user_id,
            descriptive_name=self.descriptive_name,
            bound_question_id=self.current_question_id,
            join_date=self.join_date,
            is_owner=self.is_owner,
            is_active=self.is_active,
        )
