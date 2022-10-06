from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, Text, Integer, DateTime
from sqlalchemy_utils import UUIDType
from uuid import uuid4
from bot.db.db_config import Base, is_uuid_binary
from bot.db.models.answer_model import AnswerModel


class QuestionModel(Base):
    __tablename__ = "questions"

    # RELATIONSHIPS

    # Regular User relationship
    regular_user_id = Column(
        UUIDType(binary=is_uuid_binary),
        ForeignKey("regular_users.id", ondelete="CASCADE"),
    )

    regular_user = relationship("RegularUserModel", back_populates="questions")

    # Answers for the question relationship
    answers = relationship(
        "AnswerModel", passive_deletes=True, back_populates="question"
    )

    # Support User that binded the question relationship
    current_support_user = relationship(
        "SupportUserModel", uselist=False, back_populates="current_question"
    )

    # PROPERTIES
    id = Column(
        UUIDType(binary=is_uuid_binary), primary_key=True, default=uuid4
    )

    message = Column(Text)

    tg_message_id = Column(Integer, nullable=True, unique=True)

    date = Column(DateTime, nullable=False, default=datetime.now)

    # METHODS

    def add_answer(self, answer: AnswerModel):
        """Adds answer to this user's answers

        Needed to be commited using session.commit()

        Args:
            answer (AnswerModel): an answer that will be added to
            the user's answers
        """
        self.answers.append(answer)
