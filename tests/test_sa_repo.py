from datetime import datetime
from sqlalchemy.orm import selectinload
from tests.db_test_config import async_session
from bot.db.models.sa.answer_model import AnswerModel
from bot.db.models.sa.question_model import QuestionModel
from bot.db.models.sa.support_user_model import SupportUserModel
from sqlalchemy.future import select
from bot.db.repositories.sa_repository import SARepo
from tests.utils_for_tests import (
    add_data,
    init_db,
    query_question_by_id,
    query_random_answered_question,
    query_random_question,
    query_random_regular_user_with_questions,
    query_random_support_user,
    query_random_support_user_with_answered_questions,
    query_support_user_by_id,
)
import pytest
import pytest_asyncio

init_db = init_db


@pytest_asyncio.fixture()
async def create_models(init_db):
    await add_data(async_session)
    print("\n\nMODELS CREATED\n\n")


@pytest.mark.asyncio
async def test_getting_answers(create_models):
    async with async_session() as session:
        question = await query_random_answered_question(session)

    repo = SARepo()

    all_answers = await repo.get_all_answers()

    answers_with_question_id = await repo.get_answers_with_question_id(
        question.id
    )

    answer = await repo.get_answer_by_id(all_answers[0].id)

    assert len(all_answers) != 0
    assert len(answers_with_question_id) != 0
    assert type(answer) is AnswerModel


@pytest.mark.asyncio
async def test_adding_answers(create_models):
    repo = SARepo()

    async with async_session() as session:
        question = await query_random_question(session)

        support_user = await query_random_support_user(session)

    answer1 = AnswerModel(
        message="Test message number1 for sa_answers_repo",
        tg_message_id=123123123,
        date=datetime(2022, 9, 8),
    )

    answer2 = AnswerModel(
        message="Test message number2 for sa_answers_repo",
        tg_message_id=123125523,
        date=datetime(2022, 9, 9),
    )

    await repo.add_answer_to_question(
        answer1,
        question,
        support_user,
    )

    await repo.add_answer_to_question(
        answer2,
        question,
        support_user,
    )

    async with async_session() as session:
        question = await query_question_by_id(session, question.id)

        support_user = await query_support_user_by_id(session, support_user.id)

        q = select(AnswerModel).where(AnswerModel.id == answer1.id)

        answer1 = (await session.execute(q)).scalars().first()

        q = select(AnswerModel).where(AnswerModel.id == answer2.id)

        answer2 = (await session.execute(q)).scalars().first()

        assert answer1 in question.answers
        assert answer1 in support_user.answers
        assert answer2 in question.answers
        assert answer2 in support_user.answers


@pytest.mark.asyncio
async def test_deleting_answers(create_models):
    repo = SARepo()

    async with async_session() as session:
        question = await query_random_question(session)

        support_user = await query_random_support_user(session)

    answer1 = AnswerModel(
        message="Test message number1 for sa_answers_repo",
        tg_message_id=123123123,
        date=datetime(2022, 9, 8),
    )

    answer2 = AnswerModel(
        message="Test message number2 for sa_answers_repo",
        tg_message_id=123125523,
        date=datetime(2022, 9, 9),
    )

    await repo.add_answer_to_question(
        answer1,
        question,
        support_user,
    )

    await repo.add_answer_to_question(
        answer2,
        question,
        support_user,
    )

    await repo.delete_answer_with_id(answer1.id)

    async with async_session() as session:
        question = await query_question_by_id(session, question.id)

        support_user = await query_support_user_by_id(session, support_user.id)

        q = select(AnswerModel).where(AnswerModel.id == answer1.id)

        answer1 = (await session.execute(q)).scalars().first()

        q = select(AnswerModel).where(AnswerModel.id == answer2.id)

        answer2 = (await session.execute(q)).scalars().first()

        question = await query_question_by_id(session, question.id)

        assert answer1 not in question.answers
        assert answer1 not in support_user.answers

    await repo.delete_answers_with_question_id(question.id)

    async with async_session() as session:
        question = await query_question_by_id(session, question.id)

        assert question.answers == []

    await repo.delete_all_answers()

    async with async_session() as session:
        q = select(AnswerModel)

        answers = (await session.execute(q)).scalars().all()

        assert answers == []

        q = select(QuestionModel).options(selectinload(QuestionModel.answers))

        questions = (await session.execute(q)).scalars().all()

        for question in questions:
            assert question.answers == []

        q = select(SupportUserModel).options(
            selectinload(SupportUserModel.answers)
        )

        support_users = (await session.execute(q)).scalars().all()

        for support_user in support_users:
            assert support_user.answers == []


@pytest.mark.asyncio
async def test_deleting_questions(create_models):
    repo = SARepo()

    await repo.delete_all_questions()

    assert await repo.get_all_answers() == []


@pytest.mark.asyncio
async def test_deleting_regular_users(create_models):
    repo = SARepo()

    async with async_session() as session:
        regular_user = await query_random_regular_user_with_questions(session)

    await repo.delete_regular_user_with_id(regular_user.id)

    all_questions = await repo.get_all_questions()
    all_regular_users = await repo.get_all_regular_users()
    all_answers = await repo.get_all_answers()
    all_support_users = await repo.get_all_support_users()

    assert all_regular_users != []
    assert all_questions != []
    assert all_support_users != []
    assert all_answers != []

    assert (await repo.get_support_user_by_id(regular_user.id)) == None
    assert await repo.get_questions_with_regular_user_id(regular_user.id) == []


@pytest.mark.asyncio
async def test_deleting_all_support_users(create_models):
    repo = SARepo()

    all_questions = await repo.get_all_questions()
    all_regular_users = await repo.get_all_regular_users()
    all_answers = await repo.get_all_answers()
    all_support_users = await repo.get_all_support_users()

    assert all_regular_users != []
    assert all_questions != []
    assert all_answers != []
    assert all_support_users != []

    await repo.delete_all_support_users()

    all_questions = await repo.get_all_questions()
    all_regular_users = await repo.get_all_regular_users()
    all_answers = await repo.get_all_answers()
    all_support_users = await repo.get_all_support_users()

    assert all_support_users == []
    assert all_regular_users != []
    assert all_questions != []
    assert all_answers == []


@pytest.mark.asyncio
async def test_deleting_support_users_by_id(create_models):
    repo = SARepo()

    async with async_session() as session:
        support_user = await query_random_support_user_with_answered_questions(
            session
        )

    await repo.delete_support_user_with_id(support_user.id)

    all_questions = await repo.get_all_questions()
    all_regular_users = await repo.get_all_regular_users()
    all_answers = await repo.get_all_answers()
    all_support_users = await repo.get_all_support_users()

    assert all_regular_users != []
    assert all_questions != []
    assert all_support_users != []
    assert all_answers != []

    assert (await repo.get_support_user_by_id(support_user.id)) == None
    assert await repo.get_support_user_answers_with_id(support_user.id) == []
