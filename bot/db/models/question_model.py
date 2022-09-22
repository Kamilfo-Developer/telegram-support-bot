from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, Text, Integer, DateTime
from sqlalchemy_utils import UUIDType
from uuid import uuid4
from bot.db.db_config import Base, is_uuid_binary
from bot.db.models.answer_model import AnswerModel


class QuestionModel(Base):
    __tablename__ = "questions"

    id = Column(
        UUIDType(binary=is_uuid_binary), primary_key=True, default=uuid4
    )

    regular_user_id = Column(
        UUIDType(binary=is_uuid_binary), ForeignKey("regular_users.id")
    )

    answers = relationship("AnswerModel", cascade="all, delete-orphan")

    current_support_user = relationship("SupportUserModel", uselist=False)

    message = Column(Text)

    tg_message_id = Column(Integer, nullable=True, unique=True)

    date = Column(DateTime, nullable=False, default=datetime.now)

    def add_answer(self, answer: AnswerModel):
        """Adds answer to this user's answers

        Needed to be commited using session.commit()

        Args:
            answer (AnswerModel): an answer that will be added to
            the user answers
        """
        self.answers.append(answer)
