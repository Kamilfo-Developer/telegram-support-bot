from datetime import datetime
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import func, delete
from tests.db_test_config import async_session
from bot.db.models.answer_model import AnswerModel
from bot.db.models.question_model import QuestionModel
from bot.db.models.regular_user_model import RegularUserModel
from bot.db.models.role_model import RoleModel
from bot.db.models.support_user_model import SupportUserModel
from bot.db.models.user_model import UserModel
from sqlalchemy.future import select
from tests.utils_for_tests import add_data, init_db
import pytest
import pytest_asyncio

init_db = init_db


@pytest_asyncio.fixture()
async def create_models(init_db):
    await add_data(async_session)
    print("\n\nMODELS CREATED\n\n")


@pytest.mark.asyncio
async def test_adding_questions(create_models):

    async with async_session() as session:
        q = select(RegularUserModel).options(
            selectinload(RegularUserModel.questions)
        )

        regular_user = (await session.execute(q)).scalars().first()

        new_question = QuestionModel(
            tg_message_id=3255511212,
            message="A new question goes here...",
            date=datetime(2022, 4, 19),
        )

        regular_user.questions.append(new_question)

        await session.commit()

        q = (
            select(RegularUserModel)
            .where(RegularUserModel.id == regular_user.id)
            .options(selectinload(RegularUserModel.questions))
        )

        new_result = (await session.execute(q)).scalars().first()

        assert new_question in new_result.questions


async def query_question(
    session: AsyncSession, id: UUID = None
) -> QuestionModel:
    if id:
        q = (
            select(QuestionModel)
            .where(QuestionModel.id == id)
            .options(selectinload(QuestionModel.answers))
        )

        return (await session.execute(q)).scalars().first()

    q = (
        select(QuestionModel)
        .where(QuestionModel.current_support_user == None)
        .where(QuestionModel.answers == None)
        .options(selectinload(QuestionModel.answers))
    )

    return (await session.execute(q)).scalars().first()


async def query_support_user(
    session: AsyncSession, id: UUID = None
) -> SupportUserModel:
    if id:
        q = (
            select(SupportUserModel)
            .where(SupportUserModel.id == id)
            .options(
                selectinload(SupportUserModel.answers),
                selectinload(SupportUserModel.current_question),
            )
        )

        return (await session.execute(q)).scalars().first()

    q = select(SupportUserModel).options(
        selectinload(SupportUserModel.answers),
        selectinload(SupportUserModel.current_question),
    )

    return (await session.execute(q)).scalars().first()


@pytest.mark.asyncio
async def test_binding_questions(create_models):
    async with async_session() as session:
        support_user = await query_support_user(session)

        random_question = await query_question(session)

        support_user.bind_question(random_question)

        await session.commit()

        result = await query_support_user(session, support_user.id)

        assert random_question == result.current_question


@pytest.mark.asyncio
async def test_adding_answers(create_models):
    async with async_session() as session:

        support_user = await query_support_user(session)

        question = await query_question(session)

        support_user.bind_question(question)

        await session.commit()

        q = (
            select(QuestionModel)
            .where(QuestionModel.id == support_user.current_question.id)
            .options(
                selectinload(QuestionModel.answers),
            )
        )

        current_question = (await session.execute(q)).scalars().first()

        new_answer = AnswerModel(
            tg_message_id=3255512319,
            message="A new question goes here...",
            date=datetime(2022, 4, 19),
        )

        current_question.add_answer(new_answer)
        support_user.add_answer(new_answer)

        await session.commit()

        q = (
            select(SupportUserModel)
            .where(SupportUserModel.id == support_user.id)
            .options(
                selectinload(
                    SupportUserModel.answers,
                ),
                selectinload(
                    SupportUserModel.current_question,
                ),
            )
        )

        new_result = (await session.execute(q)).scalars().first()

        assert new_answer in new_result.current_question.answers
        assert new_answer in new_result.answers


@pytest.mark.asyncio
async def test_deleting_regular_users(create_models):
    async with async_session() as session:
        q = delete(RegularUserModel)

        regular_users = await session.execute(q)

        q = select(RegularUserModel)

        regular_users = (await session.execute(q)).scalars().all()

        assert len(list(regular_users)) == 0

        q = select(QuestionModel)

        questions = (await session.execute(q)).scalars().all()

        assert len(questions) == 0

        q = select(AnswerModel)

        answers = (await session.execute(q)).scalars().all()

        assert len(answers) == 0

        q = select(SupportUserModel)

        support_users = (await session.execute(q)).scalars().all()

        assert len(support_users) != 0

        q = select(RoleModel)

        roles = (await session.execute(q)).scalars().all()

        assert len(roles) != 0


@pytest.mark.asyncio
async def test_deleting_support_users(create_models):
    async with async_session() as session:
        q = delete(SupportUserModel)

        regular_users = await session.execute(q)

        q = select(RegularUserModel)

        regular_users = (await session.execute(q)).scalars().all()

        assert len(list(regular_users)) != 0

        q = select(QuestionModel)

        questions = (await session.execute(q)).scalars().all()

        assert len(questions) != 0

        q = select(AnswerModel)

        answers = (await session.execute(q)).scalars().all()

        assert len(answers) == 0

        q = select(SupportUserModel)

        support_users = (await session.execute(q)).scalars().all()

        assert len(support_users) == 0

        q = select(RoleModel)

        roles = (await session.execute(q)).scalars().all()

        assert len(roles) != 0


@pytest.mark.asyncio
async def test_count_answer(create_models):
    async with async_session() as session:
        q = select(func.count(AnswerModel.id))

        result = (await session.execute(q)).scalar()

        assert result == 3

        support_user = await query_support_user(session)

        new_answer = QuestionModel(
            tg_message_id=12345613,
            message="Really?",
            date=datetime(2021, 10, 25),
        )

        session.add(new_answer)

        await session.commit()

        question = await query_question(session, new_answer.id)

        support_user.bind_question(question)

        await session.commit()

        new_answer = AnswerModel(
            tg_message_id=5555512319,
            message="A new question goes here...",
            date=datetime(2021, 10, 26),
        )

        question.add_answer(new_answer)
        support_user.add_answer(new_answer)

        await session.commit()

        q = select(func.count(AnswerModel.id))

        result = (await session.execute(q)).scalar()

        assert result == 4
