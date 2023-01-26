from telegram import User
from bot.entities.regular_user import RegularUser
from bot.entities.support_user import SupportUser
from bot.entities.role import Role
from bot.entities.question import Question
from bot.entities.answer import Answer

import abc


class Messages(abc.ABC):
    # ARGUMENTS NAMES MESSAGE TEMPLATES
    regular_user_id_argument_name: str
    regular_tg_bot_user_id_argument_name: str
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

    # START MESSAGES

    @abc.abstractmethod
    async def get_start_regular_user_message(
        self,
        telegram_user: User,
        user_entity: RegularUser | None = None,
        *args,
        **kwargs,
    ) -> list[str]:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_start_support_user_message(
        self,
        telegram_user: User,
        user_entity: SupportUser | None = None,
        *args,
        **kwargs,
    ) -> list[str]:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_start_owner_message(
        self,
        telegram_user: User,
        user_entity: SupportUser,
        *args,
        **kwargs,
    ) -> list[str]:
        raise NotImplementedError

    # HELP MESSAGES

    @abc.abstractmethod
    async def get_inited_owner_help_message(
        self,
        user: User,
        user_entity: SupportUser,
        *args,
        **kwargs,
    ) -> list[str]:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_not_inited_owner_help_message(
        self,
        user: User,
        *args,
        **kwargs,
    ) -> list[str]:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_regular_user_help_message(
        self, user: User, *args, **kwargs
    ) -> list[str]:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_support_user_help_message(
        self, user: User, user_entity: SupportUser, *args, **kwargs
    ) -> list[str]:
        raise NotImplementedError

    # ARGUMENTS MESSAGES

    @abc.abstractmethod
    async def get_incorrect_num_of_arguments_message(
        self, arguments_list: list[str], *args, **kwargs
    ) -> list[str]:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_incorrect_arguments_passed_message(
        self, *args, **kwargs
    ) -> list[str]:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_no_object_with_this_id_message(
        self, id: str, *args, **kwargs
    ) -> list[str]:
        raise NotImplementedError

    # ADDITION MESSAGES

    @abc.abstractmethod
    async def get_successful_role_addition_message(
        self,
        role: Role,
        *args,
        **kwargs,
    ) -> list[str]:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_role_name_duplicate_message(
        self,
        *args,
        **kwargs,
    ) -> list[str]:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_successful_support_user_addition_message(
        self,
        support_user: SupportUser,
        *args,
        **kwargs,
    ) -> list[str]:

        raise NotImplementedError

    @abc.abstractmethod
    async def get_successful_answering_message(
        self,
        question: Question,
        answer: Answer,
        *args,
        **kwargs,
    ) -> list[str]:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_successful_asking_message(
        self,
        question: Question,
        *args,
        **kwargs,
    ) -> list[str]:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_support_user_already_exists_message(
        self, support_user: SupportUser, *args, **kwargs
    ) -> list[str]:
        raise NotImplementedError

    # DELETING OBJECTS MESSAGES
    @abc.abstractmethod
    async def role_deleted_message(
        self,
        role: Role,
        *args,
        **kwargs,
    ) -> list[str]:
        raise NotImplementedError

    # ONE OBJECT INFO MESSAGES

    @abc.abstractmethod
    async def get_role_info_message(
        self,
        role: Role,
        *args,
        **kwargs,
    ) -> list[str]:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_support_user_info_message(
        self,
        support_user: SupportUser,
        *args,
        **kwargs,
    ) -> list[str]:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_question_info_message(
        self,
        question: Question,
        *args,
        **kwargs,
    ) -> list[str]:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_answer_info_message(
        self,
        answer: Answer,
        *args,
        **kwargs,
    ) -> list[str]:
        raise NotImplementedError

    # OBJECTS LIST INFO MESSAGES

    @abc.abstractmethod
    async def get_roles_list_message(
        self,
        roles_list: list[Role],
        *args,
        **kwargs,
    ) -> list[str]:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_questions_list_message(
        self,
        questions_list: list[Question],
        *args,
        **kwargs,
    ) -> list[str]:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_answers_list_message(
        self,
        answers_list: list[Answer],
        *args,
        **kwargs,
    ) -> list[str]:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_support_users_list_message(
        self,
        support_users_list: list[SupportUser],
        *args,
        **kwargs,
    ) -> list[str]:
        raise NotImplementedError

    # BINDING MESSAGES

    @abc.abstractmethod
    async def get_question_already_binded_message(
        self, question_id: int, *args, **kwargs
    ) -> list[str]:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_successful_unbinding_message(
        self, *args, **kwargs
    ) -> list[str]:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_successful_binding_message(
        self, question: Question, *args, **kwargs
    ) -> list[str]:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_no_binded_question_message(
        self, *args, **kwargs
    ) -> list[str]:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_no_unbinded_quetstions_left_message(
        self, *args, **kwargs
    ) -> list[str]:
        raise NotImplementedError

    # ESTIMATION MESSAGES

    @abc.abstractmethod
    async def get_answer_already_estimated_message(
        self, answer: Answer, *args, **kwargs
    ) -> list[str]:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_answer_estimated_as_useful_message(
        self, answer: Answer, *args, **kwargs
    ) -> list[str]:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_answer_estimated_as_unuseful_message(
        self, answer: Answer, *args, **kwargs
    ) -> list[str]:
        raise NotImplementedError

    # INITIALIZING MESSAGES

    @abc.abstractmethod
    async def get_not_inited_owner_message(
        self,
        telegram_user: User,
        *args,
        **kwargs,
    ) -> list[str]:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_already_inited_owner_message(
        self, user: User, *args, **kwargs
    ) -> list[str]:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_successful_owner_init_message(
        self, user: User, support_user: SupportUser, *args, **kwargs
    ) -> list[str]:
        raise NotImplementedError

    # SUPPORT USER ACTIVATION MESSAGES

    @abc.abstractmethod
    async def get_support_user_deactivation_message(
        self,
        support_user: SupportUser,
        *args,
        **kwargs,
    ) -> list[str]:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_support_user_activation_message(
        self,
        support_user: SupportUser,
        *args,
        **kwargs,
    ) -> list[str]:
        raise NotImplementedError

    # OTHER MESSAGES

    @abc.abstractmethod
    async def get_id_message(self, id: int, *args, **kwargs) -> list[str]:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_permission_denied_message(
        self, user: User, *args, **kwargs
    ) -> list[str]:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_answer_for_regular_user_message(
        self,
        answer: Answer,
        include_question: bool = False,
        *args,
        **kwargs,
    ) -> list[str]:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_unsupported_message_type_message(
        self, *args, **kwargs
    ) -> list[str]:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_unknown_command_message(self, *args, **kwargs) -> list[str]:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_regular_user_not_authorized_message(
        self, *args, **kwargs
    ) -> list[str]:
        raise NotImplementedError
