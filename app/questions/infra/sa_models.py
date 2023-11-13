from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Self
from uuid import uuid4

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import UUIDType

from app.config.db_sa_config import ModelBase
from app.questions.entities import Question, QuestionAttachment
from app.shared.dtos import QuestionDTO
from app.shared.value_objects import (
    QuestionIdType,
    RegularUserIdType,
    TgCaption,
    TgFileIdType,
    TgMessageIdType,
    TgMessageText,
)
from app.utils import TgFileType

if TYPE_CHECKING:
    from app.answers.infra.sa_models import AnswerModel
    from app.regular_users.infra.sa_models import RegularUserModel
    from app.support_users.infra.sa_models import SupportUserModel


class QuestionModel(ModelBase):
    __tablename__ = "questions"

    # RELATIONSHIPS

    # Regular User relationship
    regular_user_id: Mapped[RegularUserIdType] = mapped_column(
        UUIDType(binary=False),
        ForeignKey("regular_users.id", ondelete="CASCADE"),
    )

    regular_user: Mapped[RegularUserModel] = relationship(
        "RegularUserModel",
        back_populates="questions",
        foreign_keys=[regular_user_id],
    )

    # Answers for the question relationship
    answers: Mapped[list["AnswerModel"]] = relationship(
        "AnswerModel", passive_deletes=True, back_populates="question"
    )

    # Support User that bound the question relationship
    current_support_user: Mapped[SupportUserModel | None] = relationship(
        "SupportUserModel", uselist=False, back_populates="current_question"
    )

    # Attachments for the question relationship
    question_attachments: Mapped[list[QuestionAttachmentModel]] = relationship(
        "QuestionAttachmentModel",
        passive_deletes=True,
        back_populates="question",
    )

    # PROPERTIES
    id: Mapped[QuestionIdType] = mapped_column(
        UUIDType(binary=False), primary_key=True, default=uuid4
    )

    message: Mapped[TgMessageText] = mapped_column(Text, nullable=False)

    tg_message_id: Mapped[TgMessageIdType] = mapped_column(
        Integer, unique=True
    )

    date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=datetime.now
    )

    # METHODS

    @classmethod
    def from_entity(cls, question_entitity: Question) -> Self:
        result = cls()

        if question_entitity._id:
            result.id = question_entitity._id

        result.question_attachments = [
            QuestionAttachmentModel.from_entity(
                attachment_entity, question_entitity._id
            )
            for attachment_entity in question_entitity.attachments
        ]

        result.regular_user_id = question_entitity.regular_user_id

        result.message = question_entitity.message

        result.tg_message_id = question_entitity.tg_message_id

        result.date = question_entitity.date

        return result

    def add_answer(self, answer: "AnswerModel"):
        """Adds answer to this user's answers

        Must be commited using session.commit()

        Args:
            answer ("AnswerModel"): an answer that will be added to
            the user's answers
        """
        self.answers.append(answer)

    def as_entity(self) -> Question:
        attachments = [
            attachment.as_entity() for attachment in self.question_attachments
        ]

        return Question(
            id=self.id,
            regular_user_id=self.regular_user_id,
            message=self.message,
            tg_message_id=self.tg_message_id,
            attachments=attachments,
            date=self.date,
        )

    def as_dto(self) -> QuestionDTO:
        return QuestionDTO(
            id=self.id,
            regular_user_id=self.regular_user_id,
            message=self.message,
            tg_message_id=self.tg_message_id,
            date=self.date,
        )


class QuestionAttachmentModel(ModelBase):
    __tablename__ = "questions_attachments"

    # RELATIONSHIPS

    # Question relationship
    question_id: Mapped[QuestionIdType] = mapped_column(
        UUIDType(binary=False),
        ForeignKey("questions.id", ondelete="CASCADE"),
    )

    question: Mapped[Question] = relationship(
        "QuestionModel", back_populates="question_attachments"
    )

    # PROPERTIES
    tg_file_id: Mapped[TgFileIdType] = mapped_column(
        String(255),
        primary_key=True,
    )

    attachment_type: Mapped[TgFileType] = mapped_column(
        Enum(TgFileType), nullable=False
    )

    caption: Mapped[TgCaption | None] = mapped_column(
        Text, nullable=True, default=None
    )

    date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=datetime.now
    )

    # METHODS

    @classmethod
    def from_entity(
        cls,
        question_attachment_entity: QuestionAttachment,
        question_id: QuestionIdType,
    ) -> Self:
        result = cls()

        result.question_id = question_id
        result.tg_file_id = question_attachment_entity.tg_file_id
        result.attachment_type = question_attachment_entity.attachment_type
        result.caption = question_attachment_entity.caption
        result.date = question_attachment_entity.date

        return result

    def as_entity(self) -> QuestionAttachment:
        return QuestionAttachment(
            tg_file_id=self.tg_file_id,
            attachment_type=self.attachment_type,
            caption=self.caption,
            date=self.date,
        )
