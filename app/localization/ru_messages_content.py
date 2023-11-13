from datetime import timezone

from pytz.tzinfo import BaseTzInfo, DstTzInfo, StaticTzInfo


from app.bot.dtos import TgUser


from app.localization.messages_content import MessagesContent

from app.regular_users.dtos import RegularUserDTO


from app.shared.dtos import (
    AnswerDTO,
    AttachmentDTO,
    QuestionDTO,
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


from app.utils import get_eu_formated_datetime


class RUMessagesContent(MessagesContent):
    # ARGUMENTS NAMES MESSAGE TEMPLATES
    owner_password_argument_name = "пароль владельца бота"
    regular_user_id_argument_name = "ID обычного пользователя"
    regular_user_tg_bot_id_argument_name = (
        "ID обычного пользователя в Телеграме у данного бота (число)"
    )
    support_user_id_argument_name = "ID пользователя поддержки"
    role_id_argument_name = "ID роли"
    support_user_descriptive_name = "описательное имя"
    role_name_argument_name = "имя роли"
    question_id_argument_name = "ID вопроса"
    answer_id_argument_name = "ID ответа"
    can_manage_support_users_role_argument_name = (
        "может ли управлять пользователями поддержки (1 или 0)"
    )
    can_answer_questions_argument_name = (
        "может ли отвечать на вопросы (1 или 0)"
    )
    bind_question_button_text = "Привязать"
    unbind_question_button_text = "Отвязать"
    estimate_answer_as_useful_button_text = "Ответ полезен"
    estimate_answer_as_unuseful_button_text = "Ответ бесполезен"
    show_attachments_button_text = "Показать приложения к вопросу"

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
            f"Здравствуйте, {tg_user.first_name}. "
            f"Вас приветствует {bot_name}.\n"
            f"Вы можете написать сюда сообщение и в скором времени "
            f"Вам придёт ответ от одного из наших сотрудников поддержки.",
        ]

    async def get_start_support_user_message(
        self,
        tg_user: TgUser,
        bot_name: str,
        user_info: SupportUserInfo | None = None,
    ) -> list[str]:
        return [
            f"Здравствуйте, {tg_user.first_name}. "
            f"Вас приветствует {bot_name}.\n"
            f"Вы являетесь пользователь поддержки. "
            f"Если возникли трудности, введите команду /help."
        ]

    async def get_start_owner_message(
        self,
        tg_user: TgUser,
        bot_name: str,
        user_info: SupportUserInfo,
    ) -> list[str]:
        return [
            f"Здравствуйте, {tg_user.first_name}. "
            f"Вас приветствует {bot_name}.\n"
            f"Вы являетесь владельцем бота. "
            f"Если возникли трудности, введите команду /help.",
        ]

    # HELP MESSAGES

    async def get_owner_help_message(
        self,
        tg_user: TgUser,
        user_info: SupportUserInfo,
    ) -> list[str]:
        other_commands_list = "\n".join(
            [
                "Другие команды:",
                "/start",
                "/help",
                "/getid",
            ]
        )

        roles_commands_list = "\n".join(
            [
                "Комады для управления ролями:",
                "/roles",
                "/role",
                "/addrole",
            ]
        )

        support_users_commands_list = "\n".join(
            [
                "Команды управления пользователями поддержки:",
                "/supuser",
                "/supusers",
                "/addsupuser",
                "/activatesupuser",
                "/deactivatesupuser",
            ]
        )

        questions_commands_list = "\n".join(
            [
                "Команды для ответов на вопросы:",
                "/question",
                "/bind",
                "/unbind",
                "/answer",
                "/answers",
            ]
        )

        regular_users_list = "\n".join(
            [
                "Команды для получения информации об обычных пользователях:",
                "/reguser",
            ]
        )

        return [
            "Вы являетесь владельцем бота.\n"
            "Вам доступен его полный функционал.\n"
            "Вы можете управлять пользователями поддержки, создавать роли, "
            "а также самостоятельно отвечать на вопросы.\n\n"
            "Доступные команды:\n\n",
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
            "Чтобы задать вопрос, Вы можете просто отправить сообщение.\n"
            "Чтобы добавить *приложения* к вопросу (например фото, видео, "
            "голосовые сообщения и другие файты), просто задайте вопрос, "
            "а затем пришлите в этот чат нужный файл.\n\n"
            "Имейте в виду, что после того, как Вы зададите вопрос или "
            "отправите приложение к нему, *их нельзя будет удалить*!"
        ]

    async def get_support_user_help_message(
        self, tg_user: TgUser, user_info: SupportUserInfo
    ) -> list[str]:
        if not user_info.support_user_dto.role:
            return [
                "Вы являетесь пользователем поддержки. Однако у Вас нет роли. "
                "Чтобы выполнять какие-либо действия, Вам необходимо получить "
                "её. Для этого свяжитесь с владельцем бота или с другим "
                "пользователем, способным назначать роли"
            ]

        permissions = user_info.support_user_dto.role.permissions

        other_commands_list = "\n".join(
            [
                "Другие команды:",
                "/start",
                "/help",
                "/getid",
            ]
        )

        roles_commands_list = "\n".join(
            [
                "Комады для управления ролями:",
                "/roles",
                "/role",
                "/addrole",
                "/delrole",
            ]
        )

        support_users_commands_list = "\n".join(
            [
                "Команды управления пользователями поддержки:",
                "/supuser",
                "/supusers",
                "/addsupuser",
                "/activatesupuser",
                "/deactivatesupuser",
            ]
        )

        questions_commands_list = "\n".join(
            [
                "Команды для ответов на вопросы:",
                "/question",
                "/bind",
                "/unbind",
                "/answer",
                "/answers",
            ]
        )

        regular_users_list = "\n".join(
            [
                "Команды для получения информации об обычных пользователях:",
                "/reguser",
            ]
        )

        commands = "\n\n".join(
            filter(
                lambda x: x,
                [
                    "Доступные команды:",
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
            "Вы являетесь пользователем поддержки.\n",
            f"Возможности Вашей роли:\n"
            f"Управление пользователями поддержки: "
            f"{'да' if permissions.can_manage_support_users else 'нет'}\n"
            f"Ответы на вопросы: "
            f"{'да' if permissions.can_answer_questions else 'нет'}\n",
            commands,
        ]

    # ARGUMENTS MESSAGES

    async def get_incorrect_num_of_arguments_message(
        self, arguments_list: list[str]
    ) -> list[str]:
        return [
            "Неправильные аргументы для данной команды. "
            "Необходимые аргументы: "
            + ", ".join(
                arguments_list,
            ),
        ]

    async def get_incorrect_arguments_passed_message(
        self,
        arguments_list_needed: list[str],
        arguments_list_passed: list[str],
    ) -> list[str]:
        if len(arguments_list_passed) > len(arguments_list_needed):
            return [
                "Передано слишком много аргументов. "
                "Список аргументов для данной команды: "
                + ", ".join(
                    arguments_list_needed,
                ),
            ]

        if len(arguments_list_needed) > len(arguments_list_passed):
            return [
                "Передано недостаточно аргументов. "
                "Список аргументов для данной команды: "
                + ", ".join(
                    arguments_list_needed,
                ),
            ]

        return [
            "Неправильные аргументы для данной команды. "
            "Список аргументов для данной команды: "
            + ", ".join(
                arguments_list_passed,
            ),
        ]

    async def get_no_object_with_this_id_message(self, id: str) -> list[str]:
        return [f"Нет объекта с таким ID: {id}"]

    async def get_unavailable_or_deleted_object_message(self) -> list[str]:
        return ["Данный объект недоступен или был удалён"]

    # ADDITION MESSAGES

    async def get_successful_role_addition_message(
        self,
        role: RoleDTO,
    ) -> list[str]:
        return [
            f"Роль с названием `{role.name}` успешно добавлена!\n\n"
            f"Её ID: `{role.id}`\n"
            f"Её права:\n"
            f"Может отвечать на вопросы: "
            f"{'да' if role.permissions.can_answer_questions else 'нет'}\n"
            f"Может управлять пользователями поддержки: "
            f"{'да' if role.permissions.can_manage_support_users else 'нет'}"
        ]

    async def get_role_name_duplicate_message(
        self,
    ) -> list[str]:
        return ["Роль с таким именем уже существует"]

    async def get_successful_support_user_addition_message(
        self,
        support_user: SupportUserDTO,
    ) -> list[str]:
        return [
            f"Пользователь поддержки с именем "
            f"`{support_user.descriptive_name}`, "
            f"`ID роли: "
            f"{support_user.role.id if support_user.role else '(без роли)'}` "
            f"успешно добавлен!\n"
            f"Пользователь поддержки получил ID: `{support_user.tg_bot_id}`"
        ]

    async def get_successful_answering_message(
        self,
        question: QuestionDTO,
        answer: AnswerDTO,
    ) -> list[str]:
        return [
            f"Вопрос с ID: {question.tg_message_id} успешно отвечен. "
            f"Ответ получил ID: {answer.tg_message_id}"
        ]

    async def get_successful_asking_message(
        self,
        question: QuestionDTO,
    ) -> list[str]:
        return [
            "Вопрос успешно задан. Как только сотрудник поддержки ответит "
            "на Ваш вопрос, Вам придёт сообщение в этот чат. "
            "Ответ на вопрос может занять некоторое время"
        ]

    async def get_support_user_already_exists_message(
        self, support_user: SupportUserDTO
    ) -> list[str]:
        return ["Пользователь с таким ID уже является пользователем поддержки"]

    # DELETING OBJECTS MESSAGES

    async def role_deleted_message(
        self,
        role: RoleDTO,
    ) -> list[str]:
        return [f"Роль с ID: {role.id} успешно удалена"]

    # ONE OBJECT INFO MESSAGES

    async def get_role_info_message(
        self,
        role_info: RoleInfo,
    ) -> list[str]:
        can_answer_questions = (
            "*да*"
            if role_info.role_dto.permissions.can_answer_questions
            else "*нет*"
        )
        can_manage_support_users = (
            "*да*"
            if role_info.role_dto.permissions.can_manage_support_users
            else "*нет*"
        )

        return [
            f"*ID роли*: `{role_info.role_dto.id}`\n"
            f"*Имя роли*: `{role_info.role_dto.name}`\n\n"
            "*Её права*:\n\n"
            "Может отвечать на вопросы: "
            f"{can_answer_questions}\n"
            "Может управлять пользователями поддержки: "
            f"{can_manage_support_users}\n\n"
            "Всего пользователей с ролью: "
            f"{role_info.statistics.total_users}"
        ]

    async def get_support_user_info_message(
        self,
        support_user_info: SupportUserInfo,
    ) -> list[str]:
        role_desctiption = "*Роль*: " + (
            (
                support_user_info.support_user_dto.role
                and f"ID Роли: `{support_user_info.support_user_dto.role.id}`)"
            )
            or (
                support_user_info.support_user_dto.is_owner
                and "*пользователь является владельцем*"
            )
            or "*роль не назначена*"
        )

        join_date = get_eu_formated_datetime(
            support_user_info.support_user_dto.join_date,
            self.tz,  # type: ignore
        )

        return [
            f"*ID*: `{support_user_info.support_user_dto.tg_bot_id}`\n"
            f"*Имя*: "
            f"`{support_user_info.support_user_dto.descriptive_name}`\n\n"
            f"{role_desctiption}\n\n"
            f"*Дата назначения*: "
            f"{join_date}\n\n"
            f"*Статистика*:\n"
            f"Всего ответов: {support_user_info.statistics.total_answers}\n"
            f"Полезных ответов: "
            f"{support_user_info.statistics.useful_answers}\n"
            f"Бесполезных ответов: "
            f"{support_user_info.statistics.unuseful_answers}\n"
            f"Неоценённых ответов: "
            f"{support_user_info.statistics.unestimated_answers}"
        ]

    async def get_regular_user_info_message(
        self,
        regular_user_info: RegularUserInfo,
    ) -> list[str]:
        join_date = get_eu_formated_datetime(
            regular_user_info.regular_user_dto.join_date,
            self.tz,  # type: ignore
        )

        return [
            f"ID: `{regular_user_info.regular_user_dto.tg_bot_id}`\n"
            f"Дата присоединения: "
            f"{join_date}\n\n"
            f"Статистика:\n"
            f"Задано вопросов: "
            f"{regular_user_info.statistics.asked_questions}\n"
            f"Из них ответ получили: "
            f"{regular_user_info.statistics.answered_questions}\n"
            f"Из них ответ не получили: "
            f"{regular_user_info.statistics.unanswered_questions}\n"
            f"Всего ответов на вопросы пользователя: "
            f"{regular_user_info.statistics.answers_for_questions}\n"
            f"Из них полезных: "
            f"{regular_user_info.statistics.useful_answers}\n"
            f"Из них бесполезных: "
            f"{regular_user_info.statistics.unuseful_answers}\n"
            f"Из них неоценённых: "
            f"{regular_user_info.statistics.unestimated_answers}\n"
        ]

    async def get_question_info_message(
        self,
        question_info: QuestionInfo,
    ) -> list[str]:
        asked_date = get_eu_formated_datetime(
            question_info.question_dto.date, self.tz  # type: ignore
        )

        return [
            f"ID: `{question_info.question_dto.tg_message_id}`\n"
            f"ID задавшего вопрос пользователя: "
            f"`{question_info.regular_user_asked_dto.tg_bot_id}`\n"
            f"Вопрос был задан: "
            f"{asked_date}\n"
            f"Ответов на вопрос: "
            f"{question_info.statistics.total_answers}\n"
            f"Всего приложений: "
            f"{question_info.statistics.total_attachments}\n",
            "Текст вопроса:",
            f"{question_info.question_dto.message}",
        ]

    async def get_answer_info_message(
        self, answer_info: AnswerInfo
    ) -> list[str]:
        is_useful = answer_info.answer_dto.is_useful

        estimation_description = (
            "Ответ не получил оценки"
            if is_useful is None
            else f"{'Ответ был оценён как полезный' if is_useful else 'Ответ был оценён как бесполезный'}"  # noqa: E501
        )

        answer_date = get_eu_formated_datetime(
            answer_info.answer_dto.date, self.tz  # type: ignore
        )

        return [
            f"ID: `{answer_info.answer_dto.tg_message_id}`\n"
            f"ID вопроса: "
            f"`{answer_info.answered_quetsion_dto.tg_message_id}`\n"
            f"ID Автора ответа: "
            f"`{answer_info.support_user_answered_dto.tg_bot_id}`\n"
            f"Дата ответа: {answer_date}\n"
            f"{estimation_description}\n"
            f"Всего приложений: {answer_info.statistics.total_attachments}",
            "Текст ответа:",
            f"{answer_info.answer_dto.message}",
        ]

    # OBJECTS LIST INFO MESSAGES

    async def get_roles_list_message(
        self,
        roles_list: list[RoleDTO],
    ) -> list[str]:
        if not roles_list:
            return ["Ни одной роли пока не было добавлено"]

        message = ""
        for role in roles_list:
            created_date = get_eu_formated_datetime(
                role.created_date, self.tz  # type: ignore
            )

            message += (
                f"Имя: `{role.name}`; "
                f"ID: `{role.id}`; "
                f"Дата создания: {created_date}\n"
            )

        return ["Список ролей:", message]

    async def get_questions_list_message(
        self,
        questions_list: list[QuestionDTO],
    ) -> list[str]:
        message = ""
        for question in questions_list:
            # FIXME: Think about how that can be fixed
            message += (
                f"ID вопроса: `{question.tg_message_id};` "
                # TODO: Come up with a solution for this thing.
                # NOTE: Might be solved by changing users' UUIDs ids
                # to intger ids which Telegram provides
                # f"ID пользователя: `{question.regular_user.tg_bot_user_id}`; " # noqa: E501
                f"Текст вопроса: {question.message[0:100]}...\n"
            )

        return ["Список вопросов:", message]

    async def get_answers_list_message(
        self,
        answers_list: list[AnswerDTO],
    ) -> list[str]:
        message = "Список ответов:"
        for answer in answers_list:
            answer_text = (
                f"{answer.message[0:100]}..."
                if len(answer.message) > 100
                else answer.message[0:100]
            )

            message += (
                f"\nID ответа: {answer.tg_message_id}; "
                # TODO: Come up with a solution for this thing.
                # NOTE: Might be solved by changing users' UUIDs ids
                # to intger ids which Telegram provides
                # f"ID отвечавшего пользователя: "
                # f"{answer.support_user.tg_bot_user_id}\n"
                f"Текст ответа: {answer_text}"
            )

        return [message]

    async def get_support_users_list_message(
        self,
        support_users_list: list[SupportUserDTO],
    ) -> list[str]:
        message = "Пользователи поддержки:"

        for support_user in support_users_list:
            role_desctiption = "Роль: " + (
                (support_user.role and f"ID Роли: `{support_user.role.id}`")
                or (
                    support_user.is_owner
                    and "пользователь является владельцем"
                )
                or "роль не назначена"
            )

            join_date = get_eu_formated_datetime(
                support_user.join_date, self.tz  # type: ignore
            )

            message += (
                f"\nИмя: `{support_user.descriptive_name}`; "
                f"ID: `{support_user.tg_bot_id}`; "
                f"{role_desctiption}; "
                f"Дата назначения: {join_date}"
            )

        return [message]

    # BINDING MESSAGES

    async def get_question_already_bound_message(
        self, question_id: int, support_user_id: int
    ) -> list[str]:
        return [
            f"Вопрос с ID: `{question_id}` уже привязан к "
            f"другому пользователю с ID: `{support_user_id}`"
        ]

    async def get_successful_unbinding_message(self) -> list[str]:
        return ["Теперь Вы не отвечаете ни на один вопрос"]

    async def get_successful_binding_message(
        self, question: QuestionDTO
    ) -> list[str]:
        return [
            f"Теперь Вы отвечаете на вопрос с ID: {question.tg_message_id}"
        ]

    async def get_no_bound_question_message(self) -> list[str]:
        return ["Вы сейчас не отвечаете ни на один вопрос"]

    async def get_no_quetstions_to_answer_left_message(self) -> list[str]:
        return [
            "Больше неотвеченных и непрекреплённых "
            "ни к кому вопросов не осталось"
        ]

    # ESTIMATION MESSAGES

    async def get_answer_already_estimated_message(
        self, answer: AnswerDTO
    ) -> list[str]:
        return ["Ответ уже оценён"]

    async def get_answer_estimated_as_useful_message(
        self, answer: AnswerDTO
    ) -> list[str]:
        return ["Ответ был оценён как полезный"]

    async def get_answer_estimated_as_unuseful_message(
        self, answer: AnswerDTO
    ) -> list[str]:
        return ["Ответ был оценён как бесполезный"]

    # INITIALIZING MESSAGES

    async def get_already_inited_owner_message(
        self, tg_user: TgUser
    ) -> list[str]:
        return ["Владелец бота уже инициализирован"]

    async def get_successful_owner_init_message(
        self, tg_user: TgUser, support_user: SupportUserDTO
    ) -> list[str]:
        return ["Поздравляем, Вы теперь владелец данного бота!"]

    async def get_incorrect_owner_password_message(self) -> list[str]:
        return ["Пароль неверен, попробуйте снова"]

    # SUPPORT TgUser ACTIVATION MESSAGES

    async def get_support_user_deactivation_message(
        self,
        support_user: SupportUserDTO,
    ) -> list[str]:
        support_user_id = support_user.tg_bot_id

        return [f"Пользователь с ID: {support_user_id} успешно деактивирован"]

    async def get_support_user_activation_message(
        self,
        support_user: SupportUserDTO,
    ) -> list[str]:
        support_user_id = support_user.tg_bot_id

        return [f"Пользователь с ID: {support_user_id} успешно активирован"]

    # ATTACHMENTS MESSAGES

    async def get_no_last_asked_question_message(
        self, regular_user: RegularUserDTO
    ) -> list[str]:
        return ["У Вас нет последнего заданного вопроса или он был удалён"]

    async def get_no_last_answer_message(
        self, support_user: SupportUserDTO
    ) -> list[str]:
        return ["Вы пока ни на что не отвечали или Ваш ответ был удалён"]

    async def get_question_attachment_addition_message(
        self, question_attachment: AttachmentDTO
    ) -> list[str]:
        return ["Приложение к последнему вопросу успешно добавлено"]

    async def get_answer_attachment_addition_message(
        self, answer_attachment: AttachmentDTO
    ) -> list[str]:
        return ["Приложение к последнему ответу успешно добавлено"]

    # OTHER MESSAGES

    async def get_global_statistics_message(
        self, global_statistics: GlobalStatistics
    ) -> list[str]:
        return [
            "Общая статистика:\n"
            f"Всего обычных пользователей: "
            f"*{global_statistics.total_regular_users}*\n"
            f"Всего пользователей поддержки: "
            f"*{global_statistics.total_support_users}*\n"
            f"Всего ролей: "
            f"*{global_statistics.total_roles}*\n"
            f"Всего вопросов: "
            f"*{global_statistics.total_questions}*\n"
            f"Всего отвеченных вопросов: "
            f"*{global_statistics.total_answered_questions}*\n"
            f"Всего неотвеченных вопросов: "
            f"*{global_statistics.total_unanswered_questions}*\n"
            f"Всего приложений к вопросам: "
            f"*{global_statistics.total_question_attachments}*\n"
            f"Всего ответов: "
            f"*{global_statistics.total_answers}*\n"
            f"Всего полезных ответов: "
            f"*{global_statistics.total_useful_answers}*\n"
            f"Всего бесполезных ответов: "
            f"*{global_statistics.total_unuseful_answers}*\n"
            f"Всего неоценённых ответов: "
            f"*{global_statistics.total_unestimated_answers}*\n"
            f"Всего приложений к ответам: "
            f"*{global_statistics.total_answer_attachments}*\n"
        ]

    async def get_id_message(self, id: int) -> list[str]:
        return ["Ваш ID пользователя для этого бота:", str(id)]

    async def get_permission_denied_message(self, TgUser: TgUser) -> list[str]:
        return ["Отказано в доступе"]

    async def get_answer_for_regular_user_message(
        self,
        question_dto: QuestionDTO,
        answer_dto: AnswerDTO,
        include_question: bool = False,
    ) -> list[str]:
        if include_question:
            return [
                "На Ваш вопрос был дан ответ:",
                "Вопрос:",
                f"{question_dto.message}",
                "Ответ:",
                f"{answer_dto.message}",
            ]

        return [
            "На Ваш вопрос был дан ответ:",
            f"{answer_dto.message}",
        ]

    async def get_no_question_attachments_message(
        self, question: QuestionDTO
    ) -> list[str]:
        return ["К этому вопросу нет приложений"]

    async def get_unsupported_message_type_message(self) -> list[str]:
        return [
            "Мы просим прощения, но данный формат сообщений "
            "на данный момент не поддерживается"
        ]

    async def get_unknown_command_message(self) -> list[str]:
        return [
            "Это несуществующая команда. Если возникли трудности, "
            "введите команду /help"
        ]

    async def get_regular_user_not_authorized_message(self) -> list[str]:
        return ["Введите команду /start, чтобы продолжить пользоваться ботом"]
