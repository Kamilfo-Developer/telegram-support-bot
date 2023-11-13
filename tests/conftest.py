from datetime import datetime
from uuid import uuid4

import pytest
import pytest_asyncio

from app.answers.entities import Answer, AnswerAttachment
from app.answers.infra.sa_models import AnswerModel
from app.answers.repo import AnswersRepo
from app.config.db_sa_config import ModelBase
from app.containers import AppContainer
from app.errors import IncorrectDBConfigTypeProvided


from app.questions.entities import Question, QuestionAttachment
from app.questions.infra.sa_models import (
    QuestionModel,
)
from app.questions.repo import QuestionsRepo
from app.regular_users.entities import RegularUser
from app.regular_users.infra.sa_models import RegularUserModel
from app.regular_users.repo import RegularUsersRepo
from app.roles.entities import Role
from app.roles.infra.sa_models import RoleModel
from app.roles.repo import RolesRepo
from app.roles.value_objects import RoleDescription, RoleName
from app.shared.db import SADBConfig
from app.shared.value_objects import (
    AnswerIdType,
    QuestionIdType,
    RegularUserIdType,
    RoleIdType,
    RolePermissions,
    SupportUserIdType,
    TgCaption,
    TgFileIdType,
    TgMessageIdType,
    TgMessageText,
    TgUserId,
)
from app.support_users.repo import SupportUsersRepo
from app.utils import TgFileType

from app.support_users.entities import SupportUser, SupportUserRole
from app.support_users.infra.sa_models import SupportUserModel
from app.support_users.value_objects import DescriptiveName


@pytest.fixture
def container() -> AppContainer:
    return AppContainer()


@pytest.fixture
def support_users_repo(container: AppContainer) -> SupportUsersRepo:
    return container.support_users_container.support_users_repo()


@pytest.fixture
def questions_repo(container: AppContainer) -> QuestionsRepo:
    return container.quesions_container.questions_repo()


@pytest.fixture
def answers_repo(container: AppContainer) -> AnswersRepo:
    return container.answers_container.answers_repo()


@pytest.fixture
def regular_users_repo(container: AppContainer) -> RegularUsersRepo:
    return container.regular_users_container.regular_users_repo()


@pytest.fixture
def roles_repo(container: AppContainer) -> RolesRepo:
    return container.roles_container.roles_repo()


@pytest_asyncio.fixture()
async def init_db(
    container: AppContainer,
) -> None:
    db_config = container.db_config()

    if isinstance(db_config, SADBConfig):
        async with db_config.engine.begin() as conn:  # type: ignore
            await conn.run_sync(ModelBase.metadata.drop_all)
            await conn.run_sync(ModelBase.metadata.create_all)

        return

    raise IncorrectDBConfigTypeProvided()


async def fill_sa_db(async_session_maker) -> None:
    async with async_session_maker() as session:
        role1 = Role(
            role_id=RoleIdType(2),
            name=RoleName("TechnicalSupportEmployee"),
            description=RoleDescription(
                "Provides basic technical support to our users"
            ),
            permissions=RolePermissions(True, False),
            created_date=datetime(2023, 1, 5, 12, 0, 5),
        )

        role2 = Role(
            role_id=RoleIdType(3),
            name=RoleName("AnotherTechnicalSupportEmployee"),
            description=RoleDescription(
                "Provides something other than "
                "basic technical support to our users"
            ),
            permissions=RolePermissions(True, True),
            created_date=datetime(2023, 1, 5, 12, 0, 6),
        )

        session.add_all(
            [RoleModel.from_entity(role1), RoleModel.from_entity(role2)]
        )

        regular_user1 = RegularUser(
            id=RegularUserIdType(uuid4()),
            tg_bot_user_id=TgUserId(11111111),
            join_date=datetime(2023, 1, 10, 12, 0, 5),
        )

        regular_user2 = RegularUser(
            id=RegularUserIdType(uuid4()),
            tg_bot_user_id=TgUserId(11111112),
            join_date=datetime(2023, 1, 11, 12, 0, 5),
        )

        regular_user3 = RegularUser(
            id=RegularUserIdType(uuid4()),
            tg_bot_user_id=TgUserId(11111113),
            join_date=datetime(2023, 2, 15, 12, 0, 5),
        )

        session.add_all(
            [
                RegularUserModel.from_entity(regular_user1),
                RegularUserModel.from_entity(regular_user2),
                RegularUserModel.from_entity(regular_user3),
            ]
        )

        support_user1 = SupportUser(
            id=SupportUserIdType(uuid4()),
            descriptive_name=DescriptiveName("Jake"),
            tg_bot_user_id=TgUserId(11111114),
            role=None,
            current_question_id=None,
            join_date=datetime(2023, 1, 1, 12, 0, 5),
            is_owner=True,
            is_active=True,
        )

        support_user2 = SupportUser(
            id=SupportUserIdType(uuid4()),
            descriptive_name=DescriptiveName("Finn"),
            tg_bot_user_id=TgUserId(11111115),
            role=SupportUserRole(RoleIdType(role1._id), role1.permissions),  # type: ignore # noqa: E501
            current_question_id=None,
            join_date=datetime(2023, 1, 1, 12, 0, 5),
            is_owner=False,
            is_active=True,
        )

        session.add_all(
            [
                SupportUserModel.from_entity(support_user1),
                SupportUserModel.from_entity(support_user2),
            ]
        )

        question1 = Question(
            id=QuestionIdType(uuid4()),
            regular_user_id=regular_user1._id,
            tg_message_id=TgMessageIdType(12345667),
            message=TgMessageText("Hello there!"),
            attachments=[
                QuestionAttachment(
                    tg_file_id=TgFileIdType("here_should_be_tg_file_id"),
                    attachment_type=TgFileType.AUDIO,
                    caption=TgCaption("A caption"),
                    date=datetime(2023, 3, 22, 12, 5, 12),
                )
            ],
            date=datetime(2021, 10, 21),
        )

        question2 = Question(
            id=QuestionIdType(uuid4()),
            regular_user_id=regular_user1._id,
            tg_message_id=TgMessageIdType(52135235),
            message=TgMessageText("How can I use this?"),
            attachments=[
                QuestionAttachment(
                    tg_file_id=TgFileIdType(
                        "here_should_be_another_tg_file_id"
                    ),
                    attachment_type=TgFileType.VIDEO,
                    caption=TgCaption("A caption"),
                    date=datetime(2023, 3, 22, 12, 5, 12),
                )
            ],
            date=datetime(2022, 1, 11),
        )

        question3 = Question(
            id=QuestionIdType(uuid4()),
            regular_user_id=regular_user1._id,
            tg_message_id=TgMessageIdType(235123555),
            message=TgMessageText("Is this possible?"),
            attachments=[],
            date=datetime(2022, 6, 4),
        )

        question4 = Question(
            id=QuestionIdType(uuid4()),
            regular_user_id=regular_user1._id,
            tg_message_id=TgMessageIdType(3255512312),
            message=TgMessageText(
                "Well, I am here to ask something, "
                + "but I still have no idea what exactly I want to ask..."
            ),
            attachments=[],
            date=datetime(2021, 10, 21),
        )

        session.add_all(
            [
                QuestionModel.from_entity(question1),
                QuestionModel.from_entity(question2),
                QuestionModel.from_entity(question3),
                QuestionModel.from_entity(question4),
            ]
        )

        answer1 = Answer(
            id=AnswerIdType(uuid4()),
            support_user_id=support_user1._id,
            question_id=question1._id,
            message=TgMessageText("Hi! I am ready to answer your questions!"),
            tg_message_id=TgMessageIdType(59345667),
            is_useful=None,
            attachments=[
                AnswerAttachment(
                    tg_file_id=TgFileIdType("here_should_be_tg_file_id"),
                    attachment_type=TgFileType.AUDIO,
                    caption=TgCaption("A caption"),
                    date=datetime(2023, 3, 22, 12, 5, 12),
                ),
                AnswerAttachment(
                    tg_file_id=TgFileIdType(
                        "here_should_be_another_tg_file_id"
                    ),
                    attachment_type=TgFileType.AUDIO,
                    caption=TgCaption("A caption"),
                    date=datetime(2023, 3, 22, 12, 5, 12),
                ),
            ],
            date=datetime(2023, 3, 22, 12, 5, 12),
        )

        answer2 = Answer(
            id=AnswerIdType(uuid4()),
            support_user_id=support_user2._id,
            question_id=question2._id,
            message=TgMessageText("Easily!"),
            tg_message_id=TgMessageIdType(59345668),
            is_useful=False,
            attachments=[],
            date=datetime(2023, 3, 25, 12, 5, 12),
        )

        answer3 = Answer(
            id=AnswerIdType(uuid4()),
            support_user_id=support_user2._id,
            question_id=question3._id,
            tg_message_id=TgMessageIdType(59345665),
            message=TgMessageText("Yes, it is!"),
            attachments=[],
            date=datetime(2023, 3, 27, 12, 5, 12),
            is_useful=True,
        )

        session.add_all(
            [
                AnswerModel.from_entity(answer1),
                AnswerModel.from_entity(answer2),
                AnswerModel.from_entity(answer3),
            ]
        )

        await session.commit()


@pytest_asyncio.fixture()
async def fill_db(init_db, container: AppContainer) -> None:
    db_config = container.db_config()

    if isinstance(db_config, SADBConfig):
        async_session_maker = db_config.connection_provider
        await fill_sa_db(async_session_maker)

        return

    raise IncorrectDBConfigTypeProvided()
