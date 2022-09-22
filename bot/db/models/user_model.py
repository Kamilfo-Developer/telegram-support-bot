from sqlalchemy import Column, Integer
from sqlalchemy_utils import UUIDType
from uuid import uuid4
from bot.db.db_config import Base, is_uuid_binary


class UserModel(Base):
    __tablename__ = "users"

    id = Column(
        UUIDType(binary=is_uuid_binary), primary_key=True, default=uuid4
    )

    # Unique telegram id that's given
    # to a user when chatting started
    tg_bot_user_id = Column(Integer, nullable=True, default=None, unique=True)
