from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Self
from uuid import UUID, uuid4

from sqlalchemy import (
    Boolean,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils import UUIDType

from app.shared.dtos import AnswerDTO


from app.answers.entities import Answer, AnswerAttachment
from app.config.db_sa_config import ModelBase
from app.shared.value_objects import (
    AnswerIdType,
    QuestionIdType,
    SupportUserIdType,
    TgCaption,
    TgFileIdType,
    TgMessageIdType,
    TgMessageText,
)
from app.utils import TgFileType

if TYPE_CHECKING:
    from app.questions.infra.sa_models import QuestionModel
    from app.support_users.infra.sa_models import SupportUserModel


class AnswerModel(ModelBase):
    __tablename__ = "answers"

    # RELATIONSHIP

    # Support User relationship
    support_user_id: Mapped[SupportUserIdType] = mapped_column(
        UUIDType(binary=False),
        ForeignKey("support_users.id", ondelete="CASCADE"),
    )

    support_user: Mapped[SupportUserModel] = relationship(
        "SupportUserModel", back_populates="answers"
    )

    # Question relationship
    question_id: Mapped[QuestionIdType] = mapped_column(
        UUIDType(binary=False),
        ForeignKey("questions.id", ondelete="CASCADE"),
    )

    question: Mapped[QuestionModel] = relationship(
        "QuestionModel", back_populates="answers"
    )

    # Answers attachments relationship
    answer_attachments: Mapped[list[AnswerAttachmentModel]] = relationship(
        "AnswerAttachmentModel", back_populates="answer"
    )

    # PROPERTIES
    id: Mapped[AnswerIdType] = mapped_column(
        UUIDType(binary=False), primary_key=True, default=uuid4
    )

    message: Mapped[TgMessageText] = mapped_column(Text)

    is_useful: Mapped[bool | None] = mapped_column(
        Boolean, nullable=True, default=None
    )

    tg_message_id: Mapped[TgMessageIdType] = mapped_column(
        Integer, unique=True
    )

    date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=datetime.now
    )

    @classmethod
    def from_entity(cls, answer_entity: Answer) -> Self:
        result = cls()

        if answer_entity._id:
            result.id = answer_entity._id

        result.answer_attachments = [
            AnswerAttachmentModel.from_entity(
                attachment_entity, answer_entity._id
            )
            for attachment_entity in answer_entity.attachments
        ]

        result.support_user_id = answer_entity.support_user_id
        result.question_id = answer_entity.question_id
        result.message = answer_entity.message
        result.tg_message_id = answer_entity.tg_message_id
        result.is_useful = answer_entity.is_useful
        result.date = answer_entity.date

        return result

    def as_entity(self) -> Answer:
        attachments = [
            attachment.as_entity() for attachment in self.answer_attachments
        ]

        return Answer(
            id=self.id,
            support_user_id=self.support_user_id,
            question_id=self.question_id,
            message=self.message,
            tg_message_id=self.tg_message_id,
            attachments=attachments,
            is_useful=self.is_useful,
            date=self.date,
        )

    def as_dto(self) -> AnswerDTO:
        return AnswerDTO(
            id=self.id,
            support_user_id=self.support_user_id,
            question_id=self.question_id,
            message=self.message,
            tg_message_id=self.tg_message_id,
            is_useful=self.is_useful,
            date=self.date,
        )


class AnswerAttachmentModel(ModelBase):
    __tablename__ = "answers_attachments"

    # RELATIONSHIPS

    # Question relationship
    answer_id: Mapped[UUID] = mapped_column(
        UUIDType(binary=False),
        ForeignKey("answers.id", ondelete="CASCADE"),
    )

    answer: Mapped[Answer] = relationship(
        "AnswerModel", back_populates="answer_attachments"
    )

    # PROPERTIES
    tg_file_id: Mapped[TgFileIdType] = mapped_column(
        String(255), primary_key=True
    )

    attachment_type: Mapped[TgFileType] = mapped_column(
        Enum(TgFileType), nullable=False
    )

    caption: Mapped[TgCaption | None] = mapped_column(
        String(1024), nullable=True, default=None
    )

    date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=datetime.now
    )

    @classmethod
    def from_entity(
        cls,
        answer_attachment_entity: AnswerAttachment,
        answer_id: AnswerIdType,
    ) -> Self:
        result = cls()

        result.tg_file_id = answer_attachment_entity.tg_file_id
        result.answer_id = answer_id
        result.attachment_type = answer_attachment_entity.attachment_type
        result.caption = answer_attachment_entity.caption
        result.date = answer_attachment_entity.date

        return result

    def as_entity(self) -> AnswerAttachment:
        return AnswerAttachment(
            tg_file_id=self.tg_file_id,
            attachment_type=self.attachment_type,
            caption=self.caption,
            date=self.date,
        )
