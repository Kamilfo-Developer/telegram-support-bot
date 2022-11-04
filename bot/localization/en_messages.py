from telegram import User
from bot.entities.regular_user import RegularUser
from bot.entities.support_user import SupportUser
from bot.localization.messages import Messages


class ENMessages(Messages):
    async def get_start_reg_user_message(
        self, telegram_user: User, user_entity: RegularUser, *args, **kwargs
    ) -> list[str]:
        bot = telegram_user.get_bot()
        return [
            f"Hello, {telegram_user.first_name}. "
            + f"My name is {bot.name}.\n"
            + "You can send your message here and it will be soon replied "
            + "by one of our support employments.",
        ]

    async def get_start_sup_user_message(
        self, telegram_user: User, user_entity: SupportUser, *args, **kwargs
    ) -> list[str]:
        bot = telegram_user.get_bot()
        return [
            f"Hello, {telegram_user.first_name}. "
            + f"My name is {bot.name}.\n"
            + "You are a support user."
            + "If you have some issues with how to use the bot, enter /help."
        ]

    async def get_start_owner_message(
        self, telegram_user: User, user_entity: SupportUser, *args, **kwargs
    ) -> list[str]:
        bot = telegram_user.get_bot()
        return [
            f"Hello, {telegram_user.first_name}. "
            + f"My name is {bot.name}.\n"
            + "You are an owner of the bot. "
            + "If you have some issues with how to use the bot, enter /help.",
        ]

    async def get_get_id_message(self, id: int, *args, **kwargs) -> list[str]:
        return ["Your user id for this bot:", str(id)]
