from __future__ import annotations

from datetime import datetime
from typing import Self
from uuid import uuid4

from sqlalchemy import DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import UUIDType

from app.config.db_sa_config import ModelBase
from app.questions.infra.sa_models import QuestionModel
from app.regular_users.dtos import RegularUserDTO
from app.regular_users.entities import RegularUser
from app.shared.value_objects import RegularUserIdType, TgUserId


class RegularUserModel(ModelBase):
    __tablename__ = "regular_users"

    # User id
    id: Mapped[RegularUserIdType] = mapped_column(
        UUIDType(binary=False), primary_key=True, default=uuid4
    )

    # PROPERTIES

    # Unique telegram id that's given
    # to a user when chatting started
    tg_bot_user_id: Mapped[TgUserId] = mapped_column(Integer, unique=True)

    join_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=datetime.now
    )

    # RELATIONSHIPS

    # Questions relationship
    questions: Mapped[list[QuestionModel]] = relationship(
        "QuestionModel",
        passive_deletes="all",
        back_populates="regular_user",
    )

    # METHODS

    @classmethod
    def from_entity(cls, regular_user_entity: RegularUser) -> Self:
        result = cls()

        if regular_user_entity._id:
            result.id = regular_user_entity._id

        result.tg_bot_user_id = regular_user_entity.tg_bot_user_id

        result.join_date = regular_user_entity.join_date

        return result

    def add_question(self, question: QuestionModel):
        """Adds question to this user

        Must be commited using session.commit()

        Args:
            question (QuestionModel): a question that will be
            added to questions of the user
        """
        self.questions.append(question)

    def as_entity(self) -> RegularUser:
        return RegularUser(self.id, self.tg_bot_user_id, self.join_date)

    def as_dto(self) -> RegularUserDTO:
        return RegularUserDTO(self.id, self.tg_bot_user_id, self.join_date)
