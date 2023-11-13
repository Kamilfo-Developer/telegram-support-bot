from __future__ import annotations

from app.answers.repo import AnswersRepo
from app.errors import NoLastQuestionError, NoSuchAnswer
from app.questions.entities import Question
from app.questions.repo import QuestionsRepo
from app.regular_users.dtos import (
    AnswerEstimatedAsUnusefulEvent,
    AnswerEstimatedAsUsefulEvent,
    RegularUserDTO,
)
from app.regular_users.entities import RegularUser
from app.regular_users.queries import RegularUsersQueriesFactory
from app.regular_users.repo import RegularUsersRepo
from app.shared.dtos import AttachmentDTO, QuestionDTO
from app.shared.value_objects import (
    TgCaption,
    TgFileIdType,
    TgMessageIdType,
    TgMessageText,
    TgUserId,
)
from app.statistics.service import StatisticsService
from app.support_users.dtos import RegularUserInfo
from app.utils import TgFileType


class RegularUserController:
    def __init__(
        self,
        regular_users_repo: RegularUsersRepo,
        questions_repo: QuestionsRepo,
        answers_repo: AnswersRepo,
        statistics_service: StatisticsService,
        regular_users_queries_factory: RegularUsersQueriesFactory,
    ) -> None:
        self.__regular_users_repo = regular_users_repo
        self.__questions_repo = questions_repo
        self.__answers_repo = answers_repo
        self.__statistics_service = statistics_service
        self.__regular_users_queries_factory = regular_users_queries_factory

    async def authorize_regular_user(
        self, regular_user_tg_id: TgUserId
    ) -> RegularUser:
        regular_user = await self.__get_regular_user(regular_user_tg_id)

        if not regular_user:
            regular_user = await self.__add_regular_user(regular_user_tg_id)

        return regular_user

    async def get_own_regular_user_info(
        self, regular_user: RegularUser
    ) -> RegularUserInfo:
        regular_user_statistics = (
            await self.__statistics_service.get_regular_user_statistics(
                regular_user._id
            )
        )

        return RegularUserInfo(
            regular_user_dto=RegularUserDTO.from_entity(regular_user),
            statistics=regular_user_statistics,
        )

    async def __get_regular_user(
        self, regular_user_id: TgUserId
    ) -> RegularUser | None:
        return await self.__regular_users_repo.get_by_tg_bot_user_id(
            regular_user_id
        )

    async def __add_regular_user(
        self, regular_user_tg_id: TgUserId
    ) -> RegularUser:
        regular_user = RegularUser.create(regular_user_tg_id)

        return await self.__regular_users_repo.add(regular_user)

    async def ask_question(
        self,
        regular_user: RegularUser,
        question_text: TgMessageText,
        message_id: TgMessageIdType,
    ) -> QuestionDTO:
        question = await self.__questions_repo.add(
            Question.create(
                regular_user._id,
                question_text,
                message_id,
            )
        )

        return QuestionDTO.from_entity(question)

    async def estimate_answer_as_useful(
        self, regular_user: RegularUser, answer_tg_message_id: TgMessageIdType
    ) -> AnswerEstimatedAsUsefulEvent:
        answer = await self.__answers_repo.get_by_tg_message_id(
            TgMessageIdType(answer_tg_message_id)
        )

        if not answer:
            raise NoSuchAnswer()

        answer.estimate_as_useful()

        await self.__answers_repo.update(answer)

        answer_estimation_info_query = (
            self.__regular_users_queries_factory.create_answer_estimation_info_query()  # noqa: E501
        )

        answer_estimation_info = await answer_estimation_info_query.execute(
            answer._id
        )

        if not answer_estimation_info:
            raise NoSuchAnswer()

        return AnswerEstimatedAsUsefulEvent(
            answer_estimation_info.answer_dto,
            answer_estimation_info.answered_question_dto,
            answer_estimation_info.support_user_dto,
            answer_estimation_info.regular_user_dto,
        )

    async def estimate_answer_as_unuseful(
        self, regular_user: RegularUser, answer_tg_message_id: int
    ) -> AnswerEstimatedAsUnusefulEvent:
        answer = await self.__answers_repo.get_by_tg_message_id(
            TgMessageIdType(answer_tg_message_id)
        )

        if not answer:
            raise NoSuchAnswer()

        answer.estimate_as_unuseful()

        await self.__answers_repo.update(answer)

        answer_estimation_info_query = (
            self.__regular_users_queries_factory.create_answer_estimation_info_query()  # noqa: E501
        )

        answer_estimation_info = await answer_estimation_info_query.execute(
            answer._id
        )

        if not answer_estimation_info:
            raise NoSuchAnswer()

        return AnswerEstimatedAsUnusefulEvent(
            answer_estimation_info.answer_dto,
            answer_estimation_info.answered_question_dto,
            answer_estimation_info.support_user_dto,
            answer_estimation_info.regular_user_dto,
        )

    async def add_attachment_to_last_asked_question(
        self,
        regular_user: RegularUser,
        tg_file_id: TgFileIdType,
        attachment_type: TgFileType,
        caption: TgCaption | None,
    ) -> AttachmentDTO:
        last_question = await self.__questions_repo.get_last_asked(
            regular_user._id
        )

        if not last_question:
            raise NoLastQuestionError()

        last_question.add_attachment(
            TgFileIdType(tg_file_id),
            attachment_type,
            caption=caption,
        )

        await self.__questions_repo.update(last_question)

        return AttachmentDTO.from_entity(last_question.attachments[-1])

    async def get_answer_attachments(
        self, regular_user: RegularUser, answer_tg_id: TgMessageIdType
    ) -> list[AttachmentDTO]:
        answer = await self.__answers_repo.get_by_tg_message_id(answer_tg_id)

        if not answer:
            raise NoSuchAnswer()

        return [
            AttachmentDTO.from_entity(attachment)
            for attachment in answer.attachments
        ]
