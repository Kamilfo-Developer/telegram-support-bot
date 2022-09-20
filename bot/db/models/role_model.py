from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Boolean, Integer, String, DateTime
from bot.db.db_config import Base


class RoleModel(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, autoincrement=True)

    users = relationship("SupportUserModel")

    name = Column(String, nullable=False)

    date = Column(DateTime, nullable=False, default=datetime.now)

    # If False the support user cannot use answering
    # question interface
    can_answer_questions = Column(Boolean, default=True)

    can_create_roles = Column(Boolean, default=False)
    can_romove_roles = Column(Boolean, default=False)
    can_change_roles = Column(Boolean, default=False)

    # If False the support user cannot assing roles
    # to other users
    can_assign_roles = Column(Boolean, default=False)
