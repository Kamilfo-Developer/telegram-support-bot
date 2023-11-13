import pytest
from app.answers.repo import AnswersRepo

from app.questions.entities import Question
from app.questions.repo import QuestionsRepo
from app.regular_users.repo import RegularUsersRepo
from app.shared.value_objects import (
    TgCaption,
    TgFileIdType,
    TgMessageIdType,
    TgMessageText,
)
from app.utils import TgFileType, is_sub_list


@pytest.mark.asyncio
async def test_getting_questions(fill_db, questions_repo: QuestionsRepo):
    all_questions = await questions_repo.get_all()

    assert await questions_repo.get_all() != []

    assert await questions_repo.get_random_answered() in all_questions

    assert (
        await questions_repo.get_by_tg_message_id(
            all_questions[0].tg_message_id
        )
        in all_questions
    )

    assert is_sub_list(
        await questions_repo.get_by_regular_user_id(
            all_questions[0].regular_user_id
        ),
        all_questions,
    )

    assert (
        await questions_repo.get_last_asked(all_questions[0].regular_user_id)
        in all_questions
    )

    assert await questions_repo.get_random_answered() in all_questions

    assert (
        await questions_repo.get_random_unanswered_unbound() in all_questions
    )

    assert await questions_repo.get_random_unbound() in all_questions

    assert is_sub_list(
        await questions_repo.get_unanswered(),
        all_questions,
    )

    assert is_sub_list(await questions_repo.get_unbound(), all_questions)

    assert (
        await questions_repo.get_by_id(all_questions[0]._id) in all_questions
    )


@pytest.mark.asyncio
async def test_deleting_all_questions(fill_db, questions_repo: QuestionsRepo):
    await questions_repo.delete_all()

    assert await questions_repo.get_all() == []


@pytest.mark.asyncio
async def test_deleting_questions(
    fill_db, questions_repo: QuestionsRepo, answers_repo: AnswersRepo
):
    answered_question = await questions_repo.get_random_answered()

    assert answered_question

    await questions_repo.delete(answered_question._id)

    assert await questions_repo.get_by_id(answered_question._id) is None

    assert await answers_repo.get_by_question_id(answered_question._id) == []


@pytest.mark.asyncio
async def test_updating_questions(fill_db, questions_repo: QuestionsRepo):
    question = (await questions_repo.get_all())[0]

    new_message = TgMessageText("A new message for questions testing")

    question.message = new_message

    question.add_attachment(
        TgFileIdType("1234sdf"),
        TgFileType.VOICE,
        TgCaption("Here I described some important things"),
    )

    attachments = question.attachments

    await questions_repo.update(question)

    question = await questions_repo.get_by_id(question._id)  # type: ignore # noqa: E501

    assert question

    assert attachments == question.attachments


@pytest.mark.asyncio
async def test_adding_questions(
    fill_db,
    questions_repo: QuestionsRepo,
    regular_users_repo: RegularUsersRepo,
):
    regular_user = (await regular_users_repo.get_all())[0]

    question = Question.create(
        regular_user._id,
        TgMessageText("Just wanted to ask you for a date"),
        TgMessageIdType(123456),
    )

    await questions_repo.add(question)

    assert await questions_repo.get_by_id(question._id) == question
    assert question in await questions_repo.get_all()
