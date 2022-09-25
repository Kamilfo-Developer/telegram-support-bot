from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey
from sqlalchemy_utils import UUIDType
from uuid import uuid4
from bot.db.models.question_model import QuestionModel
from bot.db.models.answer_model import AnswerModel
from bot.db.models.user_model import UserModel
from bot.db.db_config import is_uuid_binary


class SupportUserModel(UserModel):
    __tablename__ = "support_users"

    id = Column(
        UUIDType(binary=is_uuid_binary),
        ForeignKey("users.id"),
        primary_key=True,
        default=uuid4,
    )

    current_question_id = Column(
        UUIDType(binary=is_uuid_binary),
        ForeignKey("questions.id"),
        nullable=True,
        default=None,
    )

    current_question = relationship(
        "QuestionModel", uselist=False, overlaps="current_support_user"
    )

    role_id = Column(
        UUIDType(binary=is_uuid_binary),
        ForeignKey("roles.id"),
        nullable=True,
        default=None,
    )

    answers = relationship("AnswerModel", passive_deletes="all")

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
