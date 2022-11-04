from datetime import datetime
from sqlalchemy import Column, ForeignKey, Text, Integer, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy_utils import UUIDType
from uuid import uuid4
from bot.db.db_settings import Base, BINARY_UUID
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

    # PROPERTIES
    id = Column(UUIDType(binary=BINARY_UUID), primary_key=True, default=uuid4)

    message = Column(Text)

    tg_message_id = Column(Integer, nullable=True, unique=True)

    date = Column(DateTime, nullable=False, default=datetime.now)

    def as_answer_entity(self) -> Answer:
        return Answer(
            self.id,
            self.support_user_id,
            self.question_id,
            self.message,
            self.tg_message_id,
            self.date,
        )
