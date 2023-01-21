from telegram import User
from bot.entities.regular_user import RegularUser
from bot.entities.support_user import SupportUser
from bot.entities.question import Question
from bot.entities.answer import Answer
from bot.localization.messages import Messages
from bot.entities.role import Role


class RUMessages(Messages):
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

    async def get_successful_role_addition_message(
        self,
        role: Role,
        *args,
        **kwargs,
    ) -> list[str]:
        return [
            f"Роль с названием ```{role.name}``` успешно добавлена!\n\nЕё ID: ```{role.id}```\nЕё права:\nМожет отвечать на вопросы: {'да' if role.can_answer_questions else 'нет'}\nМожет управлять пользователями поддержки: {'да' if role.can_manage_support_users else 'нет'}"
        ]

    async def get_successful_support_user_addition_message(
        self,
        support_user: SupportUser,
        role: Role,
        *args,
        **kwargs,
    ) -> list[str]:

        return [
            f"Пользователь поддержки с именем ```{support_user.descriptive_name}```, с ролью {role.name} успешно добавлен!\nЕго ID: ```{support_user.tg_bot_user_id}```"
        ]

    async def get_not_inited_owner_message(
        self,
        telegram_user: User,
        *args,
        **kwargs,
    ) -> list[str]:
        return [
            "Вы являетесь владельцем бота, однако Вы не завершили настройку бота. Для этого введите команду /initowner. Если возникли трудности, введите команду /help.",
        ]

    async def get_id_message(self, id: int, *args, **kwargs) -> list[str]:
        return ["Ваш id пользователя для этого бота:", str(id)]

    async def get_support_user_info_message(
        self,
        support_user: SupportUser,
        role: Role | None = None,
        *args,
        **kwargs,
    ) -> list[str]:
        role_desctiption = "Роль: " + (
            role
            and f"{role.name} (ID Роли: ```{role.id}```)"
            or (support_user.is_owner and "пользователь является владельцем")
            or "роль не назначена"
        )

        return [
            f"Имя: ```{support_user.descriptive_name}```\nID: ```{support_user.tg_bot_user_id}```\n{role_desctiption}\nДата назначения: {support_user.join_date}"
        ]

    async def get_all_support_users_list_message(
        self, support_users: list[SupportUser], *args, **kwargs
    ) -> list[str]:
        message = "Пользователи поддержки:\n"
        for user in support_users:
            message += f"Имя: {user.descriptive_name}\nID: ```{user.tg_bot_user_id}```\nID роли: {f'```{user.role_id}```' or 'нет роли'}\nДата назначения: {user.join_date}"

        return [message]

    async def get_incorrect_arguments_passed_message(
        self, *args, **kwargs
    ) -> list[str]:
        return ["Аргумент(ы) указан(ы) неверно, попробуйте снова"]

    async def get_question_info_message(
        self,
        question: Question,
        regular_user_asked: RegularUser,
        *args,
        **kwargs,
    ) -> list[str]:
        return [
            f"ID: {question.tg_message_id}\nID задавшего вопрос пользователя: {regular_user_asked.tg_bot_user_id}\nВопрос был задан: {question.date}",
            f"Текст вопроса:\n{question.message}",
        ]

    async def get_permission_denied_message(
        self, user: User, *args, **kwargs
    ) -> list[str]:
        return ["Отказано в доступе"]

    async def get_no_binded_question_message(
        self, *args, **kwargs
    ) -> list[str]:
        return ["Вы сейчас не отвечаете ни на один вопрос"]

    async def get_answer_info_message(
        self,
        answer: Answer,
        support_user: SupportUser,
        question: Question,
        *args,
        **kwargs,
    ) -> list[str]:
        return [
            f"ID: ```{answer.tg_message_id}```\nID вопроса: ```{question.tg_message_id}```\nАвтор ответа: {support_user.descriptive_name} (ID пользователя: ```{support_user.tg_bot_user_id}```)\nДата ответа: {answer.date}",
            f"Текст ответа:\n{answer.message}",
        ]

    async def get_answer_for_regular_user_message(
        self,
        answer: Answer,
        question: Question,
        include_question: bool = False,
        *args,
        **kwargs,
    ) -> list[str]:
        if include_question:
            return [
                f"На Ваш вопрос от {question.date} был дан ответ: ",
                f"Вопрос:\n\n{question.message}",
                f"Ответ:\n\n{answer.message}",
            ]

        return [
            f"На Ваш вопрос от {question.date} был дан ответ: ",
            f"Ответ:\n\n{answer.message}",
        ]

    async def get_already_inited_owner_message(
        self, user: User, *args, **kwargs
    ) -> list[str]:
        return ["Владелец бота уже инициализирован"]

    async def get_role_list_message(
        self,
        roles_list: list[Role],
        *args,
        **kwargs,
    ) -> list[str]:
        message = "Список ролей:\n"
        for role in roles_list:
            message += f"Имя: {role.name}\nID: ```{role.id}```"

        return [message]

    async def get_questions_list_message(
        self,
        questions_list: list[Question],
        *args,
        **kwargs,
    ) -> list[str]:
        message = "Список вопросов:\n"
        for question in questions_list:
            message += f"ID вопроса: {question.tg_message_id}; Текст вопроса: {question.message[0:100]}..."

        return [message]

    async def get_answers_list_message(
        self,
        answers_list: list[Answer],
        *args,
        **kwargs,
    ) -> list[str]:
        message = "Список вопросов:\n"
        for answer in answers_list:
            message += f"ID ответа: {answer.tg_message_id}; Текст ответа: {answer.message[0:100]}..."

        return [message]

    async def get_successful_owner_init_message(
        self, user: User, support_user: SupportUser, *args, **kwargs
    ) -> list[str]:
        return ["Поздравляем, Вы теперь владелец данного бота!"]

    async def get_successful_unbinding_message(
        self, *args, **kwargs
    ) -> list[str]:
        return ["Теперь Вы не отвечаете ни на один вопрос"]

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

    async def get_no_object_with_this_id_message(
        self, id: str, *args, **kwargs
    ) -> list[str]:
        return [f"Нет объекта с таким ID: {id}"]

    async def get_role_name_duplicate_message(
        self,
        *args,
        **kwargs,
    ) -> list[str]:
        return [f"Роль с таким именем уже существует"]

    async def get_no_unbinded_quetstions_left_message(
        self, *args, **kwargs
    ) -> list[str]:
        return [
            "Больше неотвеченных и непрекреплённых ни к кому вопросов не осталось"
        ]

    async def get_incorrect_num_of_arguments_message(
        self, arguments_list: list[str], *args, **kwargs
    ) -> list[str]:
        return [
            "Неправильные аргументы для данной команды. Необходимые аргументы: "
            + ", ".join(
                arguments_list,
            ),
        ]

    async def get_regular_user_help_message(
        self, user: User, *args, **kwargs
    ) -> list[str]:
        return ["Помощь ты сегодня не получишь, уважаемый пользователь"]

    async def get_support_user_help_message(
        self, user: User, user_entity: SupportUser, *args, **kwargs
    ) -> list[str]:
        return [
            "Помощь ты сегодня не получишь, уважаемый пользователь, но только поддержки"
        ]

    async def get_role_info_message(
        self,
        role: Role,
        *args,
        **kwargs,
    ) -> list[str]:
        return [
            f"ID роли: ```{role.id}``` Имя роли: ```{role.name}```\n\nЕё права:\nМожет отвечать на вопросы: {'да' if role.can_answer_questions else 'нет'}\nМожет управлять пользователями поддержки: {'да' if role.can_manage_support_users else 'нет'}"
        ]

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
