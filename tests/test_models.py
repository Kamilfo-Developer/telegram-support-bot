from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from tests.test_db_config import engine, async_session
from bot.db.db_config import Base
from bot.db.models.answer_model import AnswerModel
from bot.db.models.question_model import QuestionModel
from bot.db.models.regular_user_model import RegularUserModel
from bot.db.models.role_model import RoleModel
from bot.db.models.support_user_model import SupportUserModel
from sqlalchemy.future import select
import pytest
import pytest_asyncio


@pytest_asyncio.fixture(autouse=True)
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def add_data(async_session: AsyncSession):
    async with async_session() as session:
        role1 = RoleModel(name="support")

        regular_user1 = RegularUserModel(tg_bot_user_id=1234567809)
        regular_user2 = RegularUserModel(tg_bot_user_id=1234566342)
        regular_user3 = RegularUserModel(tg_bot_user_id=5626172212)

        support_user1 = SupportUserModel(tg_bot_user_id=1234257322)
        support_user2 = SupportUserModel(tg_bot_user_id=5321899523)

        role1.users.append(support_user1)
        role1.users.append(support_user2)

        session.add_all([regular_user1, regular_user2, regular_user3])
        session.add_all([role1, support_user1, support_user2])

        question1 = QuestionModel(
            tg_message_id=12345667,
            message="Hello there!",
            date=datetime(2021, 10, 21),
        )

        question2 = QuestionModel(
            tg_message_id=52135235,
            message="How can I use this?",
            date=datetime(2022, 1, 11),
        )

        question3 = QuestionModel(
            tg_message_id=235123555,
            message="Is this possible?",
            date=datetime(2022, 6, 4),
        )

        question4 = QuestionModel(
            tg_message_id=3255512312,
            message="Well, I am here to ask something, "
            + "but I still have no idea what exactly I want to ask...",
            date=datetime(2021, 10, 21),
        )

        regular_user1.questions.append(question1)
        regular_user1.questions.append(question2)
        regular_user2.questions.append(question3)
        regular_user3.questions.append(question4)

        answer1 = AnswerModel(
            tg_message_id=59345667,
            message="Hi! I am ready to answer your questions!",
            date=datetime(2021, 10, 22),
        )

        answer2 = AnswerModel(
            tg_message_id=59345661,
            message="It is pretty easy, let me show you :)",
            date=datetime(2022, 1, 13),
        )

        answer3 = AnswerModel(
            tg_message_id=59345665,
            message="Yes, it is!",
            date=datetime(2022, 6, 6),
        )

        support_user1.answers.append(answer1)
        question1.answers.append(answer1)

        support_user1.answers.append(answer2)
        question2.answers.append(answer2)

        support_user2.answers.append(answer3)
        question3.answers.append(answer3)

        await session.commit()


@pytest.fixture(scope="session")
async def drop_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


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
            tg_message_id=3255512312,
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


async def query_random_question(session: AsyncSession) -> QuestionModel:
    q = (
        select(QuestionModel)
        .where(QuestionModel.current_support_user == None)
        .where(QuestionModel.answers == None)
        .options(selectinload(QuestionModel.answers))
    )

    return (await session.execute(q)).scalars().first()


@pytest.mark.asyncio
async def test_binding_questions(create_models):
    async with async_session() as session:
        q = select(SupportUserModel).options(
            selectinload(SupportUserModel.answers),
            selectinload(SupportUserModel.current_question),
        )

        support_user: SupportUserModel = (
            (await session.execute(q)).scalars().first()
        )

        random_question = await query_random_question(session)

        support_user.bind_question(random_question)

        await session.commit()

        q = (
            select(SupportUserModel)
            .where(SupportUserModel.id == support_user.id)
            .options(
                selectinload(SupportUserModel.answers),
                selectinload(SupportUserModel.current_question),
            )
        )

        result = (await session.execute(q)).scalars().first()

        assert random_question == result.current_question


# TODO Figure out how to add asnwers to questions properly
@pytest.mark.asyncio
async def test_adding_answers(create_models):
    async with async_session() as session:
        q = select(SupportUserModel).options(
            selectinload(SupportUserModel.answers),
            selectinload(SupportUserModel.current_question),
        )

        support_user = (await session.execute(q)).scalars().first()

        support_user.bind_question(await query_random_question(session))

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
            tg_message_id=3255512312,
            message="A new question goes here...",
            date=datetime(2022, 4, 19),
        )

        current_question.add_answer(new_answer)

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
