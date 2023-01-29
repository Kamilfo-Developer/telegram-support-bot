from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, Text, Integer, DateTime
from sqlalchemy_utils import UUIDType
from uuid import uuid4
from bot.db.db_sa_settings import Base, BINARY_UUID
from bot.db.models.sa.answer_model import AnswerModel
from bot.entities.question import Question


class QuestionModel(Base):
    __tablename__ = "questions"

    # RELATIONSHIPS

    # Regular User relationship
    regular_user_id = Column(
        UUIDType(binary=BINARY_UUID),
        ForeignKey("regular_users.id", ondelete="CASCADE"),
    )

    regular_user = relationship(
        "RegularUserModel",
        back_populates="questions",
        foreign_keys=[regular_user_id],
    )

    # Answers for the question relationship
    answers = relationship(
        "AnswerModel", passive_deletes=True, back_populates="question"
    )

    # Support User that binded the question relationship
    current_support_user = relationship(
        "SupportUserModel", uselist=False, back_populates="current_question"
    )

    # Attachments for the question relationship
    question_attachments = relationship(
        "QuestionAttachmentModel",
        passive_deletes=True,
        back_populates="question",
    )

    # PROPERTIES
    id = Column(UUIDType(binary=BINARY_UUID), primary_key=True, default=uuid4)

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

    def as_question_entity(self) -> Question:
        regular_user = (
            self.regular_user and self.regular_user.as_regular_user_entity()
        )

        return Question(
            id=self.id,  # type: ignore
            regular_user=regular_user,  # type: ignore
            message=self.message,  # type: ignore
            tg_message_id=self.tg_message_id,  # type: ignore
            date=self.date,  # type: ignore
        )
