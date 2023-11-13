from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Self

from app.answers.entities import Answer
from app.questions.entities import Question
from app.regular_users.entities import RegularUser
from app.roles.entities import Role
from app.roles.value_objects import RoleDescription, RoleName
from app.shared.entities import Attachment
from app.shared.value_objects import (
    AnswerIdType,
    QuestionIdType,
    RegularUserIdType,
    RoleIdType,
    RolePermissions,
    SupportUserIdType,
    TgCaption,
    TgFileIdType,
    TgMessageIdType,
    TgMessageText,
    TgUserId,
)
from app.support_users.entities import SupportUser
from app.support_users.value_objects import DescriptiveName
from app.utils import TgFileType


@dataclass(frozen=True)
class AttachmentDTO:
    tg_file_id: TgFileIdType
    attachment_type: TgFileType
    caption: TgCaption | None
    date: datetime

    @classmethod
    def from_entity(cls, attachment_entity: Attachment) -> Self:
        return cls(
            tg_file_id=attachment_entity.tg_file_id,
            attachment_type=attachment_entity.attachment_type,
            caption=attachment_entity.caption,
            date=attachment_entity.date,
        )


@dataclass(frozen=True)
class RegularUserDTO:
    id: RegularUserIdType
    tg_bot_id: int
    join_date: datetime

    @classmethod
    def from_entity(cls, regular_user_entity: RegularUser) -> Self:
        return cls(
            id=regular_user_entity._id,
            tg_bot_id=regular_user_entity.tg_bot_user_id,
            join_date=regular_user_entity.join_date,
        )


@dataclass(frozen=True)
class RoleDTO:
    id: RoleIdType
    name: RoleName
    description: RoleDescription
    permissions: RolePermissions
    created_date: datetime

    @classmethod
    def from_entity(cls, role_entity: Role) -> Self:
        return cls(
            id=role_entity._id,  # type: ignore
            name=role_entity.name,
            description=role_entity.description,
            permissions=role_entity.permissions,
            created_date=role_entity.created_date,
        )


@dataclass(frozen=True)
class QuestionDTO:
    id: QuestionIdType
    regular_user_id: RegularUserIdType
    message: TgMessageText
    tg_message_id: TgMessageIdType
    date: datetime

    @classmethod
    def from_entity(cls, question_entity: Question) -> Self:
        return cls(
            id=question_entity._id,
            regular_user_id=question_entity.regular_user_id,
            message=question_entity.message,
            tg_message_id=question_entity.tg_message_id,
            date=question_entity.date,
        )


@dataclass(frozen=True)
class AnswerDTO:
    id: AnswerIdType
    support_user_id: SupportUserIdType
    question_id: QuestionIdType
    message: TgMessageText
    tg_message_id: TgMessageIdType
    is_useful: bool | None
    date: datetime

    @classmethod
    def from_entity(cls, answer_entity: Answer) -> Self:
        return cls(
            id=answer_entity._id,
            question_id=answer_entity.question_id,
            support_user_id=answer_entity.support_user_id,
            message=answer_entity.message,
            tg_message_id=answer_entity.tg_message_id,
            is_useful=answer_entity.is_useful,
            date=answer_entity.date,
        )


@dataclass(frozen=True)
class SupportUserDTO:
    id: SupportUserIdType
    tg_bot_id: TgUserId
    descriptive_name: DescriptiveName
    role: SupportUserRoleDTO | None
    bound_question_id: QuestionIdType | None
    is_owner: bool
    is_active: bool
    join_date: datetime

    @classmethod
    def from_entity(cls, support_user_entity: SupportUser) -> Self:
        return cls(
            id=support_user_entity._id,
            tg_bot_id=support_user_entity.tg_bot_user_id,
            descriptive_name=support_user_entity.descriptive_name,
            role=(
                SupportUserRoleDTO(
                    support_user_entity.role._id,
                    support_user_entity.role.permissions,
                )
                if support_user_entity.role
                else None
            ),
            bound_question_id=support_user_entity.current_question_id,
            is_owner=support_user_entity.is_active,
            is_active=support_user_entity.is_active,
            join_date=support_user_entity.join_date,
        )


@dataclass(frozen=True)
class SupportUserRoleDTO:
    id: RoleIdType
    permissions: RolePermissions
