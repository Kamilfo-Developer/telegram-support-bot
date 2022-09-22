from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Boolean, Integer, String, DateTime
from bot.db.db_config import Base
from bot.db.models.support_user_model import SupportUserModel


class RoleModel(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, autoincrement=True)

    users = relationship("SupportUserModel")

    name = Column(String, nullable=False, unique=True)

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

    def add_user(self, support_user: SupportUserModel):
        """Binds question to the support_user

        Needed to be commited using session.commit()

        Args:
            support_user (SupportUserModel): a user, which will be added
            to users with this role
        """
        self.users.append(support_user)
