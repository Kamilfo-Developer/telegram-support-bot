from datetime import datetime
from sqlalchemy import Column, ForeignKey, Text, Integer, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType
from uuid import uuid4
from bot.db.db_sa_settings import Base, BINARY_UUID
from bot.entities.answer import Answer


class AnswerModel(Base):
    __tablename__ = "answers"

    # RELATIONSHIP

    # Support User relationship
    support_user_id = Column(
        UUIDType(binary=BINARY_UUID),
        ForeignKey("support_users.id", ondelete="CASCADE"),
    )

    support_user = relationship("SupportUserModel", back_populates="answers")

    # Question relationship
    question_id = Column(
        UUIDType(binary=BINARY_UUID),
        ForeignKey("questions.id", ondelete="CASCADE"),
    )

    question = relationship("QuestionModel", back_populates="answers")

    # Answers attachments relationship
    answer_attachments = relationship(
        "AnswerAttachmentModel", back_populates="answer"
    )

    # PROPERTIES
    id = Column(UUIDType(binary=BINARY_UUID), primary_key=True, default=uuid4)

    message = Column(Text)

    is_useful = Column(Boolean, default=None)

    tg_message_id = Column(Integer, nullable=True, unique=True)

    date = Column(DateTime, nullable=False, default=datetime.now)

    def as_answer_entity(self) -> Answer:
        support_user = (
            self.support_user and self.support_user.as_support_user_entity()
        )

        question = self.question and self.question.as_question_entity()

        return Answer(
            id=self.id,  # type: ignore
            support_user=support_user,  # type: ignore
            question=question,  # type: ignore
            message=self.message,  # type: ignore
            tg_message_id=self.tg_message_id,  # type: ignore
            is_useful=self.is_useful,  # type: ignore
            date=self.date,  # type: ignore
        )
