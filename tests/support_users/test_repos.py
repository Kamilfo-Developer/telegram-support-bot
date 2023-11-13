from app.answers.repo import AnswersRepo
from app.questions.repo import QuestionsRepo
from app.regular_users.repo import RegularUsersRepo
from app.roles.repo import RolesRepo
from app.shared.value_objects import TgUserId
from app.support_users.entities import SupportUser, SupportUserRole
import pytest
from app.support_users.repo import SupportUsersRepo
from app.support_users.value_objects import DescriptiveName


# TODO: Write tests for getting


@pytest.mark.asyncio
async def test_deleting_all_support_users(
    fill_db,
    regular_users_repo: RegularUsersRepo,
    support_users_repo: SupportUsersRepo,
    roles_repo: RolesRepo,
    questions_repo: QuestionsRepo,
    answers_repo: AnswersRepo,
):
    all_questions = await questions_repo.get_all()
    all_regular_users = await regular_users_repo.get_all()
    all_answers = await answers_repo.get_all()
    all_support_users = await support_users_repo.get_all()
    all_roles = await roles_repo.get_all()

    assert all_regular_users != []
    assert all_questions != []
    assert all_answers != []
    assert all_support_users != []
    assert all_roles != []

    await support_users_repo.delete_all()

    all_questions = await questions_repo.get_all()
    all_regular_users = await regular_users_repo.get_all()
    all_answers = await answers_repo.get_all()
    all_support_users = await support_users_repo.get_all()
    all_roles = await roles_repo.get_all()

    assert all_support_users == []
    assert all_regular_users != []
    assert all_questions != []
    assert all_answers == []


@pytest.mark.asyncio
async def test_deleting_support_users_by_id(
    fill_db,
    regular_users_repo: RegularUsersRepo,
    support_users_repo: SupportUsersRepo,
    roles_repo: RolesRepo,
    questions_repo: QuestionsRepo,
    answers_repo: AnswersRepo,
):
    support_user = (await support_users_repo.get_all())[0]

    await support_users_repo.delete(support_user._id)

    all_questions = await questions_repo.get_all()
    all_regular_users = await regular_users_repo.get_all()
    all_answers = await answers_repo.get_all()
    all_support_users = await support_users_repo.get_all()
    all_roles = await roles_repo.get_all()

    assert all_regular_users != []
    assert all_questions != []
    assert all_support_users != []
    assert all_answers != []
    assert all_roles != []

    assert (await support_users_repo.get_by_id(support_user._id)) == None
    assert await answers_repo.get_by_support_user_id(support_user._id) == []


@pytest.mark.asyncio
async def test_adding_support_user(
    fill_db,
    support_users_repo: SupportUsersRepo,
    roles_repo: RolesRepo,
):
    roles = await roles_repo.get_all()

    new_support_user = SupportUser.create(
        DescriptiveName("Joe"),
        TgUserId(123456231),
        SupportUserRole(roles[0]._id, roles[0].permissions),
    )

    await support_users_repo.add(new_support_user)

    assert new_support_user == await support_users_repo.get_by_id(
        new_support_user._id
    )
    assert new_support_user in await support_users_repo.get_all()


# FIXME: Attantion, really bad code is following,
# it should be thrown away and changed by a better solution
# NOTE: It'd look much better if we move the logic for
# initial getting entities to fixtures


@pytest.mark.asyncio
async def test_updating_roles(
    fill_db,
    support_users_repo: SupportUsersRepo,
    roles_repo: RolesRepo,
    questions_repo: QuestionsRepo,
):
    all_support_users = await support_users_repo.get_all()

    support_user = None

    for elem in all_support_users:
        if not elem.is_owner:
            support_user = elem
            break

    assert support_user

    roles = await roles_repo.get_all()

    new_role = None

    for role in roles:
        if role.permissions.can_answer_questions and (
            not support_user.role or support_user.role._id != role._id
        ):
            new_role = SupportUserRole(role._id, role.permissions)
            break

    assert new_role

    new_desriptive_name = DescriptiveName("A new descriptive name")

    support_user.descriptive_name = new_desriptive_name

    support_user.assign_role(new_role)

    await support_users_repo.update(support_user)

    same_support_user = await support_users_repo.get_by_id(support_user._id)

    assert same_support_user

    assert support_user is not None

    new_question = await questions_repo.get_random_unanswered_unbound()

    assert new_question

    same_support_user.bind_question(new_question._id)

    await support_users_repo.update(same_support_user)

    same_support_user = await support_users_repo.get_by_id(support_user._id)

    assert same_support_user

    assert same_support_user.current_question_id == new_question._id
