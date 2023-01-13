from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, DateTime, String, ForeignKey, Boolean
from sqlalchemy_utils import UUIDType
from uuid import uuid4
from bot.db.models.sa.question_model import QuestionModel
from bot.db.models.sa.answer_model import AnswerModel
from bot.db.db_sa_settings import BINARY_UUID, Base
from bot.entities.support_user import SupportUser
from datetime import datetime


class SupportUserModel(Base):
    __tablename__ = "support_users"

    # User id
    id = Column(UUIDType(binary=BINARY_UUID), primary_key=True, default=uuid4)

    # PROPERTIES
    descriptive_name = Column(String, nullable=False, unique=False)

    # Unique telegram id that's given
    # to a user when chatting started
    tg_bot_user_id = Column(Integer, nullable=True, default=None, unique=True)

    join_date = Column(DateTime, nullable=False, default=datetime.now)

    is_owner = Column(Boolean, default=True)

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
        ForeignKey("roles.id", ondelete="SET DEFAULT"),
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

    def as_support_user_entity(self) -> SupportUser:
        return SupportUser(
            id=self.id,  # type: ignore
            role_id=self.role_id,  # type: ignore
            tg_bot_user_id=self.tg_bot_user_id,  # type: ignore
            descriptive_name=self.descriptive_name,  # type: ignore
            current_question_id=self.current_question_id,  # type: ignore
            join_date=self.join_date,  # type: ignore
            is_owner=self.is_owner,  # type: ignore
        )
