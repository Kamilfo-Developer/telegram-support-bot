from app.answers.entities import Answer
from app.answers.repo import AnswersRepo
from app.errors import NoSuchEntityError
from app.shared.value_objects import (
    AnswerIdType,
    QuestionIdType,
    SupportUserIdType,
    TgCaption,
    TgFileIdType,
    TgMessageIdType,
    TgMessageText,
)
from app.utils import TgFileType


class AnswersController:
    def __init__(self, answers_repo: AnswersRepo) -> None:
        self.answers_repo = answers_repo

    async def delete_answer(self, answer_id: AnswerIdType) -> None:
        await self.answers_repo.delete(answer_id)

    async def add_answer(
        self,
        support_user_id: SupportUserIdType,
        question_id: QuestionIdType,
        answer_text: TgMessageText,
        tg_message_id: TgMessageIdType,
    ) -> Answer:
        answer = Answer.create(
            support_user_id=support_user_id,
            question_id=question_id,
            message=answer_text,
            tg_message_id=tg_message_id,
        )

        await self.answers_repo.add(answer)

        return answer

    async def add_attachment(
        self,
        answer_id: AnswerIdType,
        tg_file_id: TgFileIdType,
        attachment_type: TgFileType,
        caption: TgCaption,
    ) -> None:
        answer = await self.answers_repo.get_by_id(answer_id)

        if not answer:
            raise NoSuchEntityError()

        answer.add_attachment(
            tg_file_id=tg_file_id,
            attachment_type=attachment_type,
            caption=caption,
        )

        await self.answers_repo.update(answer=answer)

    async def get_all_answers(self) -> list[Answer]:
        return await self.answers_repo.get_all()

    async def get_answer(self, answer_id: AnswerIdType) -> Answer | None:
        return await self.answers_repo.get_by_id(answer_id)

    async def get_last_answer_for_question(
        self, question_id: QuestionIdType
    ) -> Answer | None:
        return await self.answers_repo.get_question_last_answer(question_id)

    async def get_answer_by_tg_message_id(
        self, tg_message_id: TgMessageIdType
    ) -> Answer | None:
        return await self.answers_repo.get_by_tg_message_id(tg_message_id)

    async def get_answers_by_question_id(
        self, question_id: QuestionIdType
    ) -> list[Answer]:
        return await self.answers_repo.get_by_question_id(question_id)

    async def update_answer(self, answer: Answer) -> None:
        await self.answers_repo.update(answer)
