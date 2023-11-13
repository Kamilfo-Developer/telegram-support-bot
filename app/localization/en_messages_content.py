from datetime import timezone

from pytz.tzinfo import BaseTzInfo, DstTzInfo, StaticTzInfo

from app.bot.dtos import TgUser
from app.localization.messages_content import MessagesContent
from app.shared.dtos import (
    AnswerDTO,
    AttachmentDTO,
    QuestionDTO,
    RegularUserDTO,
    RoleDTO,
    SupportUserDTO,
)
from app.statistics.dtos import GlobalStatistics
from app.support_users.dtos import (
    AnswerInfo,
    QuestionInfo,
    RegularUserInfo,
    RoleInfo,
    SupportUserInfo,
)
from app.utils import get_eu_formated_datetime, get_us_formated_datetime


class ENMessagesContent(MessagesContent):
    # ARGUMENTS NAMES MESSAGE TEMPLATES
    owner_password_argument_name = "owner's password"
    regular_user_id_argument_name = "regular user's ID"
    regular_user_tg_bot_id_argument_name = (
        "regular user Telegram ID (a number)"
    )
    support_user_id_argument_name = "support user's ID"
    role_id_argument_name = "role's ID"
    support_user_descriptive_name = "descreptive name"
    role_name_argument_name = "role's name"
    question_id_argument_name = "question's ID"
    answer_id_argument_name = "answer's ID"
    can_manage_support_users_role_argument_name = (
        "access to managing support users (1 or 0)"
    )
    can_answer_questions_argument_name = (
        "access to answering questions (1 или 0)"
    )
    bind_question_button_text = "Bind"
    unbind_question_button_text = "Unbind"
    estimate_answer_as_useful_button_text = "The answer is useful"
    estimate_answer_as_unuseful_button_text = "The answer is useless"
    show_attachments_button_text = "Show question's attachments"

    def __init__(
        self, tz: timezone | DstTzInfo | BaseTzInfo | StaticTzInfo
    ) -> None:
        self.tz = tz

    # START MESSAGES
    async def get_start_regular_user_message(
        self,
        tg_user: TgUser,
        bot_name: str,
        user_info: RegularUserInfo | None = None,
    ) -> list[str]:
        return [
            f"Hello, {tg_user.first_name}. My name is {bot_name}.\n"
            f"You can send here a message and soon get a reply from one of "
            f"our technical support employees.",
        ]

    async def get_start_support_user_message(
        self,
        tg_user: TgUser,
        bot_name: str,
        user_info: SupportUserInfo | None = None,
    ) -> list[str]:
        return [
            f"Hello, {tg_user.first_name}. My name is {bot_name}.\n"
            f"You are a support user. If you are having some issues "
            f"with using the bot, send /help command."
        ]

    async def get_start_owner_message(
        self,
        tg_user: TgUser,
        bot_name: str,
        user_info: SupportUserInfo | None = None,
    ) -> list[str]:
        return [
            f"Hello, {tg_user.first_name}. My name is {bot_name}.\n"
            f"You are the owner of the bot. If you are having some "
            f"issues with using the bot, send /help command.",
        ]

    # HELP MESSAGES

    async def get_owner_help_message(
        self, tg_user: TgUser, user_info: SupportUserInfo
    ) -> list[str]:
        other_commands_list = "\n".join(
            [
                "Other commands:",
                "/start",
                "/help",
                "/getid",
            ]
        )

        roles_commands_list = "\n".join(
            [
                "Role management commands:",
                "/roles",
                "/role",
                "/addrole",
                "/delrole",
            ]
        )

        support_users_commands_list = "\n".join(
            [
                "Support users management commands:",
                "/supuser",
                "/supusers",
                "/addsupuser",
                "/activatesupuser",
                "/deactivatesupuser",
            ]
        )

        questions_commands_list = "\n".join(
            [
                "Answering questions commands:",
                "/question",
                "/bind",
                "/unbind",
                "/answer",
                "/answers",
            ]
        )

        regular_users_list = "\n".join(
            [
                "Regular users info commands:",
                "/reguser",
            ]
        )

        return [
            "You are the bot's owner.\n"
            "You have access to its full functionality.\n"
            "You can manage support users, create roles, "
            "and answer questions.\n\n"
            "Available commands:\n\n",
            questions_commands_list,
            support_users_commands_list,
            roles_commands_list,
            regular_users_list,
            other_commands_list,
        ]

    async def get_regular_user_help_message(
        self,
        tg_user: TgUser,
        user_info: RegularUserInfo | None = None,
    ) -> list[str]:
        return [
            "To ask a question, you can simply send a message.\n"
            "To add an *attachment* to a question (for example, "
            "photos, videos, voice messages and other files), "
            "just ask the question and then send the files to this chat.\n\n"
            "Keep in mind that after asking a question or sending "
            "an attachment you *won't be able to delete them*!"
        ]

    async def get_support_user_help_message(
        self, tg_user: TgUser, support_user_info: SupportUserInfo
    ) -> list[str]:
        if not support_user_info.support_user_dto.role:
            return [
                "You are a support user with no role. "
                "To access to the bot's functionality, "
                "contact the owner or a support user, having "
                "enough rights for roles assigning"
            ]

        permissions = support_user_info.support_user_dto.role.permissions

        other_commands_list = "\n".join(
            [
                "Other commands:",
                "/start",
                "/help",
                "/getid",
            ]
        )

        roles_commands_list = "\n".join(
            [
                "Roles management commands:",
                "/roles",
                "/role",
                "/addrole",
            ]
        )

        support_users_commands_list = "\n".join(
            [
                "Support users management commands:",
                "/supuser",
                "/supusers",
                "/addsupuser",
                "/activatesupuser",
                "/deactivatesupuser",
            ]
        )

        questions_commands_list = "\n".join(
            [
                "Answering questions commands:",
                "/question",
                "/bind",
                "/unbind",
                "/answer",
                "/answers",
            ]
        )

        regular_users_list = "\n".join(
            [
                "Regular users info commands:",
                "/reguser",
            ]
        )

        commands = "\n\n".join(
            filter(
                lambda x: x,
                [
                    "Available commands:",
                    questions_commands_list
                    if permissions.can_answer_questions
                    else "",
                    support_users_commands_list
                    if permissions.can_manage_support_users
                    else "",
                    roles_commands_list
                    if permissions.can_manage_support_users
                    else "",
                    regular_users_list
                    if permissions.can_answer_questions
                    else "",
                    other_commands_list,
                ],
            )
        )

        return [
            "You are a support user.\n",
            f"Your role's permitted functions:\n"
            f"Support users management: "
            f"{'yes' if permissions.can_manage_support_users else 'no'}\n"
            f"Answering questions: "
            f"{'yes' if permissions.can_answer_questions else 'no'}\n",
            commands,
        ]

    # ARGUMENTS MESSAGES

    async def get_incorrect_num_of_arguments_message(
        self, arguments_list: list[str]
    ) -> list[str]:
        return [
            "Incorrect arguments for this command. Required arguments:"
            + ", ".join(
                arguments_list,
            ),
        ]

    async def get_incorrect_arguments_passed_message(
        self,
        arguments_list_needed: list[str],
        arguments_list_passed: list[str],
    ) -> list[str]:
        if len(arguments_list_needed) > len(arguments_list_passed):
            return [
                "Too many arguments passed. "
                "Arguments list: "
                + ", ".join(
                    arguments_list_needed,
                ),
            ]

        if len(arguments_list_needed) < len(arguments_list_passed):
            return [
                "Not enough arguments passed. "
                "Arguments list: "
                + ", ".join(
                    arguments_list_needed,
                ),
            ]

        return [
            "Incorrect arguments for this command. "
            "Arguments list: "
            + ", ".join(
                arguments_list_needed,
            ),
        ]

    async def get_no_object_with_this_id_message(self, id: str) -> list[str]:
        return [f"No object with such id: {id}"]

    async def get_unavailable_or_deleted_object_message(self) -> list[str]:
        return ["This object is unavailable or was deleted"]

    # ADDITION MESSAGES

    async def get_successful_role_addition_message(
        self,
        role: RoleDTO,
    ) -> list[str]:
        return [
            f"Role with name `{role.name}` successfully added!\n\n"
            f"Its ID: `{role.id}`\n"
            f"Its permissions:\n"
            f"Answering questions: "
            f"{'yes' if role.permissions.can_answer_questions else 'no'}\n"
            f"Support users management: "
            f"{'yes' if role.permissions.can_manage_support_users else 'no'}"
        ]

    async def get_role_name_duplicate_message(
        self,
    ) -> list[str]:
        return ["Role with this name already exists"]

    async def get_successful_support_user_addition_message(
        self,
        support_user: SupportUserDTO,
    ) -> list[str]:
        return [
            f"Support user with name "
            f"`{support_user.descriptive_name}`, "
            f"`The role ID: "
            f"{support_user.role.id if support_user.role else '(no role)'}` "
            f"Successfully added!!\n"
            f"Theirs ID: `{support_user.tg_bot_id}`"
        ]

    async def get_successful_answering_message(
        self,
        question: QuestionDTO,
        answer: AnswerDTO,
    ) -> list[str]:
        return [
            f"Question with ID: {question.tg_message_id} successfully "
            f"answered. The answer now has next ID: {answer.tg_message_id}"
        ]

    async def get_successful_asking_message(
        self,
        question: QuestionDTO,
    ) -> list[str]:
        return [
            "The question successfully asked. As soon as a technical "
            "support employee answers your question, the message will "
            "be sent to this chat. Answering can take a while"
        ]

    async def get_support_user_already_exists_message(
        self, support_user: SupportUserDTO
    ) -> list[str]:
        return ["A user with such ID already is a support user"]

    # DELETING OBJECTS MESSAGES

    async def role_deleted_message(
        self,
        role: RoleDTO,
    ) -> list[str]:
        return [f"Role with ID: {role.id} successfully deleted"]

    # ONE OBJECT INFO MESSAGES

    async def get_role_info_message(
        self,
        role_info: RoleInfo,
    ) -> list[str]:
        can_answer_questions = (
            "*yes*"
            if role_info.role_dto.permissions.can_answer_questions
            else "*no*"
        )
        can_manage_support_users = (
            "*yes*"
            if role_info.role_dto.permissions.can_manage_support_users
            else "*no*"
        )

        return [
            f"*ID роли*: `{role_info.role_dto.id}`\n"
            f"*Имя роли*: `{role_info.role_dto.id}`\n\n"
            "*Её права*:\n\n"
            "Может отвечать на вопросы: "
            f"{can_answer_questions}\n"
            "Может управлять пользователями поддержки: "
            f"{can_manage_support_users}\n\n"
            "Всего пользователей с ролью: "
            f"{role_info.statistics.total_users}"
        ]

    async def get_support_user_info_message(
        self, support_user_info: SupportUserInfo
    ) -> list[str]:
        role_desctiption = "*Role*: " + (
            (
                support_user_info.support_user_dto.role
                and f"Role ID: `{support_user_info.support_user_dto.role.id}`)"
            )
            or (
                support_user_info.support_user_dto.is_owner
                and "*this support user is the Owner*"
            )
            or "*no role assigned*"
        )

        join_date = get_eu_formated_datetime(
            support_user_info.support_user_dto.join_date,
            self.tz,  # type: ignore
        )

        return [
            f"*ID*: `{support_user_info.support_user_dto.tg_bot_id}`\n"
            f"*Descriptive name*: "
            f"`{support_user_info.support_user_dto.descriptive_name}`\n\n"
            f"{role_desctiption}\n\n"
            f"*Date of assigment to support users*: "
            f"{join_date}\n\n"
            f"*Statistics*:\n"
            f"Total answers: {support_user_info.statistics.total_answers}\n"
            f"Useful answers: "
            f"{support_user_info.statistics.useful_answers}\n"
            f"Useless answers: "
            f"{support_user_info.statistics.unuseful_answers}\n"
            f"Unestimated answers: "
            f"{support_user_info.statistics.unestimated_answers}"
        ]

    async def get_regular_user_info_message(
        self, regular_user_info: RegularUserInfo
    ) -> list[str]:
        join_date = get_eu_formated_datetime(
            regular_user_info.regular_user_dto.join_date,
            self.tz,  # type: ignore
        )

        return [
            f"ID: `{regular_user_info.regular_user_dto.tg_bot_id}`\n"
            f"Join date: {join_date}\n\n"
            f"Statistics:\n"
            f"Questions asked: {regular_user_info.statistics.asked_questions}\n"  # noqa: E501
            f"Were answered: {regular_user_info.statistics.answered_questions}\n"  # noqa: E501
            f"Were not answered: {regular_user_info.statistics.unanswered_questions}\n"  # noqa: E501
            f"Total answers: {regular_user_info.statistics.answers_for_questions}\n"  # noqa: E501
            f"Useful: {regular_user_info.statistics.useful_answers}\n"
            f"Useless: {regular_user_info.statistics.unuseful_answers}\n"
            f"Unestimated: {regular_user_info.statistics.unestimated_answers}\n"  # noqa: E501
        ]

    async def get_question_info_message(
        self,
        question_info: QuestionInfo,
    ) -> list[str]:
        asking_date = get_us_formated_datetime(
            question_info.question_dto.date, self.tz  # type: ignore
        )

        return [
            f"ID: "
            f"`{question_info.question_dto.tg_message_id}`\n"
            f"Regular user ID: "
            f"`{question_info.regular_user_asked_dto.tg_bot_id}`\n"  # noqa: E501
            f"Asking date: "
            f"{asking_date}\n"
            f"Total answers: "
            f"{question_info.statistics.total_answers}\n"
            f"Total attachments: "
            f"{question_info.statistics.total_attachments}\n",
            "The question's text:",
            f"{question_info.question_dto.message}",
        ]

    async def get_answer_info_message(
        self, answer_info: AnswerInfo
    ) -> list[str]:
        is_useful = answer_info.answer_dto.is_useful

        estimation_description = (
            "The answer wasn't estimated"
            if is_useful is None
            else f"{'The answer was estimated as useful' if  is_useful else 'The answer was estimated as useless'}"  # noqa: E501
        )

        answer_date = get_eu_formated_datetime(
            answer_info.answer_dto.date, self.tz  # type: ignore
        )

        return [
            f"ID: `{answer_info.answer_dto.tg_message_id}`\n"
            f"Question's ID: "
            f"`{answer_info.answered_quetsion_dto.tg_message_id}`\n"
            f"The answer author's ID: "
            f"`{answer_info.support_user_answered_dto.tg_bot_id}`\n"
            f"Answer date: {answer_date}\n"
            f"{estimation_description}\n"
            f"Total attachments: {answer_info.statistics.total_attachments}",
            "Answer text:",
            f"{answer_info.answer_dto.message}",
        ]

    # OBJECTS LIST INFO MESSAGES

    async def get_roles_list_message(
        self,
        roles_list: list[RoleDTO],
    ) -> list[str]:
        if not roles_list:
            return ["No role was added"]

        message = ""
        for role in roles_list:
            created_date = get_eu_formated_datetime(
                role.created_date, self.tz  # type: ignore
            )

            message += (
                f"Name: `{role.name}`; "
                f"ID: `{role.id}`; "
                f"Createin date: {created_date}\n"
            )

        return ["Roles list:", message]

    async def get_questions_list_message(
        self,
        questions_list: list[QuestionDTO],
    ) -> list[str]:
        message = ""
        for question in questions_list:
            # FIXME: Think about how that can be fixed
            message += (
                f"Question's ID: `{question.tg_message_id};` "
                # TODO: Come up with a solution for this thing.
                # NOTE: Might be solved by changing users' UUIDs ids
                # to intger ids which Telegram provides
                # f"ID пользователя: `{question.regular_user.tg_bot_user_id}`; " # noqa: E501
                f"Question's text: {question.message[0:100]}...\n"
            )

        return ["Questions list:", message]

    async def get_answers_list_message(
        self,
        answers_list: list[AnswerDTO],
    ) -> list[str]:
        message = "Answers list:"
        for answer in answers_list:
            answer_text = (
                f"{answer.message[0:100]}..."
                if len(answer.message) > 100
                else answer.message[0:100]
            )

            message += (
                f"\nAnswer's ID: {answer.tg_message_id}; "
                # TODO: Come up with a solution for this thing.
                # NOTE: Might be solved by changing users' UUIDs ids
                # to intger ids which Telegram provides
                # f"ID отвечавшего пользователя: "
                # f"{answer.support_user.tg_bot_user_id}\n"
                f"Answer's text: {answer_text}"
            )

        return [message]

    async def get_support_users_list_message(
        self,
        support_users_list: list[SupportUserDTO],
    ) -> list[str]:
        message = "Support users:"

        for support_user in support_users_list:
            role_desctiption = "Role: " + (
                (support_user.role and f"Role ID: `{support_user.role.id}`")
                or (support_user.is_owner and "this user is the Owner")
                or "no role assigned"
            )

            join_date = get_eu_formated_datetime(
                support_user.join_date, self.tz  # type: ignore
            )

            message += (
                f"\nName: `{support_user.descriptive_name}`; "
                f"ID: `{support_user.tg_bot_id}`; "
                f"{role_desctiption}; "
                f"Assigning date: {join_date}"
            )

        return [message]

    # BINDING MESSAGES

    async def get_question_already_bound_message(
        self, question_id: int, support_user_id: int
    ) -> list[str]:
        return [
            f"Answer with ID: `{question_id}` is already bound to "
            f"another support user with next ID: `{support_user_id}`"
        ]

    async def get_successful_unbinding_message(self) -> list[str]:
        return [
            "Successful unbinding. Now you are not answering a single question"
        ]

    async def get_successful_binding_message(
        self, question: QuestionDTO
    ) -> list[str]:
        return [
            f"Now you are answering a question with next ID: "
            f"{question.tg_message_id}"
        ]

    async def get_no_bound_question_message(self) -> list[str]:
        return ["You are not answering a single question"]

    async def get_no_quetstions_to_answer_left_message(self) -> list[str]:
        return ["No more unanswered or unbound questions left"]

    # ESTIMATION MESSAGES

    async def get_answer_already_estimated_message(
        self, answer: AnswerDTO
    ) -> list[str]:
        return ["The answer is already estimated"]

    async def get_answer_estimated_as_useful_message(
        self, answer: AnswerDTO
    ) -> list[str]:
        return ["The answer is estimated as useful"]

    async def get_answer_estimated_as_unuseful_message(
        self, answer: AnswerDTO
    ) -> list[str]:
        return ["The answer was estimated as useless"]

    # INITIALIZING MESSAGES

    async def get_already_inited_owner_message(
        self, tg_user: TgUser
    ) -> list[str]:
        return ["The bot's owner is already initialized"]

    async def get_successful_owner_init_message(
        self, tg_user: TgUser, support_user_dto: SupportUserDTO
    ) -> list[str]:
        return ["Congratulations, now you are the bot's owner!"]

    async def get_incorrect_owner_password_message(self) -> list[str]:
        return ["Incorrect password. Please, try again"]

    # SUPPORT USER ACTIVATION MESSAGES

    async def get_support_user_deactivation_message(
        self,
        support_user: SupportUserDTO,
    ) -> list[str]:
        return [
            f"Support with ID: {support_user.tg_bot_id} successfully "
            f"deactivated"
        ]

    async def get_support_user_activation_message(
        self,
        support_user: SupportUserDTO,
    ) -> list[str]:
        return [
            f"Support user with ID: {support_user.tg_bot_id} "
            f"successfully activated"
        ]

    # ATTACHMENTS MESSAGES

    async def get_no_last_asked_question_message(
        self, regular_user: RegularUserDTO
    ) -> list[str]:
        return ["You have no last question or it was deleted"]

    async def get_no_last_answer_message(
        self, support_user: SupportUserDTO
    ) -> list[str]:
        return ["You didn't answer anything or your answer was deleted"]

    async def get_question_attachment_addition_message(
        self, question_attachment: AttachmentDTO
    ) -> list[str]:
        return ["An attachment to the last question was successfully added"]

    async def get_answer_attachment_addition_message(
        self, answer_attachment: AttachmentDTO
    ) -> list[str]:
        return ["An attachment to the last answer was successfully added"]

    # OTHER MESSAGES

    async def get_global_statistics_message(
        self, global_statistics: GlobalStatistics
    ) -> list[str]:
        return [
            "General statistics:\n"
            f"Total regular users: "
            f"*{global_statistics.total_regular_users}*\n"
            f"Total support users: "
            f"*{global_statistics.total_support_users}*\n"
            f"Total roles: "
            f"*{global_statistics.total_roles}*\n"
            f"Total questions: *{global_statistics.total_questions}*\n"
            f"Total answered questions: "
            f"*{global_statistics.total_answered_questions}*\n"
            f"Total unanswered questions: "
            f"*{global_statistics.total_unanswered_questions}*\n"
            f"Total questions attachments: "
            f"*{global_statistics.total_question_attachments}*\n"
            f"Total answers: "
            f"*{global_statistics.total_answers}*\n"
            f"Total useful answers: "
            f"*{global_statistics.total_useful_answers}*\n"
            f"Total useless answers: "
            f"*{global_statistics.total_unuseful_answers}*\n"
            f"Total unestimated answers: "
            f"*{global_statistics.total_unuseful_answers}*\n"
            f"Total answers attachments: "
            f"*{global_statistics.total_answer_attachments}*\n"
        ]

    async def get_id_message(self, id: int) -> list[str]:
        return ["Your user's ID for this bot:", str(id)]

    async def get_permission_denied_message(
        self, tg_user: TgUser
    ) -> list[str]:
        return ["Permission denied"]

    async def get_answer_for_regular_user_message(
        self,
        question_dto: QuestionDTO,
        answer_dto: AnswerDTO,
        include_question: bool = False,
    ) -> list[str]:
        if include_question:
            return [
                "Your question was answered:",
                "Question:",
                f"{question_dto.message}",
                "Anser:",
                f"{answer_dto.message}",
            ]

        return [
            "Your question was answered:",
            f"{answer_dto.message}",
        ]

    async def get_no_question_attachments_message(
        self, question: QuestionDTO
    ) -> list[str]:
        return ["No attachments for this question"]

    async def get_unsupported_message_type_message(self) -> list[str]:
        return [
            "We are sorry, but this file format is not currently supported"
        ]

    async def get_unknown_command_message(self) -> list[str]:
        return [
            "No such command. If you are having some issues using the bot, "
            "enter /help"
        ]

    async def get_regular_user_not_authorized_message(self) -> list[str]:
        return ["Enter /start command to continue using the bot"]
