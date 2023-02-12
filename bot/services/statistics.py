from __future__ import annotations
from bot.db.repositories.repository import Repo
from uuid import UUID


class GlobalStatistics:
    total_roles: int
    total_regular_users: int
    total_support_users: int
    total_questions: int
    total_unanswered_questions: int
    total_answered_questions: int
    total_answers: int
    total_questions_attachments: int
    total_answers_attachments: int
    total_useful_answers: int
    total_unuseful_answers: int
    total_unestimated_ansers: int

    @classmethod
    async def get_statistics(cls, repo: Repo) -> GlobalStatistics:
        statistics = GlobalStatistics()

        statistics.total_answered_questions = (
            await repo.count_answered_questions()
        )

        statistics.total_answers = await repo.count_all_answers()

        statistics.total_answers_attachments = (
            await repo.count_all_answers_attachments()
        )

        statistics.total_questions = await repo.count_all_questions()

        statistics.total_questions_attachments = (
            await repo.count_all_questions_attachments()
        )

        statistics.total_regular_users = await repo.count_all_regular_users()

        statistics.total_roles = await repo.count_all_roles()

        statistics.total_support_users = await repo.count_all_support_users()

        statistics.total_unanswered_questions = (
            await repo.count_unanswered_questions()
        )

        statistics.total_unuseful_answers = (
            await repo.count_all_unuseful_answers()
        )

        statistics.total_useful_answers = await repo.count_all_useful_answers()

        statistics.total_unestimated_ansers = (
            statistics.total_answers
            - statistics.total_useful_answers
            - statistics.total_unuseful_answers
        )

        return statistics


class RoleStatistics:
    total_users: int

    @classmethod
    async def get_statistics(cls, role_id: int, repo: Repo) -> RoleStatistics:
        statistics = RoleStatistics()

        statistics.total_users = await repo.count_support_users_with_role(
            role_id
        )

        return statistics


class SupportUserStatistics:
    useful_answers: int
    unuseful_answers: int
    total_answers: int
    unestimated_answers: int

    @classmethod
    async def get_statistics(
        cls, support_user_id: UUID, repo: Repo
    ) -> SupportUserStatistics:
        statistics = SupportUserStatistics()

        statistics.useful_answers = (
            await repo.count_support_user_useful_answers(support_user_id)
        )

        statistics.unuseful_answers = (
            await repo.count_support_user_unuseful_answers(support_user_id)
        )

        statistics.total_answers = await repo.count_support_user_answers(
            support_user_id
        )

        statistics.unestimated_answers = (
            statistics.total_answers
            - statistics.unuseful_answers
            - statistics.useful_answers
        )

        return statistics


class RegularUserStatistics:
    asked_questions: int
    answered_questions: int

    @classmethod
    async def get_statistics(
        cls, question_id: UUID, repo: Repo
    ) -> RegularUserStatistics:
        statistics = RegularUserStatistics()

        statistics.asked_questions = await repo.count_regular_users_questions(
            question_id
        )

        return statistics


class QuestionStatistics:
    total_answers: int
    total_attachments: int

    @classmethod
    async def get_statistics(
        cls, question_id: UUID, repo: Repo
    ) -> QuestionStatistics:
        statistics = QuestionStatistics()

        statistics.total_answers = await repo.count_question_answers(
            question_id
        )

        statistics.total_attachments = await repo.count_question_attachments(
            question_id
        )

        return statistics


class AnswerStatistics:
    total_attachments: int

    @classmethod
    async def get_statistics(
        cls, answer_id: UUID, repo: Repo
    ) -> AnswerStatistics:
        statistics = AnswerStatistics()

        statistics.total_attachments = await repo.count_answer_attachments(
            answer_id
        )

        return statistics
