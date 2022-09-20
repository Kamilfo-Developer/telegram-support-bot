from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy_utils import UUIDType
from uuid import uuid4
from bot.db.db_config import Base
from bot.db.models.question_model import QuestionModel
from bot.db.models.answer_model import AnswerModel


class SupportUserModel(Base):
    __tablename__ = "support_users"

    id = Column(UUIDType(binary=True), primary_key=True, default=uuid4)

    # Unique telegram id that's given
    # to a user when chatting started
    tg_bot_user_id = Column(Integer, nullable=True, default=None)

    current_question_id = Column(
        UUIDType(binary=True),
        ForeignKey("questions.id"),
        nullable=True,
        default=None,
    )

    current_question = relationship("QuestionModel", uselist=False)

    role_id = Column(
        Integer, ForeignKey("roles.id"), nullable=True, default=None
    )

    answers = relationship("AnswerModel", cascade="all, delete")

    def bind_question(self, question: QuestionModel):
        """Binds question to the support_user

        Needed to be commited using session.commit()

        Args:
            question (QuestionModel): a question that will be binded
        """
        self.current_question = question

    def add_answer(self, answer: AnswerModel):
        """Adds answer to this user's answers

        Needed to be commited using session.commit()

        Args:
            answer (AnswerModel): an answer that will be added to
            the user's answers
        """
        self.answers.append(answer)
