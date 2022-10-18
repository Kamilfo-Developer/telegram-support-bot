from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey
from sqlalchemy_utils import UUIDType
from uuid import uuid4
from bot.db.models.sa.question_model import QuestionModel
from bot.db.models.sa.answer_model import AnswerModel
from bot.db.models.sa.user_model import UserModel
from bot.db.db_settings import BINARY_UUID


class SupportUserModel(UserModel):
    __tablename__ = "support_users"

    # User id
    id = Column(
        UUIDType(binary=BINARY_UUID),
        ForeignKey("users.id"),
        primary_key=True,
        default=uuid4,
    )

    # RELATIONSHIPS

    # Current question relationship
    current_question_id = Column(
        UUIDType(binary=BINARY_UUID),
        ForeignKey("questions.id"),
        nullable=True,
        default=None,
    )

    current_question = relationship(
        "QuestionModel", uselist=False, back_populates="current_support_user"
    )

    # Role relationship
    role_id = Column(
        UUIDType(binary=BINARY_UUID),
        ForeignKey("roles.id"),
        nullable=True,
        default=None,
    )

    role = relationship("RoleModel", back_populates="users")

    # Answers relationship

    answers = relationship(
        "AnswerModel", passive_deletes="all", back_populates="support_user"
    )

    # METHODS

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
