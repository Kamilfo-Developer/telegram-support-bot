from datetime import datetime
from sqlalchemy import Column, ForeignKey, Text, Integer, DateTime
from sqlalchemy_utils import UUIDType
from uuid import uuid4
from bot.db.db_config import Base


class AnswerModel(Base):
    __tablename__ = "answers"

    id = Column(UUIDType(binary=True), primary_key=True, default=uuid4)

    support_user_id = Column(
        UUIDType(binary=True), ForeignKey("support_users.id")
    )

    question_id = Column(UUIDType(binary=True), ForeignKey("questions.id"))

    message = Column(Text)

    tg_message_id = Column(Integer, nullable=True)

    date = Column(DateTime, nullable=False, default=datetime.now)
