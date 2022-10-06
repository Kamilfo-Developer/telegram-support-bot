from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey
from sqlalchemy_utils import UUIDType
from uuid import uuid4
from bot.db.models.question_model import QuestionModel
from bot.db.models.user_model import UserModel
from bot.db.db_config import is_uuid_binary


class RegularUserModel(UserModel):
    __tablename__ = "regular_users"

    # User id
    id = Column(
        UUIDType(binary=is_uuid_binary),
        ForeignKey("users.id"),
        primary_key=True,
        default=uuid4,
    )

    # RELATIONSHIPS

    # Questions relationship
    questions = relationship(
        "QuestionModel", passive_deletes=True, back_populates="regular_user"
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
