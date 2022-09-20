from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer
from sqlalchemy_utils import UUIDType
from uuid import uuid4
from bot.db.db_config import Base
from bot.db.models.question_model import QuestionModel


class RegularUserModel(Base):
    __tablename__ = "regular_users"

    id = Column(UUIDType(binary=True), primary_key=True, default=uuid4)

    # Unique telegram id that's given
    # to a user when chatting started
    tg_bot_user_id = Column(Integer, nullable=True, default=None)

    questions = relationship("QuestionModel", cascade="all, delete")

    def add_question(self, question: QuestionModel):
        """Adds question to this user

        Needed to be commited using session.commit()

        Args:
            question (QuestionModel): a question that will be
            added to questions of the user
        """
        self.questions.append(question)
