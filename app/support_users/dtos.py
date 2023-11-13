from __future__ import annotations

from dataclasses import dataclass

from app.shared.dtos import (
    AnswerDTO,
    AttachmentDTO,
    QuestionDTO,
    RegularUserDTO,
    RoleDTO,
    SupportUserDTO,
)
from app.statistics.dtos import (
    AnswerStatistics,
    QuestionStatistics,
    RegularUserStatistics,
    RoleStatistics,
    SupportUserStatistics,
)


@dataclass(frozen=True)
class RegularUserInfo:
    regular_user_dto: RegularUserDTO
    statistics: RegularUserStatistics


@dataclass(frozen=True)
class RoleInfo:
    role_dto: RoleDTO
    statistics: RoleStatistics


@dataclass(frozen=True)
class QuestionInfo:
    question_dto: QuestionDTO
    regular_user_asked_dto: RegularUserDTO
    statistics: QuestionStatistics


@dataclass(frozen=True)
class SupportUserInfo:
    support_user_dto: SupportUserDTO
    statistics: SupportUserStatistics


@dataclass(frozen=True)
class AnswerInfo:
    answer_dto: AnswerDTO
    answered_quetsion_dto: QuestionDTO
    support_user_answered_dto: SupportUserDTO
    statistics: AnswerStatistics


@dataclass(frozen=True)
class AnswerAttachmentSentEvent:
    attachment_dto: AttachmentDTO
    support_user_answered: SupportUserDTO
    regular_user_asked: RegularUserDTO


@dataclass(frozen=True)
class QuestionWasAnsweredEvent:
    question_dto: QuestionDTO
    answer_dto: AnswerDTO
    regular_user_asked_dto: RegularUserDTO
