from datetime import datetime
from uuid import uuid4
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Boolean, String, DateTime, Text, Integer
from sqlalchemy_utils import UUIDType
from bot.db.db_sa_settings import Base, BINARY_UUID
from bot.db.models.sa.support_user_model import SupportUserModel
from bot.entities.role import Role


class RoleModel(Base):
    __tablename__ = "roles"

    # RELATIONSHIPS

    # Users relationship
    users = relationship("SupportUserModel", back_populates="role")

    # PROPERTIES

    id = Column(Integer, primary_key=True)

    name = Column(String, nullable=False, unique=True)

    description = Column(Text, nullable=False, default="")

    created_date = Column(DateTime, nullable=False, default=datetime.now)

    # If False a support user cannot use answering
    # question interface
    can_answer_questions = Column(Boolean, default=True)

    # If False a support user cannot manage other support users and roles
    # Also they won't be able to get information about other support users
    can_manage_support_users = Column(Boolean, default=True)

    # METHODS

    def add_user(self, support_user: SupportUserModel):
        """Binds question to the support_user

        Needed to be commited using session.commit()

        Args:
            support_user (SupportUserModel): a user, which will be added
            to users with this role
        """
        self.users.append(support_user)

    def as_role_entity(self) -> Role:
        return Role(
            id=self.id,
            name=self.name,
            description=self.description,
            can_answer_questions=self.can_answer_questions,
            can_manage_support_users=self.can_manage_support_users,
            created_date=self.created_date,
        )
