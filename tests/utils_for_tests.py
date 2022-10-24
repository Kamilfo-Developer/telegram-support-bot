from uuid import UUID
from sqlalchemy.orm import selectinload
from sqlalchemy.future import select
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from bot.db.models.sa.answer_model import AnswerModel
from bot.db.models.sa.question_model import QuestionModel
from bot.db.models.sa.regular_user_model import RegularUserModel
from bot.db.models.sa.role_model import RoleModel
from bot.db.models.sa.support_user_model import SupportUserModel
from bot.db.db_settings import Base
from tests.db_test_config import engine
import pytest_asyncio


async def add_data(async_session: AsyncSession):
    async with async_session() as session:
        role1 = RoleModel(name="support")

        regular_user1 = RegularUserModel(tg_bot_user_id=1234567809)
        regular_user2 = RegularUserModel(tg_bot_user_id=1234566342)
        regular_user3 = RegularUserModel(tg_bot_user_id=5626172212)

        support_user1 = SupportUserModel(tg_bot_user_id=1234257322)
        support_user2 = SupportUserModel(tg_bot_user_id=5321899523)

        role1.add_user(support_user1)
        role1.add_user(support_user2)

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

        regular_user1.add_question(question1)
        regular_user1.add_question(question2)
        regular_user2.add_question(question3)
        regular_user3.add_question(question4)

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

        support_user1.add_answer(answer1)
        question1.add_answer(answer1)

        support_user1.add_answer(answer2)
        question2.add_answer(answer2)

        support_user2.add_answer(answer3)
        question3.add_answer(answer3)

        await session.commit()


async def query_random_question(session: AsyncSession):
    q = select(QuestionModel).options(
        selectinload(QuestionModel.answers),
        selectinload(QuestionModel.current_support_user),
        selectinload(QuestionModel.regular_user),
    )

    return (await session.execute(q)).scalars().first()


async def query_random_unanswered_question(session: AsyncSession):
    q = (
        select(QuestionModel)
        .where(QuestionModel.answers == None)
        .options(
            selectinload(QuestionModel.answers),
            selectinload(QuestionModel.current_support_user),
            selectinload(QuestionModel.regular_user),
        )
    )

    return (await session.execute(q)).scalars().first()


async def query_random_answered_question(session: AsyncSession):
    q = (
        select(QuestionModel)
        .where(QuestionModel.answers != None)
        .options(
            selectinload(QuestionModel.answers),
            selectinload(QuestionModel.current_support_user),
            selectinload(QuestionModel.regular_user),
        )
    )

    return (await session.execute(q)).scalars().first()


async def query_question_by_id(session: AsyncSession, id: UUID):
    q = (
        select(QuestionModel)
        .where(QuestionModel.id == id)
        .options(
            selectinload(QuestionModel.answers),
            selectinload(QuestionModel.current_support_user),
            selectinload(QuestionModel.regular_user),
        )
    )

    return (await session.execute(q)).scalars().first()


async def query_regular_user_by_id(
    session: AsyncSession, id: UUID
) -> RegularUserModel:
    q = (
        select(RegularUserModel)
        .where(RegularUserModel.id == id)
        .options(selectinload(RegularUserModel.questions))
    )

    return (await session.execute(q)).scalars().first()


async def query_random_regular_user(session: AsyncSession) -> RegularUserModel:
    q = select(RegularUserModel).options(
        selectinload(RegularUserModel.questions)
    )

    return (await session.execute(q)).scalars().first()


async def query_random_regular_user_with_no_questions(
    session: AsyncSession,
) -> RegularUserModel:
    q = (
        select(RegularUserModel)
        .where(RegularUserModel.questions == None)
        .options(selectinload(RegularUserModel.questions))
    )

    return (await session.execute(q)).scalars().first()


async def query_random_regular_user_with_questions(
    session: AsyncSession,
) -> RegularUserModel:
    q = (
        select(RegularUserModel)
        .where(RegularUserModel.questions != None)
        .options(selectinload(RegularUserModel.questions))
    )

    return (await session.execute(q)).scalars().first()


async def query_support_user_by_id(
    session: AsyncSession, id: UUID = None
) -> SupportUserModel:

    q = (
        select(SupportUserModel)
        .where(SupportUserModel.id == id)
        .options(
            selectinload(SupportUserModel.answers),
            selectinload(SupportUserModel.current_question),
        )
    )

    return (await session.execute(q)).scalars().first()


async def query_random_support_user_with_no_answered_questions(
    session: AsyncSession,
):
    q = (
        select(SupportUserModel)
        .where(SupportUserModel.answers == None)
        .options(
            selectinload(SupportUserModel.answers),
            selectinload(SupportUserModel.current_question),
        )
    )

    return (await session.execute(q)).scalars().first()


async def query_random_support_user_with_answered_questions(
    session: AsyncSession,
):
    q = (
        select(SupportUserModel)
        .where(SupportUserModel.answers != None)
        .options(
            selectinload(SupportUserModel.answers),
            selectinload(SupportUserModel.current_question),
        )
    )

    return (await session.execute(q)).scalars().first()


async def query_random_support_user(session: AsyncSession) -> SupportUserModel:
    q = select(SupportUserModel).options(
        selectinload(SupportUserModel.answers),
        selectinload(SupportUserModel.current_question),
    )

    return (await session.execute(q)).scalars().first()


@pytest_asyncio.fixture(autouse=True)
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
