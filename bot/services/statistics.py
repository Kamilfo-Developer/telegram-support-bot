from bot.db.repositories.repository import Repo


class Statistics:
    def __init__(self, repo: Repo) -> None:
        self.repo = repo

    async def count_all_roles(self) -> int:
        total_roles = await self.repo.count_all_roles()
        return total_roles

    async def count_all_regular_users(self) -> int:
        total_regular_users = await self.repo.count_all_regular_users()
        return total_regular_users

    async def count_all_support_users(self) -> int:
        total_support_users = await self.repo.count_all_support_users()
        return total_support_users

    async def count_all_questions(self) -> int:
        total_questions = await self.repo.count_all_questions()
        return total_questions

    async def count_all_unanswered_questions(self) -> int:
        total_unanswered_questions = (
            await self.repo.count_unanswered_questions()
        )
        return total_unanswered_questions

    async def count_all_answered_questions(self) -> int:
        total_answered_questions = await self.repo.count_answered_questions()
        return total_answered_questions

    async def count_all_answers(self) -> int:
        total_answers = await self.repo.count_all_answers()
        return total_answers
