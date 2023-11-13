from __future__ import annotations

from dataclasses import dataclass


from app.shared.dtos import (
    AnswerDTO,
    QuestionDTO,
    RegularUserDTO,
    SupportUserDTO,
)


@dataclass(frozen=True)
class AnswerEstimationInfo:
    answer_dto: AnswerDTO
    answered_question_dto: QuestionDTO
    support_user_dto: SupportUserDTO
    regular_user_dto: RegularUserDTO


@dataclass(frozen=True)
class AnswerEstimatedAsUsefulEvent:
    answer_dto: AnswerDTO
    question_dto: QuestionDTO
    support_user_answered: SupportUserDTO | None
    regular_user_asked: RegularUserDTO


@dataclass(frozen=True)
class AnswerEstimatedAsUnusefulEvent:
    answer_dto: AnswerDTO
    answered_question_dto: QuestionDTO
    support_user_answered: SupportUserDTO
    regular_user_asked: RegularUserDTO
