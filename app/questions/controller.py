from app.questions.entities import Question
from app.questions.repo import QuestionsRepo
from app.shared.value_objects import (
    QuestionIdType,
    RegularUserIdType,
    TgMessageIdType,
    TgMessageText,
)


class QuestionsController:
    def __init__(self, questions_repo: QuestionsRepo) -> None:
        self.questions_repo = questions_repo

    async def delete_question(self, question_id: QuestionIdType) -> None:
        await self.questions_repo.delete(question_id)

    async def add_question(
        self,
        regular_user_id: RegularUserIdType,
        question_text: str,
        tg_message_id: TgMessageIdType,
    ) -> Question:
        question = Question.create(
            regular_user_id=regular_user_id,
            message=TgMessageText(question_text),
            tg_message_id=tg_message_id,
        )

        await self.questions_repo.add(question)

        return question

    async def get_all_questions(self) -> list[Question]:
        return await self.questions_repo.get_all()

    async def get_question(
        self, question_id: QuestionIdType
    ) -> Question | None:
        return await self.questions_repo.get_by_id(question_id)

    async def get_question_by_tg_message_id(
        self,
        tg_message_id: TgMessageIdType,
    ) -> Question | None:
        return await self.questions_repo.get_by_tg_message_id(tg_message_id)

    async def get_question_to_answer(self) -> Question | None:
        return await self.questions_repo.get_random_unanswered_unbound()

    async def get_regular_users_questions(
        self, regular_user_tg_id: RegularUserIdType
    ) -> list[Question]:
        return await self.questions_repo.get_by_regular_user_id(
            regular_user_tg_id
        )

    async def get_regular_user_last_question(
        self, regular_user_id: RegularUserIdType
    ) -> Question | None:
        return await self.questions_repo.get_last_asked(regular_user_id)

    async def update(self, question: Question) -> None:
        await self.questions_repo.update(question)
