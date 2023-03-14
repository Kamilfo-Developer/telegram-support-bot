from telegram import User
from bot.entities.regular_user import RegularUser
from bot.entities.support_user import SupportUser
from bot.entities.question import Question
from bot.entities.answer import Answer
from bot.localization.messages_content import MessagesContent
from bot.entities.role import Role
from bot.services.statistics import (
    GlobalStatistics,
    RoleStatistics,
    AnswerStatistics,
    QuestionStatistics,
    SupportUserStatistics,
    RegularUserStatistics,
)
from pytz.tzinfo import DstTzInfo, BaseTzInfo, StaticTzInfo
from datetime import timezone


from bot.utils import get_us_formated_datetime


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
        telegram_user: User,
        user_entity: RegularUser | None = None,
    ) -> list[str]:
        bot = telegram_user.get_bot()
        return [
            f"Hello, {telegram_user.first_name}. My name is {bot.name}.\n"
            + "You can send here a message and soon get a reply from one of our technical support employees.",
        ]

    async def get_start_support_user_message(
        self,
        telegram_user: User,
        user_entity: SupportUser | None = None,
    ) -> list[str]:
        bot = telegram_user.get_bot()
        return [
            f"Hello, {telegram_user.first_name}. My name is {bot.name}.\n"
            + "You are a support user. If you are having some issues with using the bot, send /help command."
        ]

    async def get_start_owner_message(
        self,
        telegram_user: User,
        user_entity: SupportUser,
    ) -> list[str]:
        bot = telegram_user.get_bot()

        return [
            f"Hello, {telegram_user.first_name}. My name is {bot.name}.\n"
            + "You are the owner of the bot. If you are having some issues with using the bot, send /help command.",
        ]

    # HELP MESSAGES

    async def get_owner_help_message(
        self,
        user: User,
        user_entity: SupportUser,
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
            + "You have access to its full functionality.\n"
            + "You can manage support users, create roles, and answer questions.\n\n"
            "Available commands:\n\n",
            questions_commands_list,
            support_users_commands_list,
            roles_commands_list,
            regular_users_list,
            other_commands_list,
        ]

    async def get_regular_user_help_message(self, user: User) -> list[str]:
        return [
            "To ask a question, you can simply send a message.\n"
            + "To add an *attachment* to a question (for example, photos, videos, voice messages and other files), just ask the question and then send the files to this chat.\n\n"
            + "Keep in mind that after asking a question or sending an attachment you *won't be able to delete them*!"
        ]

    async def get_support_user_help_message(
        self, tg_user: User, support_user: SupportUser
    ) -> list[str]:
        if not support_user.role:
            return [
                "You are a support user with no role. To access to bot's functionality, contact the owner or a support user, having enough rights for roles assigning"
            ]

        permissions = support_user.role.permissions

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
            "You role's permitted functions:\n"
            + f"Support users management: {'yes' if permissions.can_manage_support_users else 'no'}\n"
            + f"Answering questions: {'yes' if permissions.can_answer_questions else 'no'}\n",
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

    async def get_incorrect_arguments_passed_message(self) -> list[str]:
        return ["Invalid argument(s). Please, try again"]

    async def get_no_object_with_this_id_message(self, id: str) -> list[str]:
        return [f"No object with such id: {id}"]

    async def get_unavailable_or_deleted_object_message(self) -> list[str]:
        return ["This object is unavailable or was deleted"]

    # ADDITION MESSAGES

    async def get_successful_role_addition_message(
        self,
        role: Role,
    ) -> list[str]:
        return [
            f"Role with name `{role.name}` successfully added!\n\n"
            + f"Its ID: `{role.id}`\n"
            + "Its permissions:\n"
            + f"Answering questions: {'yes' if role.permissions.can_answer_questions else 'no'}\n"
            + f"Support users management: {'yes' if role.permissions.can_manage_support_users else 'no'}"
        ]

    async def get_role_name_duplicate_message(
        self,
    ) -> list[str]:
        return ["Role with this name already exists"]

    async def get_successful_support_user_addition_message(
        self,
        support_user: SupportUser,
    ) -> list[str]:
        return [
            f"Support user with name `{support_user.descriptive_name}`, with role `{support_user.role.name if support_user.role else '(no role)'}` successfully added!\n"
            + f"Theirs ID: `{support_user.tg_bot_user_id}`"
        ]

    async def get_successful_answering_message(
        self,
        question: Question,
        answer: Answer,
    ) -> list[str]:
        return [
            f"Question with ID: {question.tg_message_id} successfully answered. The answer now has next ID: {answer.tg_message_id}"
        ]

    async def get_successful_asking_message(
        self,
        question: Question,
    ) -> list[str]:
        return [
            "The question successfully asked. As soon as a technical support employee answers your question, the message will be sent to this chat. Answering can take a while"
        ]

    async def get_support_user_already_exists_message(
        self, support_user: SupportUser
    ) -> list[str]:
        return ["A user with such ID already is a support user"]

    # DELETING OBJECTS MESSAGES

    async def role_deleted_message(
        self,
        role: Role,
    ) -> list[str]:
        return [f"Role with ID: {role.id} successfully deleted"]

    # ONE OBJECT INFO MESSAGES

    async def get_role_info_message(
        self,
        role: Role,
        role_statistics: RoleStatistics,
    ) -> list[str]:
        return [
            f"*The role's ID*: `{role.id}`\n"
            + f"*The role's name*: `{role.name}`\n\n"
            + "*Its permissions*:\n\n"
            + "Can answer questions: "
            + f"{'*yes*' if role.permissions.can_answer_questions else '*no*'}\n"
            + "Can manage support users: "
            + f"{'*yes*' if role.permissions.can_manage_support_users else '*no*'}\n\n"
            + "Support users with this role: "
            + f"{role_statistics.total_users}"
        ]

    async def get_support_user_info_message(
        self,
        support_user: SupportUser,
        support_user_statistics: SupportUserStatistics,
    ) -> list[str]:
        role_desctiption = "*Role*: " + (
            (
                support_user.role
                and f"`{support_user.role.name}` (the role's ID: `{support_user.role.id}`)"
            )
            or (support_user.is_owner and "*the support user is the owner*")
            or "*no role assigned*"
        )

        return [
            f"*ID*: `{support_user.tg_bot_user_id}`\n"
            + f"*Descriptive name*: `{support_user.descriptive_name}`\n\n"
            + f"{role_desctiption}\n\n"
            + f"*Appointment date*: {get_us_formated_datetime(support_user.join_date, self.tz)}\n\n"
            + "*Statistics*:\n"
            + f"Total answers: {support_user_statistics.total_answers}\n"
            + f"Useful answers: {support_user_statistics.useful_answers}\n"
            + f"Useless answers: {support_user_statistics.unuseful_answers}\n"
            + f"Unestimated answers: {support_user_statistics.unestimated_answers}"
        ]

    async def get_regular_user_info_message(
        self,
        regular_user: RegularUser,
        regular_user_statistics: RegularUserStatistics,
    ) -> list[str]:
        return [
            f"ID: `{regular_user.tg_bot_user_id}`\n"
            + f"Join date: {get_us_formated_datetime(regular_user.join_date, self.tz)}\n\n"
            + f"Statistics:\n"
            + f"Questions asked: {regular_user_statistics.asked_questions}\n"
            + f"Were answered: {regular_user_statistics.answered_questions}\n"
            + f"Were not answered: {regular_user_statistics.unanswered_questions}\n"
            + f"Total answers: {regular_user_statistics.answers_for_questions}\n"
            + f"Useful: {regular_user_statistics.useful_answers}\n"
            + f"Useless: {regular_user_statistics.unuseful_answers}\n"
            + f"Unestimated: {regular_user_statistics.unestimated_answers}\n"
        ]

    async def get_question_info_message(
        self,
        question: Question,
        question_statistics: QuestionStatistics,
    ) -> list[str]:
        return [
            f"ID: `{question.tg_message_id}`\n"
            + f"Regular user ID: `{question.regular_user.tg_bot_user_id}`\n"
            + f"Asking date: {get_us_formated_datetime(question.date, self.tz)}\n"
            + f"Total answers: {question_statistics.total_answers}\n"
            + f"Total attachments: {question_statistics.total_attachments}\n",
            "The question's text:",
            f"{question.message}",
        ]

    async def get_answer_info_message(
        self,
        answer: Answer,
        answer_statistics: AnswerStatistics,
    ) -> list[str]:
        estimation_description = (
            "The answer wasn't estimated"
            if answer.is_useful is None
            else f"{'The answer was estimated as useful' if answer.is_useful else 'The answer was estimated as useless'}"
        )
        return [
            f"ID: `{answer.tg_message_id}`\n"
            + f"Question's ID: `{answer.question.tg_message_id}`\n"
            + f"The answer's author: {answer.support_user.descriptive_name} (Support user's ID: `{answer.support_user.tg_bot_user_id}`)\n"
            + f"The answer's date: {get_us_formated_datetime(answer.date, self.tz)}\n{estimation_description}\n"
            + f"Total attachments: {answer_statistics.total_attachments}",
            "The answer's text:",
            f"{answer.message}",
        ]

    # OBJECTS LIST INFO MESSAGES

    async def get_roles_list_message(
        self,
        roles_list: list[Role],
    ) -> list[str]:
        if not roles_list:
            return ["No role was added"]

        message = ""
        for role in roles_list:
            message += f"Name: `{role.name}`; ID: `{role.id}`; Creation date: {get_us_formated_datetime(role.created_date, self.tz)}\n"

        return ["Roles list:", message]

    async def get_questions_list_message(
        self,
        questions_list: list[Question],
    ) -> list[str]:
        message = ""
        for question in questions_list:
            message += f"Question's ID: {question.tg_message_id}; Regular user's ID: {question.regular_user.tg_bot_user_id}; Question's text: {question.message[0:100]}...\n"

        return ["Questions list:", message]

    async def get_answers_list_message(
        self,
        answers_list: list[Answer],
    ) -> list[str]:
        message = "Answers list:"
        for answer in answers_list:
            message += (
                f"\nAnswer's ID: {answer.tg_message_id}; Support user's ID: {answer.support_user.tg_bot_user_id}\n"
                + f"Answer's text: {f'{answer.message[0:100]}...' if len(answer.message) > 100 else answer.message[0:100]}"
            )

        return [message]

    async def get_support_users_list_message(
        self,
        support_users_list: list[SupportUser],
    ) -> list[str]:
        message = "Support users:"

        for support_user in support_users_list:
            role_desctiption = "Role: " + (
                (
                    support_user.role
                    and f"`{support_user.role.name}` (Role's ID: `{support_user.role.id}`)"
                )
                or (support_user.is_owner and "the user is owner")
                or "no role assigned"
            )

            message += f"\nName: `{support_user.descriptive_name}`; ID: `{support_user.tg_bot_user_id}`; {role_desctiption}; Appointment date: {get_us_formated_datetime(support_user.join_date, self.tz)}"

        return [message]

    # BINDING MESSAGES

    async def get_question_already_binded_message(
        self, question_id: int, support_user_id: int
    ) -> list[str]:
        return [
            f"Answer with ID: `{question_id}` is already binded to another support user with next ID: `{support_user_id}`"
        ]

    async def get_successful_unbinding_message(self) -> list[str]:
        return [
            "Successful unbinding. Now you are not answering a single question"
        ]

    async def get_successful_binding_message(
        self, question: Question
    ) -> list[str]:
        return [
            f"Now you are answering a question with next ID: {question.tg_message_id}"
        ]

    async def get_no_binded_question_message(self) -> list[str]:
        return ["You are not answering a single question"]

    async def get_no_unbinded_quetstions_left_message(self) -> list[str]:
        return ["No more unanswered or unbinded questions left"]

    # ESTIMATION MESSAGES

    async def get_answer_already_estimated_message(
        self, answer: Answer
    ) -> list[str]:
        return ["The answer is already estimated"]

    async def get_answer_estimated_as_useful_message(
        self, answer: Answer
    ) -> list[str]:
        return ["The answer is estimated as useful"]

    async def get_answer_estimated_as_unuseful_message(
        self, answer: Answer
    ) -> list[str]:
        return ["The answer was estimated as useless"]

    # INITIALIZING MESSAGES

    async def get_already_inited_owner_message(self, user: User) -> list[str]:
        return ["The bot's owner is already initialized"]

    async def get_successful_owner_init_message(
        self, user: User, support_user: SupportUser
    ) -> list[str]:
        return ["Congratulations, now you are the bot's owner!"]

    async def get_incorrect_owner_password_message(self) -> list[str]:
        return ["Incorrect password. Please, try again"]

    # SUPPORT USER ACTIVATION MESSAGES

    async def get_support_user_deactivation_message(
        self,
        support_user: SupportUser,
    ) -> list[str]:
        return [
            f"Support with ID: {support_user.tg_bot_user_id} successfully deactivated"
        ]

    async def get_support_user_activation_message(
        self,
        support_user: SupportUser,
    ) -> list[str]:
        return [
            f"Support user with ID: {support_user.tg_bot_user_id} successfully activated"
        ]

    # ATTACHMENTS MESSAGES

    async def get_no_last_asked_question_message(
        self, regular_user: RegularUser
    ) -> list[str]:
        return ["You have no last question or it was deleted"]

    async def get_no_last_answer_message(
        self, support_user: SupportUser
    ) -> list[str]:
        return ["You didn't answer anything or your answer was deleted"]

    async def get_question_attachment_addition_message(
        self, support_user: RegularUser
    ) -> list[str]:
        return ["An attachment to the last question was successfully added"]

    async def get_answer_attachment_addition_message(
        self, support_user: SupportUser
    ) -> list[str]:
        return ["An attachment to the last answer was successfully added"]

    # OTHER MESSAGES

    async def get_global_statistics_message(
        self, global_statistics: GlobalStatistics
    ) -> list[str]:
        return [
            "General statistics:\n"
            + f"Total regular users: *{global_statistics.total_regular_users}*\n"
            + f"Total support users: *{global_statistics.total_support_users}*\n"
            + f"Total roles: *{global_statistics.total_roles}*\n"
            + f"Total questions: *{global_statistics.total_questions}*\n"
            + f"Total answered questions: *{global_statistics.total_answered_questions}*\n"
            + f"Total unanswered questions: *{global_statistics.total_unanswered_questions}*\n"
            + f"Total questions attachments: *{global_statistics.total_questions_attachments}*\n"
            + f"Total answers: *{global_statistics.total_answers}*\n"
            + f"Total useful answers: *{global_statistics.total_useful_answers}*\n"
            + f"Total useless answers: *{global_statistics.total_unuseful_answers}*\n"
            + f"Total unestimated answers: *{global_statistics.total_unestimated_ansers}*\n"
            + f"Total answers attachments: *{global_statistics.total_answers_attachments}*\n"
        ]

    async def get_id_message(self, id: int) -> list[str]:
        return ["Your user's ID for this bot:", str(id)]

    async def get_permission_denied_message(self, user: User) -> list[str]:
        return ["Permission denied"]

    async def get_answer_for_regular_user_message(
        self,
        answer: Answer,
        include_question: bool = False,
    ) -> list[str]:
        if include_question:
            return [
                "Your question was answered:",
                "Question:",
                f"{answer.question.message}",
                "Anser:",
                f"{answer.message}",
            ]

        return [
            "Your question was answered:",
            f"{answer.message}",
        ]

    async def get_no_question_attachments_message(
        self, question: Question
    ) -> list[str]:
        return ["No attachments for this question"]

    async def get_unsupported_message_type_message(self) -> list[str]:
        return [
            "We are sorry, but this file format is not currently supported"
        ]

    async def get_unknown_command_message(self) -> list[str]:
        return [
            "No such command. If you are having some issues using the bot, enter /help"
        ]

    async def get_regular_user_not_authorized_message(self) -> list[str]:
        return ["Enter /start command to continue using the bot"]
