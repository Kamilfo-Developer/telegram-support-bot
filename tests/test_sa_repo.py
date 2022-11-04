from bot.entities.answer import Answer
from bot.entities.regular_user import RegularUser
from bot.entities.support_user import SupportUser
from tests.db_test_config import async_session
from bot.db.repositories.sa_repository import SARepo
from tests.utils_for_tests import (
    add_data,
    init_db,
    query_random_answered_question,
    query_random_regular_user,
    query_random_regular_user_with_questions,
    query_random_support_user_with_answered_questions,
    query_random_support_user,
    query_random_unanswered_question,
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
    assert type(answer) is Answer


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


@pytest.mark.asyncio
async def test_adding_support_user(create_models):
    repo = SARepo()

    roles = await repo.get_all_roles()

    new_support_user = await SupportUser.add_support_user(
        roles[0].id, 2352135235, SARepo
    )

    assert new_support_user == await repo.get_support_user_by_id(
        new_support_user.id
    )
    assert new_support_user in await repo.get_all_support_users()


@pytest.mark.asyncio
async def test_adding_questions(create_models):
    repo = SARepo()

    async with async_session() as session:
        user_model = await query_random_regular_user(session)

    regular_user = await RegularUser.get_regular_user_by_tg_bot_user_id(
        user_model.tg_bot_user_id, SARepo
    )

    question = await regular_user.ask_question(
        "Hello there!", 12423561345, SARepo
    )

    assert await repo.get_question_by_id(question.id) == question
    assert question in await repo.get_all_questions()


@pytest.mark.asyncio
async def test_adding_answers(create_models):
    repo = SARepo()

    async with async_session() as session:
        user_model = await query_random_support_user(session)
        question = await query_random_unanswered_question(session)

    support_user = await SupportUser.get_support_user_by_tg_bot_user_id(
        user_model.tg_bot_user_id, SARepo
    )

    await support_user.bind_question(question.id, SARepo)

    answer = await support_user.answer_current_question(
        "Hello there! Now you question is answered!", 12345678, SARepo
    )

    assert answer == await repo.get_answer_by_id(answer.id)
    assert answer in await repo.get_all_answers()
