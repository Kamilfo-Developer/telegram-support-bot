import pytest
from app.answers.repo import AnswersRepo
from app.questions.repo import QuestionsRepo

from app.regular_users.entities import RegularUser
from app.regular_users.repo import RegularUsersRepo
from app.shared.value_objects import TgUserId
from app.support_users.repo import SupportUsersRepo


# TODO: Write tests for getting


@pytest.mark.asyncio
async def test_getting_regular_users(
    fill_db, regular_users_repo: RegularUsersRepo
):
    regular_users = await regular_users_repo.get_all()

    assert regular_users

    assert (
        await regular_users_repo.get_by_id(regular_users[0]._id)
        in regular_users
    )

    assert await regular_users_repo.get_by_tg_bot_user_id(
        regular_users[0].tg_bot_user_id
    )


@pytest.mark.asyncio
async def test_deleting_regular_users(
    fill_db,
    regular_users_repo: RegularUsersRepo,
    support_users_repo: SupportUsersRepo,
    questions_repo: QuestionsRepo,
    answers_repo: AnswersRepo,
):
    regular_user = (await regular_users_repo.get_all())[0]

    await regular_users_repo.delete(regular_user._id)

    all_questions = await questions_repo.get_all()
    all_regular_users = await regular_users_repo.get_all()
    all_answers = await answers_repo.get_all()
    all_support_users = await support_users_repo.get_all()

    assert all_regular_users != []
    assert all_questions == []
    assert all_support_users != []
    assert all_answers == []

    assert (await regular_users_repo.get_by_id(regular_user._id)) == None
    assert await questions_repo.get_by_regular_user_id(regular_user._id) == []


@pytest.mark.asyncio
async def test_deleting_all_regular_users(
    fill_db,
    regular_users_repo: RegularUsersRepo,
    support_users_repo: SupportUsersRepo,
    questions_repo: QuestionsRepo,
    answers_repo: AnswersRepo,
):
    await regular_users_repo.delete_all()

    all_questions = await questions_repo.get_all()
    all_regular_users = await regular_users_repo.get_all()
    all_answers = await answers_repo.get_all()
    all_support_users = await support_users_repo.get_all()

    assert all_regular_users == []
    assert all_questions == []
    assert all_support_users != []
    assert all_answers == []


# This test actually makes no sense since there are no properties
# that we'd really like to chagne so far
@pytest.mark.asyncio
async def test_update_regular_users(
    fill_db,
    regular_users_repo: RegularUsersRepo,
):
    regular_user = (await regular_users_repo.get_all())[0]

    assert regular_user

    new_tg_bot_user_id = TgUserId(123451363156)

    regular_user.tg_bot_user_id = new_tg_bot_user_id

    await regular_users_repo.update(regular_user)

    same_regular_user = await regular_users_repo.get_by_id(regular_user._id)

    assert (
        same_regular_user
        and same_regular_user.tg_bot_user_id == new_tg_bot_user_id
    )


@pytest.mark.asyncio
async def test_adding_regular_users(
    fill_db,
    regular_users_repo: RegularUsersRepo,
):
    regular_user = RegularUser.create(TgUserId(1234124))

    await regular_users_repo.add(regular_user)

    assert regular_user == await regular_users_repo.get_by_id(regular_user._id)

    assert regular_user in await regular_users_repo.get_all()
