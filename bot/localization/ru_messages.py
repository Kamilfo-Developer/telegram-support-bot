from telegram import User
from bot.entities.regular_user import RegularUser
from bot.entities.support_user import SupportUser
from bot.entities.question import Question
from bot.entities.answer import Answer
from bot.localization.messages import Messages
from bot.entities.role import Role
from bot.services.statistics import (
    GlobalStatistics,
    RoleStatistics,
    AnswerStatistics,
    QuestionStatistics,
    SupportUserStatistics,
    RegularUserStatistics,
)


class RUMessages(Messages):
    # ARGUMENTS NAMES MESSAGE TEMPLATES
    regular_user_id_argument_name = "ID обычного пользователя"
    regular_tg_bot_user_id_argument_name = (
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

    # START MESSAGES
    async def get_start_regular_user_message(
        self,
        telegram_user: User,
        user_entity: RegularUser | None = None,
        *args,
        **kwargs,
    ) -> list[str]:
        bot = telegram_user.get_bot()
        return [
            f"Здравствуйте, {telegram_user.first_name}. Вас приветствует {bot.name}.\nВы можете написать сюда сообщение и в скором времени Вам придёт ответ от одного из наших сотрудников поддержки.",
        ]

    async def get_start_support_user_message(
        self,
        telegram_user: User,
        user_entity: SupportUser | None = None,
        *args,
        **kwargs,
    ) -> list[str]:
        bot = telegram_user.get_bot()
        return [
            f"Здравствуйте, {telegram_user.first_name}. Вас приветствует {bot.name}.\nВы являетесь пользователь поддержки. Если возникли трудности, введите команду /help."
        ]

    async def get_start_owner_message(
        self,
        telegram_user: User,
        user_entity: SupportUser,
        *args,
        **kwargs,
    ) -> list[str]:
        bot = telegram_user.get_bot()

        return [
            f"Здравствуйте, {telegram_user.first_name}. Вас приветствует {bot.name}.\nВы являетесь владельцем бота. Если возникли трудности, введите команду /help.",
        ]

    # HELP MESSAGES

    async def get_inited_owner_help_message(
        self,
        user: User,
        user_entity: SupportUser,
        *args,
        **kwargs,
    ) -> list[str]:
        return [
            "Помощь ты сегодня не получишь, ёбаный ты долбоёб инициализированный"
        ]

    async def get_not_inited_owner_help_message(
        self,
        user: User,
        *args,
        **kwargs,
    ) -> list[str]:
        return [
            "Помощь ты сегодня не получишь, ёбаный ты долбоёб неинициализированный"
        ]

    async def get_regular_user_help_message(
        self, user: User, *args, **kwargs
    ) -> list[str]:
        return ["Уважаемый пользователь, эта команда пока не реализована"]

    async def get_support_user_help_message(
        self, user: User, user_entity: SupportUser, *args, **kwargs
    ) -> list[str]:
        return [
            "Уважаемый пользователь поддержки, эта команда пока не реализована"
        ]

    # ARGUMENTS MESSAGES

    async def get_incorrect_num_of_arguments_message(
        self, arguments_list: list[str], *args, **kwargs
    ) -> list[str]:
        return [
            "Неправильные аргументы для данной команды. Необходимые аргументы: "
            + ", ".join(
                arguments_list,
            ),
        ]

    async def get_incorrect_arguments_passed_message(
        self, *args, **kwargs
    ) -> list[str]:
        return ["Аргумент(ы) указан(ы) неверно, попробуйте снова"]

    async def get_no_object_with_this_id_message(
        self, id: str, *args, **kwargs
    ) -> list[str]:
        return [f"Нет объекта с таким ID: {id}"]

    async def get_unavailable_or_deleted_object_message(
        self, *args, **kwargs
    ) -> list[str]:
        return [f"Данный объект недоступен или был удалён"]

    # ADDITION MESSAGES

    async def get_successful_role_addition_message(
        self,
        role: Role,
        *args,
        **kwargs,
    ) -> list[str]:
        return [
            f"Роль с названием `{role.name}` успешно добавлена!\n\nЕё ID: `{role.id}`\nЕё права:\nМожет отвечать на вопросы: {'да' if role.can_answer_questions else 'нет'}\nМожет управлять пользователями поддержки: {'да' if role.can_manage_support_users else 'нет'}"
        ]

    async def get_role_name_duplicate_message(
        self,
        *args,
        **kwargs,
    ) -> list[str]:
        return ["Роль с таким именем уже существует"]

    async def get_successful_support_user_addition_message(
        self,
        support_user: SupportUser,
        *args,
        **kwargs,
    ) -> list[str]:

        return [
            f"Пользователь поддержки с именем `{support_user.descriptive_name}`, с ролью `{support_user.role.name}` успешно добавлен!\nЕго ID: `{support_user.tg_bot_user_id}`"  # type: ignore
        ]

    async def get_successful_answering_message(
        self,
        question: Question,
        answer: Answer,
        *args,
        **kwargs,
    ) -> list[str]:
        return [
            f"Вопрос с ID: {question.tg_message_id} успешно отвечен. Ответ получил ID: {answer.tg_message_id}"
        ]

    async def get_successful_asking_message(
        self,
        question: Question,
        *args,
        **kwargs,
    ) -> list[str]:
        return [
            "Вопрос успешно задан. Как только сотрудник поддержки ответит на Ваш вопрос, Вам придёт сообщение в этот чат. Ответ на вопрос может занять некоторое время"
        ]

    async def get_support_user_already_exists_message(
        self, support_user: SupportUser, *args, **kwargs
    ) -> list[str]:
        return ["Пользователь с таким ID уже является пользователем поддержки"]

    # DELETING OBJECTS MESSAGES

    async def role_deleted_message(
        self,
        role: Role,
        *args,
        **kwargs,
    ) -> list[str]:
        return [f"Роль с ID: {role.id} успешно удалена"]

    # ONE OBJECT INFO MESSAGES

    async def get_role_info_message(
        self,
        role: Role,
        role_statistics: RoleStatistics,
        *args,
        **kwargs,
    ) -> list[str]:
        return [
            f"*ID роли*: `{role.id}`\n"
            + f"*Имя роли*: `{role.name}`\n\n"
            + "*Её права*:\n\n"
            + "Может отвечать на вопросы: "
            + f"{'*да*' if role.can_answer_questions else '*нет*'}\n"
            + "Может управлять пользователями поддержки: "
            + f"{'*да*' if role.can_manage_support_users else '*нет*'}\n\n"
            + "Всего пользователей с ролью: "
            + f"{role_statistics.total_users}"
        ]

    async def get_support_user_info_message(
        self,
        support_user: SupportUser,
        support_user_statistics: SupportUserStatistics,
        *args,
        **kwargs,
    ) -> list[str]:
        role_desctiption = "*Роль*: " + (
            (
                support_user.role
                and f"`{support_user.role.name}` (ID Роли: `{support_user.role.id}`)"
            )
            or (support_user.is_owner and "*пользователь является владельцем*")
            or "*роль не назначена*"
        )

        return [
            f"*ID*: `{support_user.tg_bot_user_id}`\n"
            + f"*Имя*: `{support_user.descriptive_name}`\n\n"
            + f"{role_desctiption}\n\n"
            + f"*Дата назначения*: {support_user.join_date}\n\n"
            + "*Статистика*:\n"
            + f"Всего ответов: {support_user_statistics.total_answers}\n"
            + f"Полезных ответов: {support_user_statistics.useful_answers}\n"
            + f"Бесполезных ответов: {support_user_statistics.unuseful_answers}\n"
            + f"Неоценённых ответов: {support_user_statistics.unestimated_answers}"
        ]

    async def get_regular_user_info_message(
        self,
        regular_user: RegularUser,
        regular_user_statistics: RegularUserStatistics,
        *args,
        **kwargs,
    ) -> list[str]:
        return [
            f"ID: `{regular_user.tg_bot_user_id}`\n"
            + f"Дата присоединения: {regular_user.join_date}\n"
            + f"Задано вопросов: {regular_user_statistics.asked_questions}\n"
            + f"Из них ответ получили: {regular_user_statistics.answered_questions}"
        ]

    async def get_question_info_message(
        self,
        question: Question,
        question_statistics: QuestionStatistics,
        *args,
        **kwargs,
    ) -> list[str]:
        return [
            f"ID: `{question.tg_message_id}`\n"
            + f"ID задавшего вопрос пользователя: `{question.regular_user.tg_bot_user_id}`\n"
            + f"Вопрос был задан: {question.date}"
            + f"Ответов на вопрос: {question_statistics.total_answers}"
            + f"Всего приложений: {question_statistics.total_attachments}",
            "Текст вопроса:",
            f"{question.message}",
        ]

    async def get_answer_info_message(
        self,
        answer: Answer,
        answer_statistics: AnswerStatistics,
        *args,
        **kwargs,
    ) -> list[str]:
        estimation_description = (
            "Ответ не получил оценки"
            if answer.is_useful is None
            else f"{'Ответ был оценён как полезный' if answer.is_useful else 'Ответ был оценён как бесполезный'}"
        )
        return [
            f"ID: `{answer.tg_message_id}`\n"
            + f"ID вопроса: `{answer.question.tg_message_id}`\n"
            + f"Автор ответа: {answer.support_user.descriptive_name} (ID пользователя: `{answer.support_user.tg_bot_user_id}`)\n"
            + f"Дата ответа: {answer.date}\n{estimation_description}\n"
            + f"Всего приложений: {answer_statistics.total_attachments}",
            "Текст ответа:",
            f"{answer.message}",
        ]

    # OBJECTS LIST INFO MESSAGES

    async def get_roles_list_message(
        self,
        roles_list: list[Role],
        *args,
        **kwargs,
    ) -> list[str]:
        if not roles_list:
            return ["Ни одной роли пока не было добавлено"]

        message = ""
        for role in roles_list:
            message += f"Имя: `{role.name}`; ID: `{role.id}`; Дата создания: {role.created_date}\n"

        return ["Список ролей:", message]

    async def get_questions_list_message(
        self,
        questions_list: list[Question],
        *args,
        **kwargs,
    ) -> list[str]:
        message = ""
        for question in questions_list:
            message += f"ID вопроса: {question.tg_message_id}; ID пользователя: {question.regular_user.tg_bot_user_id}; Текст вопроса: {question.message[0:100]}...\n"

        return ["Список вопросов:", message]

    async def get_answers_list_message(
        self,
        answers_list: list[Answer],
        *args,
        **kwargs,
    ) -> list[str]:
        message = "Список ответов:"
        for answer in answers_list:
            message += (
                f"\nID ответа: {answer.tg_message_id}; ID отвечавшего пользователя: {answer.support_user.tg_bot_user_id}\n"
                + f"Текст ответа: {f'{answer.message[0:100]}...' if len(answer.message) > 100 else answer.message[0:100]}"
            )

        return [message]

    async def get_support_users_list_message(
        self,
        support_users_list: list[SupportUser],
        *args,
        **kwargs,
    ) -> list[str]:
        message = "Пользователи поддержки:"

        for support_user in support_users_list:
            role_desctiption = "Роль: " + (
                (
                    support_user.role
                    and f"`{support_user.role.name}` (ID Роли: `{support_user.role.id}`)"
                )
                or (
                    support_user.is_owner
                    and "пользователь является владельцем"
                )
                or "роль не назначена"
            )

            message += f"\nИмя: `{support_user.descriptive_name}`; ID: `{support_user.tg_bot_user_id}`; {role_desctiption}; Дата назначения: {support_user.join_date}"

        return [message]

    # BINDING MESSAGES

    async def get_question_already_binded_message(
        self, question_id: int, *args, **kwargs
    ) -> list[str]:
        return [
            f"Вопрос с ID: {question_id} уже привязан к другому пользователю"
        ]

    async def get_successful_unbinding_message(
        self, *args, **kwargs
    ) -> list[str]:
        return ["Теперь Вы не отвечаете ни на один вопрос"]

    async def get_successful_binding_message(
        self, question: Question, *args, **kwargs
    ) -> list[str]:
        return [
            f"Теперь Вы отвечаете на вопрос с ID: {question.tg_message_id}"
        ]

    async def get_no_binded_question_message(
        self, *args, **kwargs
    ) -> list[str]:
        return ["Вы сейчас не отвечаете ни на один вопрос"]

    async def get_no_unbinded_quetstions_left_message(
        self, *args, **kwargs
    ) -> list[str]:
        return [
            "Больше неотвеченных и непрекреплённых ни к кому вопросов не осталось"
        ]

    # ESTIMATION MESSAGES

    async def get_answer_already_estimated_message(
        self, answer: Answer, *args, **kwargs
    ) -> list[str]:
        return ["Ответ уже оценён"]

    async def get_answer_estimated_as_useful_message(
        self, answer: Answer, *args, **kwargs
    ) -> list[str]:
        return ["Ответ был оценён как полезный"]

    async def get_answer_estimated_as_unuseful_message(
        self, answer: Answer, *args, **kwargs
    ) -> list[str]:
        return ["Ответы был оценён как бесполезный"]

    # INITIALIZING MESSAGES

    async def get_not_inited_owner_message(
        self,
        telegram_user: User,
        *args,
        **kwargs,
    ) -> list[str]:
        return [
            "Вы являетесь владельцем бота, однако Вы не завершили настройку бота."
            + "Для этого введите команду /initowner. Если возникли трудности, введите команду /help.",
        ]

    async def get_already_inited_owner_message(
        self, user: User, *args, **kwargs
    ) -> list[str]:
        return ["Владелец бота уже инициализирован"]

    async def get_successful_owner_init_message(
        self, user: User, support_user: SupportUser, *args, **kwargs
    ) -> list[str]:
        return ["Поздравляем, Вы теперь владелец данного бота!"]

    # SUPPORT USER ACTIVATION MESSAGES

    async def get_support_user_deactivation_message(
        self,
        support_user: SupportUser,
        *args,
        **kwargs,
    ) -> list[str]:
        return [
            f"Пользователь с ID: {support_user.tg_bot_user_id} успешно деактивирован"
        ]

    async def get_support_user_activation_message(
        self,
        support_user: SupportUser,
        *args,
        **kwargs,
    ) -> list[str]:
        return [
            f"Пользователь с ID: {support_user.tg_bot_user_id} успешно активирован"
        ]

    # ATTACHMENTS MESSAGES

    async def get_no_last_asked_question_message(
        self, regular_user: RegularUser
    ) -> list[str]:
        return ["У Вас нет последнего заданного вопроса или он был удалён"]

    async def get_no_last_answer_message(
        self, support_user: SupportUser
    ) -> list[str]:
        return ["Вы пока ни на что не отвечали или Ваш ответ был удалён"]

    async def get_question_attachment_addition_message(
        self, support_user: RegularUser
    ) -> list[str]:
        return ["Приложение к последнему вопросу успешно добавлено"]

    async def get_answer_attachment_addition_message(
        self, support_user: SupportUser
    ) -> list[str]:
        return ["Приложение к последнему ответу успешно добавлено"]

    # OTHER MESSAGES

    async def get_id_message(self, id: int, *args, **kwargs) -> list[str]:
        return ["Ваш id пользователя для этого бота:", str(id)]

    async def get_permission_denied_message(
        self, user: User, *args, **kwargs
    ) -> list[str]:
        return ["Отказано в доступе"]

    async def get_answer_for_regular_user_message(
        self,
        answer: Answer,
        include_question: bool = False,
        *args,
        **kwargs,
    ) -> list[str]:
        if include_question:
            return [
                f"На Ваш вопрос от {answer.question.date} был дан ответ: ",
                "Вопрос:",
                f"{answer.question.message}",
                "Ответ:",
                f"{answer.message}",
            ]

        return [
            f"На Ваш вопрос от {answer.question.date} был дан ответ: ",
            f"{answer.message}",
        ]

    async def get_no_question_attachments_message(
        self, question: Question
    ) -> list[str]:
        return ["К этому вопросу нет приложений"]

    async def get_unsupported_message_type_message(
        self, *args, **kwargs
    ) -> list[str]:
        return [
            "Мы просим прощения, но данный формат сообщений на данный момент не поддерживается"
        ]

    async def get_unknown_command_message(self, *args, **kwargs) -> list[str]:
        return [
            "Это несуществующая команда. Если возникли трудности, введите команду /help"
        ]

    async def get_regular_user_not_authorized_message(
        self, *args, **kwargs
    ) -> list[str]:
        return ["Введите команду /start, чтобы продолжить пользоваться ботом"]
