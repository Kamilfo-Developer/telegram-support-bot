from __future__ import annotations
from app.answers.entities import Answer
from app.answers.repo import AnswersRepo

from app.errors import (
    IncorrectActionError,
    IncorrectPasswordError,
    NoBoundQuestion,
    NoSuchAnswer,
    NoSuchEntityError,
    NoSuchQuestion,
    NoSuchRegularUser,
    NoSuchRole,
    NoSuchSupportUser,
    OwnerAlreadyInitialized,
    PermissionDeniedError,
    RoleNameDuplicationError,
    SameValueAssigningError,
    SupportUserAlreadyExists,
    UserIsNotAuthorizedError,
)
from app.shared.dtos import QuestionDTO, SupportUserDTO


from app.questions.repo import QuestionsRepo
from app.regular_users.repo import RegularUsersRepo
from app.roles.entities import Role
from app.roles.repo import RolesRepo
from app.roles.value_objects import RoleDescription, RoleName
from app.shared.value_objects import (
    RoleIdType,
    RolePermissions,
    TgCaption,
    TgFileIdType,
    TgMessageIdType,
    TgMessageText,
    TgUserId,
)

from app.statistics.service import StatisticsService
from app.statistics.dtos import GlobalStatistics
from app.support_users.dtos import (
    AnswerAttachmentSentEvent,
    AnswerDTO,
    AnswerInfo,
    AttachmentDTO,
    QuestionInfo,
    QuestionWasAnsweredEvent,
    RegularUserDTO,
    RegularUserInfo,
    RoleDTO,
    RoleInfo,
    SupportUserInfo,
)
from app.support_users.entities import SupportUser, SupportUserRole
from app.support_users.queries import (
    SupportUsersQueriesFactory,
)

from app.support_users.repo import SupportUsersRepo
from app.support_users.value_objects import DescriptiveName
from app.utils import (
    TgFileType,
)


class SupportUserController:
    def __init__(
        self,
        support_users_repo: SupportUsersRepo,
        regular_users_repo: RegularUsersRepo,
        questions_repo: QuestionsRepo,
        answers_repo: AnswersRepo,
        roles_repo: RolesRepo,
        statistics_service: StatisticsService,
        support_users_queries_factory: SupportUsersQueriesFactory,
    ) -> None:
        self.__support_users_repo = support_users_repo
        self.__regular_users_repo = regular_users_repo
        self.__questions_repo = questions_repo
        self.__answers_repo = answers_repo
        self.__roles_repo = roles_repo
        self.__statistics_service = statistics_service
        self.__support_users_queries_factory = support_users_queries_factory

    async def get_global_statistics(
        self, authorized_support_user: SupportUserDTO
    ) -> GlobalStatistics:
        support_user = self.__support_user_entity_from_dto(
            authorized_support_user
        )

        if not support_user.can_manage_support_users():
            raise PermissionDeniedError()

        global_statistics = (
            await self.__statistics_service.get_global_statistics()
        )

        return global_statistics

    async def get_own_support_user_info(
        self,
        authorized_support_user: SupportUserDTO,
    ) -> SupportUserInfo:
        support_user = self.__support_user_entity_from_dto(
            authorized_support_user
        )

        support_user_statistics = (
            await (
                self.__statistics_service.get_support_user_statistics(
                    support_user._id
                )
            )
        )

        return SupportUserInfo(
            support_user_dto=SupportUserDTO.from_entity(support_user),
            statistics=support_user_statistics,
        )

    async def get_regular_user_info_by_id(
        self,
        authorized_support_user: SupportUserDTO,
        regular_user_tg_id: TgUserId,
    ) -> RegularUserInfo:
        support_user = self.__support_user_entity_from_dto(
            authorized_support_user
        )

        if not support_user.can_manage_support_users():
            raise PermissionDeniedError()

        query = (
            self.__support_users_queries_factory.create_get_regular_user_info_by_tg_user_id_query()  # noqa: E501
        )

        regular_user_info = await query.execute(regular_user_tg_id)

        if not regular_user_info:
            raise NoSuchRegularUser()

        return regular_user_info

    async def bind_question(
        self,
        authorized_support_user: SupportUserDTO,
        question_tg_message_id: TgMessageIdType,
    ) -> QuestionDTO:
        support_user = self.__support_user_entity_from_dto(
            authorized_support_user
        )

        if not support_user.can_answer_questions():
            raise PermissionDeniedError()

        question = await self.__questions_repo.get_by_tg_message_id(
            TgMessageIdType(question_tg_message_id)
        )

        if not question:
            raise NoSuchQuestion()

        support_user.bind_question(question_id=question._id)

        await self.__support_users_repo.update(support_user)

        return QuestionDTO.from_entity(question)

    async def unbind_question(
        self, authorized_support_user: SupportUserDTO
    ) -> None:
        support_user = self.__support_user_entity_from_dto(
            authorized_support_user
        )

        if not support_user.can_answer_questions():
            raise PermissionDeniedError()

        try:
            support_user.unbind_question()
        except SameValueAssigningError:
            raise NoBoundQuestion()

        await self.__support_users_repo.update(support_user)

    async def add_role(
        self,
        authorized_support_user: SupportUserDTO,
        role_name: RoleName,
        role_description: RoleDescription,
        can_answer_questions: bool,
        can_manage_support_users: bool,
    ) -> RoleDTO:
        support_user = self.__support_user_entity_from_dto(
            authorized_support_user
        )

        if not support_user.can_manage_support_users():
            raise PermissionDeniedError()

        if await self.__roles_repo.get_by_name(RoleName(role_name)):
            raise RoleNameDuplicationError()

        role = await self.__roles_repo.add(
            Role.create(
                name=RoleName(role_name),
                description=RoleDescription(role_description),
                permissions=RolePermissions(
                    can_answer_questions=can_answer_questions,
                    can_manage_support_users=can_manage_support_users,
                ),
            )
        )

        return RoleDTO.from_entity(role)

    async def get_role_info(
        self,
        authorized_support_user: SupportUserDTO,
        role_id: RoleIdType,
    ) -> RoleInfo:
        support_user = self.__support_user_entity_from_dto(
            authorized_support_user
        )

        if not support_user.can_manage_support_users():
            raise PermissionDeniedError()

        query = (
            self.__support_users_queries_factory.create_get_role_info_by_id_query()  # noqa: E501
        )

        role_info = await query.execute(role_id)

        if not role_info:
            raise NoSuchRole()

        return role_info

    async def get_all_roles(
        self, authorized_support_user: SupportUserDTO
    ) -> list[RoleDTO]:
        support_user = self.__support_user_entity_from_dto(
            authorized_support_user
        )

        if not support_user.can_manage_support_users():
            raise PermissionDeniedError()

        roles = await self.__roles_repo.get_all()

        return [RoleDTO.from_entity(role) for role in roles]

    async def delete_role(
        self, authorized_support_user: SupportUserDTO, role_id: int
    ) -> RoleDTO:
        support_user = self.__support_user_entity_from_dto(
            authorized_support_user
        )
        if not support_user.can_manage_support_users():
            raise PermissionDeniedError()

        role = await self.__roles_repo.get_by_id(RoleIdType(role_id))

        if not role:
            raise NoSuchRole()

        await self.__roles_repo.delete(role._id)  # type: ignore

        return RoleDTO.from_entity(role)

    async def add_support_user(
        self,
        authorized_support_user: SupportUserDTO,
        regular_user_tg_id: TgUserId,
        role_id: RoleIdType,
        descriptive_name: str,
    ) -> SupportUserDTO:
        support_user = self.__support_user_entity_from_dto(
            authorized_support_user
        )
        if not support_user.can_manage_support_users():
            raise PermissionDeniedError()

        role_for_user = await self.__roles_repo.get_by_id(RoleIdType(role_id))

        if not role_for_user:
            raise NoSuchRole()

        regular_user = await self.__regular_users_repo.get_by_tg_bot_user_id(
            regular_user_tg_id
        )

        if not regular_user:
            raise NoSuchRegularUser()

        new_support_user = (
            await self.__support_users_repo.get_by_tg_bot_user_id(
                regular_user.tg_bot_user_id
            )
        )

        if new_support_user:
            raise SupportUserAlreadyExists()

        new_support_user = SupportUser.create(
            descriptive_name=DescriptiveName(descriptive_name),
            tg_bot_user_id=regular_user.tg_bot_user_id,
            role=SupportUserRole(
                role_for_user._id, role_for_user.permissions  # type: ignore
            ),
        )

        await self.__support_users_repo.add(new_support_user)

        return SupportUserDTO.from_entity(new_support_user)

    async def get_support_user_info_by_id(
        self,
        authorized_support_user: SupportUserDTO,
        support_user_tg_id_to_get_info: TgUserId,
    ) -> SupportUserInfo:
        support_user = self.__support_user_entity_from_dto(
            authorized_support_user
        )

        if not support_user.can_manage_support_users():
            raise PermissionDeniedError()

        query = (
            self.__support_users_queries_factory.create_get_support_user_info_by_tg_user_id_query()  # noqa: E501
        )

        support_user_info = await query.execute(support_user_tg_id_to_get_info)

        if not support_user_info:
            raise NoSuchSupportUser()

        return support_user_info

    async def get_all_support_users(
        self, authorized_support_user: SupportUserDTO
    ) -> list[SupportUserDTO]:
        support_user = self.__support_user_entity_from_dto(
            authorized_support_user
        )

        if not support_user.can_manage_support_users():
            raise PermissionDeniedError()

        all_support_users = await self.__support_users_repo.get_all()

        return [
            SupportUserDTO.from_entity(support_user)
            for support_user in all_support_users
        ]

    async def get_question_info_by_id(
        self,
        authorized_support_user: SupportUserDTO,
        question_tg_message_id: TgMessageIdType,
    ) -> QuestionInfo:
        support_user = self.__support_user_entity_from_dto(
            authorized_support_user
        )
        if not support_user.can_answer_questions():
            raise PermissionDeniedError()

        query = (
            self.__support_users_queries_factory.create_get_question_info_by_tg_message_id_query()  # noqa: E501
        )

        question_info = await query.execute(question_tg_message_id)

        if not question_info:
            raise NoSuchQuestion()

        return question_info

    async def get_question_to_answer(
        self,
        authorized_support_user: SupportUserDTO,
    ) -> QuestionInfo | None:
        support_user = self.__support_user_entity_from_dto(
            authorized_support_user
        )

        if not support_user.can_answer_questions():
            raise PermissionDeniedError()

        query = (
            self.__support_users_queries_factory.create_get_question_to_answer_query()  # noqa: E501
        )

        # NOTE: Probably, here we should add some configurable behavior
        # which can be implemented using the Strategy pattern
        question_info = await query.execute()

        if not question_info:
            return None

        return question_info

    async def get_answer_info(
        self,
        authorized_support_user: SupportUserDTO,
        answer_tg_message_id: TgMessageIdType,
    ) -> AnswerInfo:
        support_user = self.__support_user_entity_from_dto(
            authorized_support_user
        )
        if not support_user.can_answer_questions():
            raise PermissionDeniedError()

        query = (
            self.__support_users_queries_factory.create_get_answer_info_by_tg_message_id_query()  # noqa: E501
        )

        answer_info = await query.execute(answer_tg_message_id)

        if not answer_info:
            raise NoSuchEntityError()

        return answer_info

    async def get_question_answers(
        self,
        authorized_support_user: SupportUserDTO,
        question_tg_message_id: TgMessageIdType,
    ) -> list[AnswerDTO]:
        support_user = self.__support_user_entity_from_dto(
            authorized_support_user
        )
        if not support_user.can_answer_questions():
            raise PermissionDeniedError()

        question = await self.__questions_repo.get_by_tg_message_id(
            TgMessageIdType(question_tg_message_id)
        )

        if not question:
            raise NoSuchQuestion()

        answers = await self.__answers_repo.get_by_question_id(
            question_id=question._id
        )

        return [AnswerDTO.from_entity(answer) for answer in answers]

    async def activate_support_user(
        self,
        authorized_support_user: SupportUserDTO,
        support_user_to_activate_tg_id: TgUserId,
    ) -> SupportUserDTO:
        support_user = self.__support_user_entity_from_dto(
            authorized_support_user
        )
        if not support_user.can_manage_support_users():
            raise PermissionDeniedError()

        support_user_to_activate = (
            await self.__support_users_repo.get_by_tg_bot_user_id(
                support_user_to_activate_tg_id
            )
        )

        if not support_user_to_activate:
            raise NoSuchSupportUser()

        support_user_to_activate.activate()

        await self.__support_users_repo.update(support_user_to_activate)

        return SupportUserDTO.from_entity(support_user_to_activate)

    async def deactivate_support_user(
        self,
        authorized_support_user: SupportUserDTO,
        support_user_to_deactivate_tg_id: TgUserId,
    ) -> SupportUserDTO:
        support_user = self.__support_user_entity_from_dto(
            authorized_support_user
        )
        if not support_user.can_manage_support_users():
            raise PermissionDeniedError()

        support_user_to_deactivate = (
            await self.__support_users_repo.get_by_tg_bot_user_id(
                support_user_to_deactivate_tg_id
            )
        )

        if not support_user_to_deactivate:
            raise NoSuchSupportUser()

        try:
            support_user_to_deactivate.deactivate()

        except IncorrectActionError:
            # FIXME: We should raise another error here
            raise PermissionDeniedError()

        await self.__support_users_repo.update(support_user_to_deactivate)

        return SupportUserDTO.from_entity(support_user_to_deactivate)

    async def answer_bound_question(
        self,
        authorized_support_user: SupportUserDTO,
        answer_text: TgMessageText,
        message_id: TgMessageIdType,
    ) -> QuestionWasAnsweredEvent:
        support_user = self.__support_user_entity_from_dto(
            authorized_support_user
        )

        if not support_user.can_manage_support_users():
            raise PermissionDeniedError()

        if not support_user.current_question_id:
            raise NoBoundQuestion()

        question = await self.__questions_repo.get_by_id(
            support_user.current_question_id
        )

        if not question:
            raise NoSuchQuestion()

        answer = await self.__answers_repo.add(
            Answer.create(
                support_user_id=support_user._id,
                message=TgMessageText(answer_text),
                question_id=question._id,
                tg_message_id=TgMessageIdType(message_id),
            )
        )

        regular_user = await self.__regular_users_repo.get_by_id(
            question.regular_user_id
        )

        if not regular_user:
            raise NoSuchRegularUser()

        return QuestionWasAnsweredEvent(
            QuestionDTO.from_entity(question),
            AnswerDTO.from_entity(answer),
            RegularUserDTO.from_entity(regular_user),
        )

    async def add_attachment_to_last_answer(
        self,
        authorized_support_user: SupportUserDTO,
        tg_file_id: TgFileIdType,
        attachment_type: TgFileType,
        caption: TgCaption | None,
    ) -> AnswerAttachmentSentEvent:
        support_user = self.__support_user_entity_from_dto(
            authorized_support_user
        )

        if not support_user.can_answer_questions():
            raise PermissionDeniedError()

        if not support_user.current_question_id:
            raise NoBoundQuestion()

        question = await self.__questions_repo.get_by_id(
            support_user.current_question_id
        )

        if not question:
            raise NoSuchQuestion()

        regular_user_asked = await self.__regular_users_repo.get_by_id(
            question.regular_user_id
        )

        if not regular_user_asked:
            raise NoSuchRegularUser()

        last_answer = await self.__answers_repo.get_question_last_answer(
            question._id
        )

        if not last_answer:
            raise NoSuchAnswer()

        last_answer.add_attachment(
            tg_file_id=TgFileIdType(tg_file_id),
            attachment_type=attachment_type,
            caption=caption,
        )

        return AnswerAttachmentSentEvent(
            attachment_dto=AttachmentDTO.from_entity(
                last_answer.attachments[-1]
            ),
            support_user_answered=SupportUserDTO.from_entity(support_user),
            regular_user_asked=RegularUserDTO.from_entity(
                regular_user_entity=regular_user_asked
            ),
        )

    async def get_attachments_for_question(
        self,
        authorized_support_user: SupportUserDTO,
        question_tg_message_id: TgMessageIdType,
    ) -> list[AttachmentDTO]:
        support_user = self.__support_user_entity_from_dto(
            authorized_support_user
        )

        if not support_user.can_answer_questions():
            raise PermissionDeniedError()

        question = await self.__questions_repo.get_by_tg_message_id(
            question_tg_message_id
        )

        if not question:
            raise NoSuchQuestion()

        return [
            AttachmentDTO.from_entity(attachment)
            for attachment in question.attachments
        ]

    async def initialize_owner(
        self,
        regular_user_tg_id: TgUserId,
        entered_password: str,
        owner_password: str,
        default_owner_descriptive_name: DescriptiveName,
    ) -> SupportUserDTO:
        support_user = await self.__support_users_repo.get_by_tg_bot_user_id(
            regular_user_tg_id
        )

        if support_user:
            raise OwnerAlreadyInitialized()

        if entered_password != owner_password:
            raise IncorrectPasswordError()

        support_user = SupportUser.create_owner(
            descriptive_name=default_owner_descriptive_name,
            tg_bot_user_id=regular_user_tg_id,
        )

        await self.__support_users_repo.add(support_user)

        return SupportUserDTO.from_entity(support_user)

    def __support_user_entity_from_dto(self, support_user_dto: SupportUserDTO):
        return SupportUser(
            id=support_user_dto.id,
            descriptive_name=support_user_dto.descriptive_name,
            tg_bot_user_id=support_user_dto.tg_bot_id,
            role=SupportUserRole(
                support_user_dto.role.id, support_user_dto.role.permissions
            )
            if support_user_dto.role
            else None,
            current_question_id=support_user_dto.bound_question_id,
            join_date=support_user_dto.join_date,
            is_active=support_user_dto.is_active,
            is_owner=support_user_dto.is_owner,
        )

    async def authorize_support_user(self, tg_id: TgUserId) -> SupportUserDTO:
        support_user = await self.__support_users_repo.get_by_tg_bot_user_id(
            tg_id
        )

        if support_user is None or not support_user.is_active:
            raise UserIsNotAuthorizedError()

        return SupportUserDTO.from_entity(support_user)
