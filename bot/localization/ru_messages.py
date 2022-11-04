from telegram import User
from bot.entities.regular_user import RegularUser
from bot.entities.support_user import SupportUser
from bot.localization.messages import Messages


class RUMessages(Messages):
    async def get_start_reg_user_message(
        self, telegram_user: User, user_entity: RegularUser, *args, **kwargs
    ) -> list[str]:
        bot = telegram_user.get_bot()
        return [
            f"Здравствуйте, {telegram_user.first_name}. "
            + f"Вас приветствует {bot.name}.\n"
            + "Вы можете написать сюда сообщение и в скором времени "
            + "Вам придёт ответ от одного из наших сотрудников поддержки.",
        ]

    async def get_start_sup_user_message(
        self, telegram_user: User, user_entity: SupportUser, *args, **kwargs
    ) -> list[str]:
        bot = telegram_user.get_bot()
        return [
            f"Здравствуйте, {telegram_user.first_name}. "
            + f"Вас приветствует {bot.name}.\n"
            + "Вы являетесь пользователь поддержки."
            + "Если возникли трудности, введите команду /help."
        ]

    async def get_start_owner_message(
        self, telegram_user: User, user_entity: SupportUser, *args, **kwargs
    ) -> list[str]:
        bot = telegram_user.get_bot()
        return [
            f"Здравствуйте, {telegram_user.first_name}. "
            + f"Вас приветствует {bot.name}.\n"
            + "Вы являетесь владельцем бота. "
            + "Если возникли трудности, введите команду /help.",
        ]

    async def get_get_id_message(self, id: int, *args, **kwargs) -> list[str]:
        return ["Ваш id пользователя для этого бота:", str(id)]
