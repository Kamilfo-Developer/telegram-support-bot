import json
import traceback
from time import sleep
from typing import NoReturn

from telegram import Update, User
from telegram.error import NetworkError
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CallbackContext,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
)
from telegram.ext.filters import (
    ALL,
    AUDIO,
    PHOTO,
    VIDEO,
    VOICE,
    Command,
    Document,
    Text,
)

from app.bot.bot import Bot
from app.bot.bot_handlers import BotHandlers
from app.bot.bot_messages import MessageToSend
from app.bot.dtos import TgFile, TgMessage, TgUser
from app.bot.states import States
from app.config.app_config import AppSettings
from app.errors import NoBotTokenProvided
from app.loggers.logger import AppLogger
from app.shared.value_objects import (
    TgCaption,
    TgFileIdType,
    TgMessageIdType,
    TgMessageText,
    TgUserId,
)
from app.utils import get_file_type_and_file_id


class PTBBot(Bot):
    def __init__(
        self,
        bot_handlers: BotHandlers,
        app_settings: AppSettings,
        app_logger: AppLogger,
    ) -> None:
        self.__bot_handlers = bot_handlers
        self.__app_settings = app_settings
        self.__application = self.__initialize()
        self.__logger = app_logger

    async def __send_messages(
        self, messages: list[MessageToSend], update: Update
    ) -> None:
        for message in messages:
            await message.send(update)

    def __get_tg_user_from_ptb_user(self, user: User) -> TgUser:
        return TgUser(
            TgUserId(user.id),
            user.first_name,
            user.last_name or "",
            user.language_code or self.__app_settings.DEFAULT_LANGUAGE_CODE,
        )

    def __get_tg_file(self, update: Update) -> TgFile | None:
        assert update.message

        file_type_and_id = get_file_type_and_file_id(update.message)

        if not all(file_type_and_id):
            return None

        tg_file = (
            TgFile(
                file_id=TgFileIdType(file_type_and_id[1]),
                file_type=file_type_and_id[0],  # type: ignore
                caption=TgCaption(update.message.caption)
                if update.message.caption
                else None,
            )
            if all(file_type_and_id)
            else None
        )

        return tg_file

    async def __handle_start(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
    ) -> None:
        """
        Handles /start command
        """
        user = update.effective_user

        assert user

        messages = await self.__bot_handlers.handle_start_command(
            self.__get_tg_user_from_ptb_user(user),
            update.get_bot().name,
        )

        await self.__send_messages(messages, update)

    async def __handle_init_owner(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """
        Handles /initowner command
        """
        user = update.effective_user

        assert user

        messages = await self.__bot_handlers.handle_init_owner(
            self.__get_tg_user_from_ptb_user(user),
            context.args or [],
        )

        await self.__send_messages(messages, update)

    async def __handle_help_command(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        user = update.effective_user

        assert user

        messages = await self.__bot_handlers.handle_help_command(
            self.__get_tg_user_from_ptb_user(user)
        )

        await self.__send_messages(messages, update)

    async def __handle_get_id(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """
        Handles /getid command
        """
        user = update.effective_user

        assert user

        messages = await self.__bot_handlers.handle_get_id(
            self.__get_tg_user_from_ptb_user(user)
        )

        await self.__send_messages(messages, update)

    # REGULAR USERS

    async def __handle_get_regular_user(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        user = update.effective_user

        assert user

        messages = await self.__bot_handlers.handle_get_regular_user_info(
            self.__get_tg_user_from_ptb_user(user), context.args or []
        )

        await self.__send_messages(messages, update)

    # STATISTICS

    async def __handle_global_statistics(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """
        Handles /globalstats command
        """
        user = update.effective_user

        assert user

        messages = await self.__bot_handlers.handle_get_global_statistics(
            self.__get_tg_user_from_ptb_user(user)
        )

        await self.__send_messages(messages, update)

    # ROLES

    async def __handle_add_role(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        user = update.effective_user

        assert user

        messages = await self.__bot_handlers.handle_add_role(
            self.__get_tg_user_from_ptb_user(user), context.args or []
        )

        await self.__send_messages(messages, update)

    async def __handle_get_role(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        user = update.effective_user

        assert user

        messages = await self.__bot_handlers.handle_get_role_info(
            self.__get_tg_user_from_ptb_user(user), context.args or []
        )

        await self.__send_messages(messages, update)

    async def __handle_get_all_roles(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """
        Handles /allroles command
        """
        user = update.effective_user

        assert user

        messages = await self.__bot_handlers.handle_get_all_roles(
            self.__get_tg_user_from_ptb_user(user), context.args or []
        )

        await self.__send_messages(messages, update)

    async def __handle_delete_role(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        user = update.effective_user

        assert user

        messages = await self.__bot_handlers.handle_delete_role(
            self.__get_tg_user_from_ptb_user(user), context.args or []
        )

        await self.__send_messages(messages, update)

    # SUPPORT USERS

    async def __handle_add_support_user(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        user = update.effective_user

        assert user

        messages = await self.__bot_handlers.handle_add_support_user(
            self.__get_tg_user_from_ptb_user(user), context.args or []
        )

        await self.__send_messages(messages, update)

    async def __handle_activate_support_user(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        user = update.effective_user

        assert user

        messages = await self.__bot_handlers.handle_activate_support_user(
            self.__get_tg_user_from_ptb_user(user), context.args or []
        )

        await self.__send_messages(messages, update)

    async def __handle_deactivate_support_user(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        user = update.effective_user

        assert user

        messages = await self.__bot_handlers.handle_deactivate_support_user(
            self.__get_tg_user_from_ptb_user(user), context.args or []
        )

        await self.__send_messages(messages, update)

    async def __handle_get_support_user(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """
        Handles /getsupuser command
        """
        user = update.effective_user

        assert user

        messages = await self.__bot_handlers.handle_get_support_user_info(
            self.__get_tg_user_from_ptb_user(user), context.args or []
        )

        await self.__send_messages(messages, update)

    async def __handle_get_all_suppurt_users(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """
        Handles /allsupusers command
        """
        user = update.effective_user

        assert user

        messages = await self.__bot_handlers.handle_get_all_suppurt_users(
            self.__get_tg_user_from_ptb_user(user)
        )

        await self.__send_messages(messages, update)

    # QUESTIONS

    async def __handle_get_question(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """
        Handles /question command
        """
        user = update.effective_user

        assert user

        messages = await self.__bot_handlers.handle_get_question(
            self.__get_tg_user_from_ptb_user(user), context.args or []
        )

        await self.__send_messages(messages, update)

    async def __handle_get_question_answers(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        user = update.effective_user

        assert user

        messages = await self.__bot_handlers.handle_get_question_answers(
            self.__get_tg_user_from_ptb_user(user), context.args or []
        )

        await self.__send_messages(messages, update)

    async def __handle_bind_question(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """
        Handles /bind command
        """
        user = update.effective_user

        assert user

        messages = await self.__bot_handlers.handle_bind_question(
            self.__get_tg_user_from_ptb_user(user), context.args or []
        )

        await self.__send_messages(messages, update)

    async def __handle_unbind_question(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """
        Handles /unbind command
        """
        user = update.effective_user

        assert user

        messages = await self.__bot_handlers.handle_unbind_question(
            self.__get_tg_user_from_ptb_user(user), context.args or []
        )

        await self.__send_messages(messages, update)

    # ANSWERS

    async def __handle_get_answer(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """
        Handles /answer [answerId] command
        """
        user = update.effective_user

        assert user

        messages = await self.__bot_handlers.handle_get_answer_info(
            self.__get_tg_user_from_ptb_user(user), context.args or []
        )

        await self.__send_messages(messages, update)

    # MESSAGE HANDLERS

    async def __handle_message(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """
        Handles all text messages
        """
        user = update.effective_user

        assert user

        assert (
            update.message
            and update.message.text
            and update.message.message_id
        )

        messages = await self.__bot_handlers.handle_message(
            self.__get_tg_user_from_ptb_user(user),
            TgMessage(
                TgMessageIdType(update.message.message_id),
                TgMessageText(update.message.text),
            ),
            context.args or [],
        )

        await self.__send_messages(messages, update)

    async def __handle_file(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        user = update.effective_user

        assert user

        messages = await self.__bot_handlers.handle_file(
            self.__get_tg_user_from_ptb_user(user), self.__get_tg_file(update)
        )

        await self.__send_messages(messages, update)

    async def __handle_unsuppported_message_type(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        user = update.effective_user

        assert user

        messages = await self.__bot_handlers.handle_unsuppported_message_type(
            self.__get_tg_user_from_ptb_user(user)
        )

        await self.__send_messages(messages, update)

    async def __handle_unknown_command(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        user = update.effective_user

        assert user

        messages = await self.__bot_handlers.handle_unknown_command(
            self.__get_tg_user_from_ptb_user(user)
        )

        await self.__send_messages(messages, update)

    # BUTTONS HANDLERS

    async def __handle_bind_question_button(
        self, update: Update, context: CallbackContext
    ) -> None:
        user = update.effective_user

        assert user and update.callback_query

        messages = await self.__bot_handlers.handle_bind_question_button(
            self.__get_tg_user_from_ptb_user(user),
            str(update.callback_query.data),
        )

        await self.__send_messages(messages, update)

        await update.callback_query.answer()

    async def __handle_unbind_question_button(
        self, update: Update, context: CallbackContext
    ) -> None:
        user = update.effective_user

        assert user and update.callback_query

        messages = await self.__bot_handlers.handle_unbind_question_button(
            self.__get_tg_user_from_ptb_user(user),
            str(update.callback_query.data),
        )

        await self.__send_messages(messages, update)

        await update.callback_query.answer()

    async def __handle_estimate_question_as_useful_button(
        self, update: Update, context: CallbackContext
    ) -> None:
        user = update.effective_user

        assert user and update.callback_query

        messages = await self.__bot_handlers.handle_estimate_question_as_useful_button(  # noqa: E501
            self.__get_tg_user_from_ptb_user(user),
            str(update.callback_query.data),
        )

        await self.__send_messages(messages, update)

        await update.callback_query.answer()

    async def __handle_estimate_question_as_unuseful_button(
        self, update: Update, context: CallbackContext
    ) -> None:
        user = update.effective_user

        assert user and update.callback_query

        messages = await self.__bot_handlers.handle_estimate_question_as_unuseful_button(  # noqa: E501
            self.__get_tg_user_from_ptb_user(user),
            str(update.callback_query.data),
        )

        await self.__send_messages(messages, update)

        await update.callback_query.answer()

    async def __handle_show_attachments_button(
        self, update: Update, context: CallbackContext
    ) -> None:
        user = update.effective_user

        assert user and update.callback_query

        messages = await self.__bot_handlers.handle_show_question_attachments_button(  # noqa: E501
            self.__get_tg_user_from_ptb_user(user),
            str(update.callback_query.data),
        )

        await self.__send_messages(messages, update)

        await update.callback_query.answer()

    async def __handle_error(
        self, update: object, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        await self.__logger.error(str(context.error))

        traceback.print_exc()

    def __initialize(self) -> Application:
        if not self.__app_settings.BOT_TOKEN:
            raise NoBotTokenProvided(
                "You must provide a Telegram bot token. "
                "You can get a token using this bot: https://t.me/botfather"
            )

        app = ApplicationBuilder().token(self.__app_settings.BOT_TOKEN).build()

        app.add_handler(CommandHandler("start", self.__handle_start))

        app.add_handler(CommandHandler("help", self.__handle_help_command))

        app.add_handler(CommandHandler("getid", self.__handle_get_id))

        app.add_handler(CommandHandler("initowner", self.__handle_init_owner))

        app.add_handler(
            CommandHandler("supuser", self.__handle_get_support_user)
        )

        app.add_handler(
            CommandHandler("supusers", self.__handle_get_all_suppurt_users)
        )

        app.add_handler(CommandHandler("question", self.__handle_get_question))

        app.add_handler(CommandHandler("bind", self.__handle_bind_question))

        app.add_handler(
            CommandHandler("unbind", self.__handle_unbind_question)
        )

        app.add_handler(
            CommandHandler("addsupuser", self.__handle_add_support_user)
        )

        app.add_handler(CommandHandler("answer", self.__handle_get_answer))

        app.add_handler(
            CommandHandler("answers", self.__handle_get_question_answers)
        )

        app.add_handler(CommandHandler("addrole", self.__handle_add_role))

        app.add_handler(CommandHandler("role", self.__handle_get_role))

        app.add_handler(CommandHandler("delrole", self.__handle_delete_role))

        app.add_handler(CommandHandler("roles", self.__handle_get_all_roles))

        app.add_handler(
            CommandHandler(
                "activatesupuser", self.__handle_activate_support_user
            )
        )

        app.add_handler(
            CommandHandler(
                "deactivatesupuser",
                self.__handle_deactivate_support_user,
            )
        )

        app.add_handler(
            CommandHandler("reguser", self.__handle_get_regular_user)
        )

        app.add_handler(
            CommandHandler("globalstats", self.__handle_global_statistics)
        )

        app.add_handler(
            CallbackQueryHandler(
                self.__handle_bind_question_button,
                lambda x: (
                    json.loads(x)["action"] == States.BIND_ACTION  # type: ignore # noqa: E501
                ),
            )
        )

        app.add_handler(
            CallbackQueryHandler(
                self.__handle_unbind_question_button,
                lambda x: (
                    json.loads(x)["action"] == States.UNBIND_ACTION  # type: ignore # noqa: E501
                ),
            )
        )

        app.add_handler(
            CallbackQueryHandler(
                self.__handle_estimate_question_as_useful_button,
                lambda x: (
                    json.loads(x)["action"]  # type: ignore
                    == States.ESTIMATE_AS_USEFUL_ACTION
                ),
            )
        )

        app.add_handler(
            CallbackQueryHandler(
                self.__handle_estimate_question_as_unuseful_button,
                lambda x: (
                    json.loads(x)["action"]  # type: ignore
                    == States.ESTIMATE_AS_UNUSEFUL_ACTION
                ),
            )
        )

        app.add_handler(
            CallbackQueryHandler(
                self.__handle_show_attachments_button,
                lambda x: (
                    json.loads(x)["action"]  # type: ignore
                    == States.SHOW_ATTACHMENTS_ACTION
                ),
            )
        )

        app.add_handler(
            MessageHandler(Command(False), self.__handle_unknown_command)
        )

        app.add_handler(
            MessageHandler(
                PHOTO | VIDEO | AUDIO | VOICE | Document.ALL,
                self.__handle_file,
            )
        )

        app.add_handler(MessageHandler(Text(), self.__handle_message))

        app.add_handler(
            MessageHandler(ALL, self.__handle_unsuppported_message_type)
        )

        app.add_handler(CommandHandler("roles", self.__handle_get_all_roles))

        app.add_error_handler(self.__handle_error)

        return app

    # Why `type: ignore`? Because the developer of PTB
    # typed the `start_polling` method of
    # the Updater class as None for some reason

    async def run(self) -> NoReturn:  # type: ignore
        RETRY_TIME_SECONDS = 3

        is_running = False

        while not is_running:
            try:
                await self.__application.initialize()
                await self.__application.start()
                assert self.__application.updater
                await self.__application.updater.start_polling()

                is_running = True

            except NetworkError:
                await self.__logger.critical(
                    f"Cannot connect to Telegram Bot API. "
                    f"The bot will retry in {RETRY_TIME_SECONDS} seconds."
                )

                sleep(RETRY_TIME_SECONDS)
