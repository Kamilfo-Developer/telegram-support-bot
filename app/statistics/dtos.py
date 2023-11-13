from dataclasses import dataclass


@dataclass(frozen=True)
class RoleStatistics:
    total_users: int


@dataclass(frozen=True)
class RegularUserStatistics:
    asked_questions: int
    answered_questions: int
    unanswered_questions: int
    answers_for_questions: int
    unestimated_answers: int
    useful_answers: int
    unuseful_answers: int


@dataclass(frozen=True)
class QuestionStatistics:
    total_answers: int
    total_attachments: int


@dataclass(frozen=True)
class AnswerStatistics:
    total_attachments: int


@dataclass(frozen=True)
class SupportUserStatistics:
    useful_answers: int
    unuseful_answers: int
    unestimated_answers: int
    total_answers: int


@dataclass(frozen=True)
class GlobalStatistics:
    total_roles: int
    total_regular_users: int
    total_support_users: int
    total_questions: int
    total_unanswered_questions: int
    total_answered_questions: int
    total_answers: int
    total_question_attachments: int
    total_answer_attachments: int
    total_useful_answers: int
    total_unuseful_answers: int
    total_unestimated_answers: int
