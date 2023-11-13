# TODO: Write all tests
import pytest
from app.answers.entities import Answer
from app.answers.repo import AnswersRepo

from app.questions.repo import QuestionsRepo
from app.regular_users.repo import RegularUsersRepo


from app.shared.value_objects import (
    TgCaption,
    TgFileIdType,
    TgMessageIdType,
    TgMessageText,
)
from app.support_users.repo import SupportUsersRepo
from app.utils import TgFileType, is_sub_list


# TODO: Write tests for getting


@pytest.mark.asyncio
async def test_getting_answers(
    fill_db,
    support_users_repo: SupportUsersRepo,
    questions_repo: QuestionsRepo,
    answers_repo: AnswersRepo,
):
    question = await questions_repo.get_random_answered()

    assert question

    all_answers = await answers_repo.get_all()

    assert await answers_repo.get_by_id(all_answers[0]._id) in all_answers

    assert is_sub_list(
        await answers_repo.get_by_question_id(question._id), all_answers
    )

    assert (
        await answers_repo.get_by_tg_message_id(all_answers[0].tg_message_id)
        in all_answers
    )

    support_users = await support_users_repo.get_all()

    for support_user in support_users:
        answers = await answers_repo.get_by_support_user_id(support_user._id)
        assert is_sub_list(answers, all_answers)

    assert (
        await answers_repo.get_question_last_answer(question._id)
        in all_answers
    )


@pytest.mark.asyncio
async def test_deleting_answers(
    fill_db,
    support_users_repo: SupportUsersRepo,
    questions_repo: QuestionsRepo,
    answers_repo: AnswersRepo,
    regular_users_repo: RegularUsersRepo,
):
    answers = await answers_repo.get_all()

    assert len(answers) > 0

    answer = answers[0]

    all_questions_before_deletion = await questions_repo.get_all()
    all_regular_users_before_deletion = await regular_users_repo.get_all()
    all_support_users_before_deletion = await support_users_repo.get_all()

    await answers_repo.delete(answer._id)

    all_questions = await questions_repo.get_all()
    all_regular_users = await regular_users_repo.get_all()
    all_answers = await answers_repo.get_all()
    all_support_users = await support_users_repo.get_all()

    assert all_regular_users == all_regular_users_before_deletion
    assert all_questions == all_questions_before_deletion
    assert all_support_users == all_support_users_before_deletion
    assert answer not in all_answers

    assert (await answers_repo.get_by_id(answer._id)) == None


@pytest.mark.asyncio
async def test_deleting_all_answers(
    fill_db,
    support_users_repo: SupportUsersRepo,
    questions_repo: QuestionsRepo,
    answers_repo: AnswersRepo,
    regular_users_repo: RegularUsersRepo,
):
    await answers_repo.delete_all()

    all_questions = await questions_repo.get_all()
    all_regular_users = await regular_users_repo.get_all()
    all_answers = await answers_repo.get_all()
    all_support_users = await support_users_repo.get_all()

    assert all_regular_users != []
    assert all_questions != []
    assert all_support_users != []
    assert all_answers == []


# This test actually makes no sense since there are no properties
# that we'd really like to chagne so far
@pytest.mark.asyncio
async def test_update_answers(fill_db, answers_repo: AnswersRepo):
    answers = await answers_repo.get_all()

    assert len(answers) > 0

    answer = answers[0]

    new_message = TgMessageText("A new message for answers testing")

    answer.message = new_message

    new_is_useful_status = not bool(answer.is_useful)

    if answer.is_useful is None:
        answer.estimate_as_useful()
    elif answer.is_useful:
        answer.estimate_as_unuseful()
    else:
        answer.estimate_as_useful()

    answer.add_attachment(
        TgFileIdType("1234sdf"),
        TgFileType.VIDEO,
        TgCaption("Here I described some important things but not really"),
    )

    attachments = answer.attachments

    await answers_repo.update(answer)

    answer = await answers_repo.get_by_id(answer._id)  # type: ignore # noqa: E501

    assert answer

    assert attachments == answer.attachments

    assert answer.is_useful == new_is_useful_status

    assert answer.message == new_message


@pytest.mark.asyncio
async def test_adding_regular_users(
    fill_db,
    support_users_repo: SupportUsersRepo,
    questions_repo: QuestionsRepo,
    answers_repo: AnswersRepo,
):
    support_user = (await support_users_repo.get_all())[0]

    assert support_user

    question = await questions_repo.get_random_unbound()

    assert question

    answer = Answer.create(
        support_user_id=support_user._id,
        question_id=question._id,
        message=TgMessageText("An answer"),
        tg_message_id=TgMessageIdType(61423612346),
    )

    await answers_repo.add(answer)

    assert answer == await answers_repo.get_by_id(answer._id)
    assert answer in await answers_repo.get_all()
