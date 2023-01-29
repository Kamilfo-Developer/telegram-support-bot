from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy_utils import UUIDType
from uuid import uuid4
from bot.db.models.sa.question_model import QuestionModel
from bot.db.db_sa_settings import BINARY_UUID, Base
from bot.entities.regular_user import RegularUser
from datetime import datetime


class RegularUserModel(Base):
    __tablename__ = "regular_users"

    # User id
    id = Column(UUIDType(binary=BINARY_UUID), primary_key=True, default=uuid4)

    # PROPERTIES

    # Unique telegram id that's given
    # to a user when chatting started
    tg_bot_user_id = Column(Integer, nullable=True, default=None, unique=True)

    join_date = Column(DateTime, nullable=False, default=datetime.now)

    # RELATIONSHIPS

    # Questions relationship
    questions = relationship(
        "QuestionModel",
        passive_deletes=True,
        back_populates="regular_user",
    )

    # METHODS
    def add_question(self, question: QuestionModel):
        """Adds question to this user

        Needed to be commited using session.commit()

        Args:
            question (QuestionModel): a question that will be
            added to questions of the user
        """
        self.questions.append(question)

    def as_regular_user_entity(self) -> RegularUser:
        return RegularUser(
            self.id, self.tg_bot_user_id, self.join_date  # type: ignore
        )
