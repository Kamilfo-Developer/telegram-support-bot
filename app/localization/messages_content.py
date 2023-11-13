import abc
from datetime import timezone

from pytz.tzinfo import BaseTzInfo, DstTzInfo, StaticTzInfo

from app.bot.dtos import TgUser


from app.regular_users.dtos import RegularUserDTO


from app.shared.dtos import (
    AnswerDTO,
    AttachmentDTO,
    QuestionDTO,
    RoleDTO,
    SupportUserDTO,
)
from app.shared.value_objects import TgMessageIdType
from app.statistics.dtos import GlobalStatistics

from app.support_users.dtos import (
    AnswerInfo,
    QuestionInfo,
    RegularUserInfo,
    RoleInfo,
    SupportUserInfo,
)


class MessagesContent(abc.ABC):
    # ARGUMENTS NAMES MESSAGE TEMPLATES
    owner_password_argument_name: str
    regular_user_id_argument_name: str
    regular_user_tg_bot_id_argument_name: str
    support_user_id_argument_name: str
    role_id_argument_name: str
    support_user_descriptive_name: str
    role_name_argument_name: str
    question_id_argument_name: str
    answer_id_argument_name: str
    can_manage_support_users_role_argument_name: str
    can_answer_questions_argument_name: str
    bind_question_button_text: str
    unbind_question_button_text: str
    estimate_answer_as_useful_button_text: str
    estimate_answer_as_unuseful_button_text: str
    show_attachments_button_text: str

    @abc.abstractmethod
    def __init__(
        self, tz: timezone | DstTzInfo | BaseTzInfo | StaticTzInfo
    ) -> None:
        ...

    # START MESSAGES

    @abc.abstractmethod
    async def get_start_regular_user_message(
        self,
        tg_user: TgUser,
        bot_name: str,
        user_info: RegularUserInfo | None = None,
    ) -> list[str]:
        ...

    @abc.abstractmethod
    async def get_start_support_user_message(
        self,
        tg_user: TgUser,
        bot_name: str,
        user_info: SupportUserInfo | None = None,
    ) -> list[str]:
        ...

    @abc.abstractmethod
    async def get_start_owner_message(
        self,
        tg_user: TgUser,
        bot_name: str,
        user_info: SupportUserInfo,
    ) -> list[str]:
        ...

    # HELP MESSAGES

    @abc.abstractmethod
    async def get_owner_help_message(
        self,
        tg_user: TgUser,
        user_info: SupportUserInfo,
    ) -> list[str]:
        ...

    @abc.abstractmethod
    async def get_regular_user_help_message(
        self,
        tg_user: TgUser,
        user_info: RegularUserInfo | None = None,
    ) -> list[str]:
        ...

    @abc.abstractmethod
    async def get_support_user_help_message(
        self, tg_user: TgUser, user_info: SupportUserInfo
    ) -> list[str]:
        ...

    # ARGUMENTS MESSAGES

    @abc.abstractmethod
    async def get_incorrect_num_of_arguments_message(
        self, arguments_list: list[str]
    ) -> list[str]:
        ...

    @abc.abstractmethod
    async def get_incorrect_arguments_passed_message(
        self,
        arguments_list_needed: list[str],
        arguments_list_passed: list[str],
    ) -> list[str]:
        ...

    @abc.abstractmethod
    async def get_no_object_with_this_id_message(self, id: str) -> list[str]:
        ...

    @abc.abstractmethod
    async def get_unavailable_or_deleted_object_message(self) -> list[str]:
        ...

    # ADDITION MESSAGES

    @abc.abstractmethod
    async def get_successful_role_addition_message(
        self,
        role: RoleDTO,
    ) -> list[str]:
        ...

    @abc.abstractmethod
    async def get_role_name_duplicate_message(
        self,
    ) -> list[str]:
        ...

    @abc.abstractmethod
    async def get_successful_support_user_addition_message(
        self,
        support_user: SupportUserDTO,
    ) -> list[str]:
        ...

    @abc.abstractmethod
    async def get_successful_answering_message(
        self,
        question: QuestionDTO,
        answer: AnswerDTO,
    ) -> list[str]:
        ...

    @abc.abstractmethod
    async def get_successful_asking_message(
        self,
        question: QuestionDTO,
    ) -> list[str]:
        ...

    @abc.abstractmethod
    async def get_support_user_already_exists_message(
        self, support_user: SupportUserDTO
    ) -> list[str]:
        ...

    # DELETING OBJECTS MESSAGES
    @abc.abstractmethod
    async def role_deleted_message(
        self,
        role: RoleDTO,
    ) -> list[str]:
        ...

    # ONE OBJECT INFO MESSAGES

    @abc.abstractmethod
    async def get_role_info_message(
        self,
        role_info: RoleInfo,
    ) -> list[str]:
        ...

    @abc.abstractmethod
    async def get_support_user_info_message(
        self, support_user_info: SupportUserInfo
    ) -> list[str]:
        ...

    @abc.abstractmethod
    async def get_regular_user_info_message(
        self, regular_user_info: RegularUserInfo
    ) -> list[str]:
        ...

    @abc.abstractmethod
    async def get_question_info_message(
        self, question_info: QuestionInfo
    ) -> list[str]:
        ...

    @abc.abstractmethod
    async def get_answer_info_message(
        self, answer_info: AnswerInfo
    ) -> list[str]:
        ...

    # OBJECTS LIST INFO MESSAGES

    @abc.abstractmethod
    async def get_roles_list_message(
        self,
        roles_list: list[RoleDTO],
    ) -> list[str]:
        ...

    @abc.abstractmethod
    async def get_questions_list_message(
        self,
        questions_list: list[QuestionDTO],
    ) -> list[str]:
        ...

    @abc.abstractmethod
    async def get_answers_list_message(
        self,
        answers_list: list[AnswerDTO],
    ) -> list[str]:
        ...

    @abc.abstractmethod
    async def get_support_users_list_message(
        self,
        support_users_list: list[SupportUserDTO],
    ) -> list[str]:
        ...

    # BINDING MESSAGES

    @abc.abstractmethod
    async def get_question_already_bound_message(
        self, question_tg_id: TgMessageIdType, support_user_id: int
    ) -> list[str]:
        ...

    @abc.abstractmethod
    async def get_successful_unbinding_message(self) -> list[str]:
        ...

    @abc.abstractmethod
    async def get_successful_binding_message(
        self, question: QuestionDTO
    ) -> list[str]:
        ...

    @abc.abstractmethod
    async def get_no_bound_question_message(self) -> list[str]:
        ...

    @abc.abstractmethod
    async def get_no_quetstions_to_answer_left_message(self) -> list[str]:
        ...

    # ESTIMATION MESSAGES

    @abc.abstractmethod
    async def get_answer_already_estimated_message(
        self, answer: AnswerDTO
    ) -> list[str]:
        ...

    @abc.abstractmethod
    async def get_answer_estimated_as_useful_message(
        self, answer: AnswerDTO
    ) -> list[str]:
        ...

    @abc.abstractmethod
    async def get_answer_estimated_as_unuseful_message(
        self, answer: AnswerDTO
    ) -> list[str]:
        ...

    # INITIALIZING MESSAGES

    @abc.abstractmethod
    async def get_already_inited_owner_message(
        self, tg_user: TgUser
    ) -> list[str]:
        ...

    @abc.abstractmethod
    async def get_successful_owner_init_message(
        self, tg_user: TgUser, support_user: SupportUserDTO
    ) -> list[str]:
        ...

    @abc.abstractmethod
    async def get_incorrect_owner_password_message(self) -> list[str]:
        ...

    # SUPPORT TgUser ACTIVATION MESSAGES

    @abc.abstractmethod
    async def get_support_user_deactivation_message(
        self,
        support_user: SupportUserDTO,
    ) -> list[str]:
        ...

    @abc.abstractmethod
    async def get_support_user_activation_message(
        self,
        support_user: SupportUserDTO,
    ) -> list[str]:
        ...

    # ATTACHMENTS MESSAGES

    @abc.abstractmethod
    async def get_no_last_asked_question_message(
        self, regular_user: RegularUserDTO
    ) -> list[str]:
        ...

    @abc.abstractmethod
    async def get_no_last_answer_message(
        self, support_user: SupportUserDTO
    ) -> list[str]:
        ...

    @abc.abstractmethod
    async def get_question_attachment_addition_message(
        self, question_attachment: AttachmentDTO
    ) -> list[str]:
        ...

    @abc.abstractmethod
    async def get_answer_attachment_addition_message(
        self, answer_attachment: AttachmentDTO
    ) -> list[str]:
        ...

    @abc.abstractmethod
    async def get_no_question_attachments_message(
        self, question: QuestionDTO
    ) -> list[str]:
        ...

    # OTHER MESSAGES

    @abc.abstractmethod
    async def get_global_statistics_message(
        self, global_statistics: GlobalStatistics
    ) -> list[str]:
        ...

    @abc.abstractmethod
    async def get_id_message(self, id: int) -> list[str]:
        ...

    @abc.abstractmethod
    async def get_permission_denied_message(
        self, tg_user: TgUser
    ) -> list[str]:
        ...

    @abc.abstractmethod
    async def get_answer_for_regular_user_message(
        self,
        question_dto: QuestionDTO,
        answer_dto: AnswerDTO,
        include_question: bool = False,
    ) -> list[str]:
        ...

    @abc.abstractmethod
    async def get_unsupported_message_type_message(self) -> list[str]:
        ...

    @abc.abstractmethod
    async def get_unknown_command_message(self) -> list[str]:
        ...

    @abc.abstractmethod
    async def get_regular_user_not_authorized_message(self) -> list[str]:
        ...
