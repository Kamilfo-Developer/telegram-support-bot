from __future__ import annotations
from datetime import datetime
from sqlalchemy.orm import (
    DeclarativeBase,
    relationship,
    Mapped,
    mapped_column,
)
from sqlalchemy import (
    ForeignKey,
    DateTime,
    String,
    Enum,
    Boolean,
    Integer,
    Text,
)
from sqlalchemy_utils import UUIDType
from uuid import uuid4, UUID
from bot.db.db_sa_settings import BINARY_UUID
from bot.entities.answer import AnswerAttachment
from bot.utils import AttachmentType
from bot.entities.answer import Answer
from bot.entities.regular_user import RegularUser
from bot.entities.support_user import SupportUser
from bot.entities.role import Role, RolePermissions
from bot.entities.question_attachment import QuestionAttachment
from bot.entities.question import Question


class ModelBase(DeclarativeBase):
    pass


class RoleModel(ModelBase):
    __tablename__ = "roles"

    # RELATIONSHIPS

    # Users relationship
    users = relationship("SupportUserModel", back_populates="role")

    # PROPERTIES

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)

    description: Mapped[str] = mapped_column(Text, nullable=False, default="")

    created_date: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now
    )

    # If False a support user cannot use answering
    # questions interface
    can_answer_questions: Mapped[bool] = mapped_column(Boolean, default=True)

    # If False a support user cannot manage other support users and roles
    # Also they won't be able to get information about other support users
    can_manage_support_users: Mapped[bool] = mapped_column(
        Boolean, default=False
    )

    # METHODS

    def add_user(self, support_user: SupportUserModel):
        """Binds question to the support_user

        Should be commited using session.commit()

        Args:
            support_user (SupportUserModel): a user, which will be added
            to users with this role
        """
        self.users.append(support_user)

    def as_role_entity(self) -> Role:
        permissions = RolePermissions(
            self.can_answer_questions, self.can_manage_support_users
        )

        return Role(
            id=self.id,
            name=self.name,
            description=self.description,
            permissions=permissions,
            created_date=self.created_date,
        )


class RegularUserModel(ModelBase):
    __tablename__ = "regular_users"

    # User id
    id: Mapped[UUID] = mapped_column(
        UUIDType(binary=BINARY_UUID), primary_key=True, default=uuid4
    )

    # PROPERTIES

    # Unique telegram id that's given
    # to a user when chatting started
    tg_bot_user_id: Mapped[int] = mapped_column(Integer, unique=True)

    join_date: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now
    )

    # RELATIONSHIPS

    # Questions relationship
    questions: Mapped[list[QuestionModel]] = relationship(
        "QuestionModel",
        passive_deletes=True,
        back_populates="regular_user",
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

    def as_regular_user_entity(self) -> RegularUser:
        return RegularUser(self.id, self.tg_bot_user_id, self.join_date)


class SupportUserModel(ModelBase):
    __tablename__ = "support_users"

    # User id
    id: Mapped[UUID] = mapped_column(
        UUIDType(binary=BINARY_UUID), primary_key=True, default=uuid4
    )

    # PROPERTIES
    descriptive_name: Mapped[str] = mapped_column(
        String, nullable=False, unique=False
    )

    # Unique telegram id that's given
    # to a user when chatting started
    tg_bot_user_id: Mapped[int] = mapped_column(Integer, unique=True)

    join_date: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now
    )

    is_owner: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True
    )

    # RELATIONSHIPS

    # Current question relationship
    current_question_id: Mapped[UUID | None] = mapped_column(
        UUIDType(binary=BINARY_UUID),
        ForeignKey("questions.id"),
        nullable=True,
        default=None,
    )

    current_question: Mapped[QuestionModel | None] = relationship(
        "QuestionModel", uselist=False, back_populates="current_support_user"
    )

    # Role relationship
    role_id: Mapped[int | None] = mapped_column(
        Integer(),
        ForeignKey("roles.id", ondelete="SET DEFAULT"),
        nullable=True,
        default=None,
    )

    role: Mapped[RoleModel | None] = relationship(
        "RoleModel", back_populates="users"
    )

    # Answers relationship

    answers: Mapped[list[AnswerModel]] = relationship(
        "AnswerModel", passive_deletes="all", back_populates="support_user"
    )

    # METHODS

    def bind_question(self, question: QuestionModel):
        """Binds question to the support_user

        Needed to be commited using session.commit()

        Args:
            question (QuestionModel): a question that will be binded
        """
        self.current_question = question

    def add_answer(self, answer: AnswerModel):
        """Adds answer to this user's answers

        Needed to be commited using session.commit()

        Args:
            answer (AnswerModel): an answer that will be added to
            the user's answers
        """
        self.answers.append(answer)

    def as_support_user_entity(self) -> SupportUser:
        role = self.role.as_role_entity() if self.role else None

        current_question = (
            self.current_question.as_question_entity()
            if self.current_question
            else None
        )

        return SupportUser(
            id=self.id,
            role=role,
            tg_bot_user_id=self.tg_bot_user_id,
            descriptive_name=self.descriptive_name,
            current_question=current_question,
            join_date=self.join_date,
            is_owner=self.is_owner,
            is_active=self.is_active,
        )


class QuestionModel(ModelBase):
    __tablename__ = "questions"

    # RELATIONSHIPS

    # Regular User relationship
    regular_user_id: Mapped[UUID] = mapped_column(
        UUIDType(binary=BINARY_UUID),
        ForeignKey("regular_users.id", ondelete="CASCADE"),
    )

    regular_user: Mapped[RegularUserModel] = relationship(
        "RegularUserModel",
        back_populates="questions",
        foreign_keys=[regular_user_id],
    )

    # Answers for the question relationship
    answers: Mapped[list[AnswerModel]] = relationship(
        "AnswerModel", passive_deletes=True, back_populates="question"
    )

    # Support User that binded the question relationship
    current_support_user: Mapped[SupportUserModel | None] = relationship(
        "SupportUserModel", uselist=False, back_populates="current_question"
    )

    # Attachments for the question relationship
    question_attachments: Mapped[list[QuestionAttachmentModel]] = relationship(
        "QuestionAttachmentModel",
        passive_deletes=True,
        back_populates="question",
    )

    # PROPERTIES
    id: Mapped[UUID] = mapped_column(
        UUIDType(binary=BINARY_UUID), primary_key=True, default=uuid4
    )

    message: Mapped[str] = mapped_column(Text, nullable=False)

    tg_message_id: Mapped[int] = mapped_column(Integer, unique=True)

    date: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now
    )

    # METHODS

    def add_answer(self, answer: AnswerModel):
        """Adds answer to this user's answers

        Needed to be commited using session.commit()

        Args:
            answer (AnswerModel): an answer that will be added to
            the user's answers
        """
        self.answers.append(answer)

    def as_question_entity(self) -> Question:
        regular_user = (
            self.regular_user.as_regular_user_entity()
            if self.regular_user
            else None
        )

        return Question(
            id=self.id,
            regular_user=regular_user,
            message=self.message,
            tg_message_id=self.tg_message_id,
            date=self.date,
        )


class AnswerModel(ModelBase):
    __tablename__ = "answers"

    # RELATIONSHIP

    # Support User relationship
    support_user_id: Mapped[UUID] = mapped_column(
        UUIDType(binary=BINARY_UUID),
        ForeignKey("support_users.id", ondelete="CASCADE"),
    )

    support_user: Mapped[SupportUserModel] = relationship(
        "SupportUserModel", back_populates="answers"
    )

    # Question relationship
    question_id: Mapped[UUID] = mapped_column(
        UUIDType(binary=BINARY_UUID),
        ForeignKey("questions.id", ondelete="CASCADE"),
    )

    question: Mapped[QuestionModel] = relationship(
        "QuestionModel", back_populates="answers"
    )

    # Answers attachments relationship
    answer_attachments: Mapped[list[AnswerAttachmentModel]] = relationship(
        "AnswerAttachmentModel", back_populates="answer"
    )

    # PROPERTIES
    id: Mapped[UUID] = mapped_column(
        UUIDType(binary=BINARY_UUID), primary_key=True, default=uuid4
    )

    message: Mapped[str] = mapped_column(Text)

    is_useful: Mapped[bool | None] = mapped_column(
        Boolean, nullable=True, default=None
    )

    tg_message_id: Mapped[int] = mapped_column(Integer, unique=True)

    date: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now
    )

    def as_answer_entity(self) -> Answer:
        support_user = (
            self.support_user.as_support_user_entity()
            if self.support_user
            else None
        )

        question = (
            self.question.as_question_entity() if self.question else None
        )

        return Answer(
            id=self.id,
            support_user=support_user,
            question=question,
            message=self.message,
            tg_message_id=self.tg_message_id,
            is_useful=self.is_useful,
            date=self.date,
        )


class QuestionAttachmentModel(ModelBase):
    __tablename__ = "questions_attachmets"

    # RELATIONSHIPS

    # Question relationship
    question_id: Mapped[UUID] = mapped_column(
        UUIDType(binary=BINARY_UUID),
        ForeignKey("questions.id", ondelete="CASCADE"),
    )

    question: Mapped[Question] = relationship(
        "QuestionModel", back_populates="question_attachments"
    )

    # PROPERTIES
    id: Mapped[UUID] = mapped_column(
        UUIDType(binary=BINARY_UUID), primary_key=True, default=uuid4
    )

    tg_file_id: Mapped[str] = mapped_column(String, nullable=False)

    attachment_type: Mapped[AttachmentType] = mapped_column(
        Enum(AttachmentType), nullable=False
    )

    caption: Mapped[str | None] = mapped_column(
        Text, nullable=True, default=None
    )

    date: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now
    )

    def as_question_attachment_entity(self) -> QuestionAttachment:
        return QuestionAttachment(
            id=self.id,
            question_id=self.question.id,
            tg_file_id=self.tg_file_id,
            attachment_type=self.attachment_type,
            caption=self.caption,
            date=self.date,
        )


class AnswerAttachmentModel(ModelBase):
    __tablename__ = "answers_attachmets"

    # RELATIONSHIPS

    # Question relationship
    answer_id: Mapped[UUID] = mapped_column(
        UUIDType(binary=BINARY_UUID),
        ForeignKey("answers.id", ondelete="CASCADE"),
    )

    answer: Mapped[Answer] = relationship(
        "AnswerModel", back_populates="answer_attachments"
    )

    # PROPERTIES
    id: Mapped[UUID] = mapped_column(
        UUIDType(binary=BINARY_UUID), primary_key=True, default=uuid4
    )

    tg_file_id: Mapped[str] = mapped_column(String, nullable=False)

    attachment_type: Mapped[AttachmentType] = mapped_column(
        Enum(AttachmentType), nullable=False
    )

    caption: Mapped[str | None] = mapped_column(
        Text, nullable=True, default=None
    )

    date: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now
    )

    def as_answer_attachment_entity(self) -> AnswerAttachment:
        return AnswerAttachment(
            id=self.id,
            answer_id=self.answer.id,
            tg_file_id=self.tg_file_id,
            attachment_type=self.attachment_type,
            caption=self.caption,
            date=self.date,
        )
