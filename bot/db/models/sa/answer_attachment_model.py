from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, DateTime, String, Enum
from sqlalchemy_utils import UUIDType
from uuid import uuid4
from bot.db.db_sa_settings import Base, BINARY_UUID
from bot.entities.answer import AnswerAttachment
from bot.utils import AttachmentType


class AnswerAttachmentModel(Base):
    __tablename__ = "questions_attachmets"

    # RELATIONSHIPS

    # Question relationship
    answer_id = Column(
        UUIDType(binary=BINARY_UUID),
        ForeignKey("answers.id", ondelete="CASCADE"),
    )

    answer = relationship("AnswerModel", back_populates="answer_attachments")

    # PROPERTIES
    id = Column(UUIDType(binary=BINARY_UUID), primary_key=True, default=uuid4)

    tg_file_id = Column(String, nullable=False)

    attachment_type = Column(Enum(AttachmentType), nullable=False)

    date = Column(DateTime, nullable=False, default=datetime.now)

    def as_answer_attachment_entity(self) -> AnswerAttachment:
        return AnswerAttachment(
            id=self.id,  # type: ignore
            answer_id=self.answer.id,  # type: ignore
            tg_file_id=self.tg_file_id,  # type: ignore
            attachment_type=self.attachment_type,  # type: ignore
            date=self.date,  # type: ignore
        )
