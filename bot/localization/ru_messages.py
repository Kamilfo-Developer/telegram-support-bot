from telegram import User
from bot.entities.regular_user import RegularUser
from bot.entities.support_user import SupportUser
from bot.entities.question import Question
from bot.entities.answer import Answer
from bot.localization.messages import Messages
from bot.entities.role import Role


class RUMessages(Messages):
    user_id_argument_name = "ID пользователя"

    async def get_start_reg_user_message(
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

    async def get_start_sup_user_message(
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
            message += f"Имя: {user.descriptive_name}\nID: ```{user.id}```\nID роли: {f'```{user.role_id}```' or 'нет роли'}\nДата назначения: {user.join_date}"

        return [message]

    async def get_incorrect_id_message(self, *args, **kwargs) -> list[str]:
        return ["ID указан неверно, попробуйте снова"]

    async def get_question_info_message(
        self, question: Question, *args, **kwargs
    ) -> list[str]:
        return [
            f"ID: {question.id}\nID задавшего вопрос пользователя: {question.regular_user_id}\nВопрос был задан: {question.date}",
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
        *args,
        **kwargs,
    ) -> list[str]:
        return [
            f"ID: ```{answer.id}```\nID вопроса: ```{answer.question_id}```\nАвтор ответа: {support_user.descriptive_name} (ID пользователя: ```{support_user.id}```)\nДата ответа: {answer.date}",
            f"Текст ответа:\n{answer.message}",
        ]

    async def get_answer_for_regular_user_message(
        self, answer: Answer, question: Question, *args, **kwargs
    ) -> list[str]:
        return [
            f"На Ваш вопрос от {question.date} был дан ответ: ",
            f"{answer.message}",
        ]

    async def get_already_inited_owner_message(
        self, user: User, *args, **kwargs
    ) -> list[str]:
        return ["Владелец бота уже инициализирован"]

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

    async def get_no_object_with_this_id_message(
        self, *args, **kwargs
    ) -> list[str]:
        return ["Нет объекта с таким ID"]

    async def get_no_unbinded_quetstions_left_message(
        self, *args, **kwargs
    ) -> list[str]:
        return [
            "Больше неотвеченных и непрекреплённых ни к кому вопросов не осталось"
        ]

    async def get_not_enough_arguments_message(
        self, arguments_list: list[str], *args, **kwargs
    ) -> list[str]:
        return [
            "".join(
                [
                    "Недостаточно аргументов для данной команды. Необходимые аргументы: ",
                    *arguments_list,
                ],
            ),
        ]
