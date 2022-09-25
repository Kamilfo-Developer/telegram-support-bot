from datetime import datetime
from sqlalchemy import Column, ForeignKey, Text, Integer, DateTime
from sqlalchemy_utils import UUIDType
from uuid import uuid4
from bot.db.db_config import Base, is_uuid_binary


class AnswerModel(Base):
    __tablename__ = "answers"

    id = Column(
        UUIDType(binary=is_uuid_binary), primary_key=True, default=uuid4
    )

    support_user_id = Column(
        UUIDType(binary=is_uuid_binary),
        ForeignKey("support_users.id", ondelete="CASCADE"),
    )

    question_id = Column(
        UUIDType(binary=is_uuid_binary),
        ForeignKey("questions.id", ondelete="CASCADE"),
    )

    message = Column(Text)

    tg_message_id = Column(Integer, nullable=True, unique=True)

    date = Column(DateTime, nullable=False, default=datetime.now)
