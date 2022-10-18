from sqlalchemy import Column, Integer
from sqlalchemy_utils import UUIDType
from uuid import uuid4
from bot.db.db_settings import Base, BINARY_UUID


class UserModel(Base):
    __tablename__ = "users"

    # PROPERTIES
    id = Column(UUIDType(binary=BINARY_UUID), primary_key=True, default=uuid4)

    # Unique telegram id that's given
    # to a user when chatting started
    tg_bot_user_id = Column(Integer, nullable=True, default=None, unique=True)
