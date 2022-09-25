from datetime import datetime
from uuid import uuid4
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Boolean, String, DateTime, Text
from sqlalchemy_utils import UUIDType
from bot.db.db_config import Base, is_uuid_binary
from bot.db.models.support_user_model import SupportUserModel


class RoleModel(Base):
    __tablename__ = "roles"

    id = Column(
        UUIDType(binary=is_uuid_binary), primary_key=True, default=uuid4
    )

    users = relationship("SupportUserModel")

    name = Column(String, nullable=False, unique=True)

    description = Column(Text, nullable=False, default="")

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
