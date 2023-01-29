from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, DateTime, String, Enum
from sqlalchemy_utils import UUIDType
from uuid import uuid4
from bot.db.db_sa_settings import Base, BINARY_UUID
from bot.entities.question_attachment import QuestionAttachment
from bot.utils import AttachmentType


class QuestionAttachmentModel(Base):
    __tablename__ = "questions_attachmets"

    # RELATIONSHIPS

    # Question relationship
    question_id = Column(
        UUIDType(binary=BINARY_UUID),
        ForeignKey("questions.id", ondelete="CASCADE"),
    )

    question = relationship(
        "QuestionModel", back_populates="question_attachments"
    )

    # PROPERTIES
    id = Column(UUIDType(binary=BINARY_UUID), primary_key=True, default=uuid4)

    tg_file_id = Column(String, nullable=False)

    attachment_type = Column(Enum(AttachmentType), nullable=False)

    date = Column(DateTime, nullable=False, default=datetime.now)

    def as_question_attachment_entity(self) -> QuestionAttachment:
        return QuestionAttachment(
            id=self.id,  # type: ignore
            question_id=self.question.id,  # type: ignore
            tg_file_id=self.tg_file_id,  # type: ignore
            attachment_type=self.attachment_type,  # type: ignore
            date=self.date,  # type: ignore
        )
