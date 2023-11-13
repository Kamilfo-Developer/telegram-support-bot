from __future__ import annotations

import json
from typing import Any


from app.bot.bot_messages import (
    FileToSend,
    MessageToSend,
    MessagesToSendFactory,
    TextToSend,
)
from app.bot.dtos import TgFile, TgMessage, TgUser
from app.bot.markup import MarkupProvider
from app.bot.states import States
from app.config.app_config import AppSettings

from app.errors import (
    IncorrectCallbackDataError,
    IncorrectPasswordError,
    NoBoundQuestion,
    NoSuchAnswer,
    NoSuchQuestion,
    NoSuchRegularUser,
    NoSuchRole,
    NoSuchSupportUser,
    OwnerAlreadyInitialized,
    PermissionDeniedError,
    RoleNameDuplicationError,
    UserIsNotAuthorizedError,
)
from app.localization.messages_content_factory import MessagesContentFactory
from app.localization.messages_content import MessagesContent
from app.loggers.logger import AppLogger
from app.regular_users.controller import RegularUserController
from app.roles.value_objects import RoleDescription, RoleName
from app.shared.dtos import AttachmentDTO
from app.shared.value_objects import (
    RoleIdType,
    TgMessageIdType,
    TgUserId,
)
from app.support_users.controller import SupportUserController
from app.support_users.dtos import QuestionInfo
from app.support_users.value_objects import DescriptiveName
from app.utils import ArgumentsValidator, TgFileType


class BotHandlers:
    def __init__(
        self,
        msgs_content_factory: MessagesContentFactory,
        support_user_controller: SupportUserController,
        regular_user_controller: RegularUserController,
        markup_provider: MarkupProvider,
        msgs_to_send_factory: MessagesToSendFactory,
        app_settings: AppSettings,
        app_logger: AppLogger,
    ) -> None:
        self.__msgs_content_factory = msgs_content_factory
        self.__support_user_controller = support_user_controller
        self.__regular_user_controller = regular_user_controller
        self.__markup_provider = markup_provider
        self.__msgs_to_send_factory = msgs_to_send_factory
        self.__regular_user_id_type = TgUserId
        self.__support_user_id_type = TgUserId
        self.__question_id_type = TgMessageIdType
        self.__answer_id_type = TgMessageIdType
        self.__role_id_type = RoleIdType
        self.__app_settings = app_settings
        self.__app_logger = app_logger

    async def handle_start_command(
        self,
        tg_user: TgUser,
        bot_name: str,
    ) -> list[MessageToSend]:
        """
        Handles /start command
        """

        await self.__app_logger.info(
            f"{tg_user.first_name} {tg_user.last_name} sent start command"
        )

        messages = self.__msgs_content_factory.get_messages_content(
            tg_user.language_code
        )

        try:
            support_user = (
                await self.__support_user_controller.authorize_support_user(
                    tg_user.tg_user_id
                )
            )

            support_user_info = (
                await self.__support_user_controller.get_own_support_user_info(
                    support_user
                )
            )

            if support_user.is_owner:
                return [
                    self.__msgs_to_send_factory.get_text_to_send(
                        await messages.get_start_owner_message(
                            tg_user, bot_name, support_user_info
                        )
                    )
                ]

            if support_user.is_active:
                return [
                    self.__msgs_to_send_factory.get_text_to_send(
                        await messages.get_start_support_user_message(
                            tg_user, bot_name, support_user_info
                        )
                    )
                ]

        except UserIsNotAuthorizedError:
            pass

        regular_user = (
            await self.__regular_user_controller.authorize_regular_user(
                tg_user.tg_user_id
            )
        )

        regular_user_info = (
            await self.__regular_user_controller.get_own_regular_user_info(
                regular_user
            )
        )

        return [
            self.__msgs_to_send_factory.get_text_to_send(
                await messages.get_start_regular_user_message(
                    tg_user, bot_name, regular_user_info
                )
            )
        ]

    async def handle_init_owner(
        self, tg_user: TgUser, inline_args: list[str]
    ) -> list[MessageToSend]:
        """
        Handles /initowner command
        """

        messages = self.__msgs_content_factory.get_messages_content(
            tg_user.language_code
        )

        if not ArgumentsValidator(inline_args).is_valid():
            return [
                self.__msgs_to_send_factory.get_text_to_send(
                    await messages.get_incorrect_arguments_passed_message(
                        [messages.owner_password_argument_name], inline_args
                    )
                )
            ]

        try:
            support_user_dto = (
                await self.__support_user_controller.initialize_owner(
                    tg_user.tg_user_id,
                    inline_args[0],
                    self.__app_settings.OWNER_PASSWORD,
                    DescriptiveName(
                        self.__app_settings.OWNER_DEFAULT_DESCRIPTIVE_NAME
                    ),
                )
            )

            return [
                self.__msgs_to_send_factory.get_text_to_send(
                    await messages.get_successful_owner_init_message(
                        tg_user, support_user_dto
                    )
                )
            ]

        except OwnerAlreadyInitialized:
            return [
                self.__msgs_to_send_factory.get_text_to_send(
                    await messages.get_already_inited_owner_message(tg_user)
                )
            ]

        except IncorrectPasswordError:
            return [
                self.__msgs_to_send_factory.get_text_to_send(
                    await messages.get_incorrect_owner_password_message()
                )
            ]

    async def handle_help_command(
        self,
        tg_user: TgUser,
    ) -> list[MessageToSend]:
        messages = self.__msgs_content_factory.get_messages_content(
            tg_user.language_code
        )

        try:
            support_user = (
                await self.__support_user_controller.authorize_support_user(
                    tg_user.tg_user_id
                )
            )

            support_user_info = (
                await self.__support_user_controller.get_own_support_user_info(
                    support_user
                )
            )

            if support_user_info.support_user_dto.is_owner:
                return [
                    self.__msgs_to_send_factory.get_text_to_send(
                        await messages.get_owner_help_message(
                            tg_user, support_user_info
                        )
                    )
                ]

            if support_user_info.support_user_dto.is_active:
                return [
                    self.__msgs_to_send_factory.get_text_to_send(
                        await messages.get_support_user_help_message(
                            tg_user, support_user_info
                        )
                    )
                ]

        except UserIsNotAuthorizedError:
            pass

        regular_user = (
            await self.__regular_user_controller.authorize_regular_user(
                tg_user.tg_user_id
            )
        )

        regular_user_info = (
            await self.__regular_user_controller.get_own_regular_user_info(
                regular_user
            )
        )

        return [
            self.__msgs_to_send_factory.get_text_to_send(
                await messages.get_regular_user_help_message(
                    tg_user, regular_user_info
                )
            )
        ]

    async def handle_get_id(
        self,
        tg_user: TgUser,
    ) -> list[MessageToSend]:
        """
        Handles /getid command
        """
        messages = self.__msgs_content_factory.get_messages_content(
            tg_user.language_code
        )

        get_id_messages = await messages.get_id_message(tg_user.tg_user_id)

        return [self.__msgs_to_send_factory.get_text_to_send(get_id_messages)]

    async def handle_get_regular_user_info(
        self, tg_user: TgUser, inline_args: list[str]
    ) -> list[MessageToSend]:
        messages = self.__msgs_content_factory.get_messages_content(
            tg_user.language_code
        )

        if not (
            ArgumentsValidator(inline_args)
            .convertable(self.__regular_user_id_type)
            .is_valid()
        ):
            return [
                self.__msgs_to_send_factory.get_text_to_send(
                    await messages.get_incorrect_arguments_passed_message(
                        [messages.regular_user_tg_bot_id_argument_name],
                        inline_args,
                    )
                )
            ]

        id = self.__regular_user_id_type(inline_args[0])

        try:
            support_user = (
                await self.__support_user_controller.authorize_support_user(
                    tg_user.tg_user_id
                )
            )

            info = await self.__support_user_controller.get_regular_user_info_by_id(  # noqa: E501
                support_user, TgUserId(id)
            )

            return [
                self.__msgs_to_send_factory.get_text_to_send(
                    await messages.get_regular_user_info_message(info)
                )
            ]

        except (UserIsNotAuthorizedError, PermissionDeniedError):
            return [
                await self.__get_permission_denied_text_message(
                    messages, tg_user
                )
            ]

        except NoSuchRegularUser:
            return [
                self.__msgs_to_send_factory.get_text_to_send(
                    await messages.get_no_object_with_this_id_message(
                        str(inline_args)[0]
                    )
                )
            ]

    async def handle_get_global_statistics(
        self,
        tg_user: TgUser,
    ) -> list[MessageToSend]:
        """
        Handles /globalstats command
        """

        messages = self.__msgs_content_factory.get_messages_content(
            tg_user.language_code
        )

        try:
            support_user = (
                await self.__support_user_controller.authorize_support_user(
                    tg_user.tg_user_id
                )
            )

            stats = await self.__support_user_controller.get_global_statistics(
                support_user
            )

            return [
                self.__msgs_to_send_factory.get_text_to_send(
                    await messages.get_global_statistics_message(stats)
                )
            ]

        except (UserIsNotAuthorizedError, PermissionDeniedError):
            return [
                await self.__get_permission_denied_text_message(
                    messages, tg_user
                )
            ]

    async def handle_add_role(
        self, tg_user: TgUser, inline_args: list[str]
    ) -> list[MessageToSend]:
        messages = self.__msgs_content_factory.get_messages_content(
            tg_user.language_code
        )

        if not (
            ArgumentsValidator(inline_args)
            .convertable(RoleName)
            .next()
            .satisfies(lambda x: x in ["1", "0"])
            .next()
            .satisfies(lambda x: x in ["1", "0"])
            .is_valid()
        ):
            can_manage_support_users_role_argument_name = (
                messages.can_manage_support_users_role_argument_name
            )

            return [
                self.__msgs_to_send_factory.get_text_to_send(
                    await messages.get_incorrect_arguments_passed_message(
                        [
                            messages.role_name_argument_name,
                            can_manage_support_users_role_argument_name,
                            messages.can_answer_questions_argument_name,
                        ],
                        inline_args,
                    )
                )
            ]

        role_name = RoleName(inline_args[0])

        can_answer_questions = bool(int(inline_args[1]))
        can_manage_support_users = bool(int(inline_args[2]))

        try:
            support_user = (
                await self.__support_user_controller.authorize_support_user(
                    tg_user.tg_user_id
                )
            )
        except UserIsNotAuthorizedError:
            return [
                await self.__get_permission_denied_text_message(
                    messages, tg_user
                )
            ]

        try:
            role = await self.__support_user_controller.add_role(
                support_user,
                RoleName(role_name),
                # TODO: We should add a way to make description for roles
                RoleDescription(""),
                can_answer_questions,
                can_manage_support_users,
            )

        except RoleNameDuplicationError:
            return [
                self.__msgs_to_send_factory.get_text_to_send(
                    await messages.get_role_name_duplicate_message()
                )
            ]

        except PermissionDeniedError:
            return [
                await self.__get_permission_denied_text_message(
                    messages, tg_user
                )
            ]

        return [
            self.__msgs_to_send_factory.get_text_to_send(
                await messages.get_successful_role_addition_message(role)
            )
        ]

    async def handle_get_role_info(
        self, tg_user: TgUser, inline_args: list[str]
    ) -> list[MessageToSend]:
        messages = self.__msgs_content_factory.get_messages_content(
            tg_user.language_code
        )

        if (
            not ArgumentsValidator(inline_args)
            .convertable(self.__role_id_type)
            .is_valid()
        ):
            return [
                self.__msgs_to_send_factory.get_text_to_send(
                    await messages.get_incorrect_arguments_passed_message(
                        [messages.answer_id_argument_name], inline_args
                    )
                )
            ]

        id = self.__role_id_type(inline_args[0])

        try:
            support_user = (
                await self.__support_user_controller.authorize_support_user(
                    tg_user.tg_user_id
                )
            )
        except UserIsNotAuthorizedError:
            return [
                await self.__get_permission_denied_text_message(
                    messages, tg_user
                )
            ]

        try:
            role_info = await self.__support_user_controller.get_role_info(
                support_user, RoleIdType(id)
            )

        except NoSuchRole:
            return [
                self.__msgs_to_send_factory.get_text_to_send(
                    await messages.get_no_object_with_this_id_message(str(id))
                )
            ]

        except PermissionDeniedError:
            return [
                await self.__get_permission_denied_text_message(
                    messages, tg_user
                )
            ]

        return [
            self.__msgs_to_send_factory.get_text_to_send(
                await messages.get_role_info_message(role_info)
            )
        ]

    async def handle_get_all_roles(
        self, tg_user: TgUser, inline_args: list[str]
    ) -> list[MessageToSend]:
        """
        Handles /allroles command
        """
        messages = self.__msgs_content_factory.get_messages_content(
            tg_user.language_code
        )

        try:
            support_user = (
                await self.__support_user_controller.authorize_support_user(
                    tg_user.tg_user_id
                )
            )
        except UserIsNotAuthorizedError:
            return [
                await self.__get_permission_denied_text_message(
                    messages, tg_user
                )
            ]

        try:
            roles_dtos = await self.__support_user_controller.get_all_roles(
                support_user
            )

        except PermissionDeniedError:
            return [
                await self.__get_permission_denied_text_message(
                    messages, tg_user
                )
            ]

        return [
            self.__msgs_to_send_factory.get_text_to_send(
                await messages.get_roles_list_message(roles_dtos)
            )
        ]

    async def handle_delete_role(
        self, tg_user: TgUser, inline_args: list[str]
    ) -> list[MessageToSend]:
        messages = self.__msgs_content_factory.get_messages_content(
            tg_user.language_code
        )

        if (
            not ArgumentsValidator(inline_args)
            .convertable(self.__role_id_type)
            .is_valid()
        ):
            return [
                self.__msgs_to_send_factory.get_text_to_send(
                    await messages.get_incorrect_arguments_passed_message(
                        [messages.answer_id_argument_name],
                        inline_args,
                    ),
                )
            ]

        id = self.__role_id_type(inline_args[0])

        try:
            support_user = (
                await self.__support_user_controller.authorize_support_user(
                    tg_user.tg_user_id
                )
            )
        except UserIsNotAuthorizedError:
            return [
                await self.__get_permission_denied_text_message(
                    messages, tg_user
                )
            ]

        try:
            role_dto = await self.__support_user_controller.delete_role(
                support_user, id
            )
        except PermissionDeniedError:
            return [
                await self.__get_permission_denied_text_message(
                    messages, tg_user
                )
            ]

        except NoSuchRole:
            return [
                self.__msgs_to_send_factory.get_text_to_send(
                    await messages.get_no_object_with_this_id_message(str(id)),
                )
            ]

        return [
            self.__msgs_to_send_factory.get_text_to_send(
                await messages.role_deleted_message(role_dto)
            )
        ]

    async def handle_add_support_user(
        self, tg_user: TgUser, inline_args: list[str]
    ) -> list[MessageToSend]:
        messages = self.__msgs_content_factory.get_messages_content(
            tg_user.language_code
        )

        if (
            not ArgumentsValidator(inline_args)
            .convertable(self.__regular_user_id_type)
            .next()
            .convertable(self.__role_id_type)
            .next()
            .convertable(DescriptiveName)
            .is_valid()
        ):
            return [
                self.__msgs_to_send_factory.get_text_to_send(
                    await messages.get_incorrect_arguments_passed_message(
                        [
                            messages.regular_user_id_argument_name,
                            messages.role_id_argument_name,
                            messages.support_user_descriptive_name,
                        ],
                        inline_args,
                    )
                )
            ]

        regular_user_id = self.__regular_user_id_type(inline_args[0])
        role_id = self.__role_id_type(inline_args[1])
        descriptive_name = DescriptiveName(inline_args[2])

        try:
            support_user = (
                await self.__support_user_controller.authorize_support_user(
                    tg_user.tg_user_id
                )
            )
        except UserIsNotAuthorizedError:
            return [
                await self.__get_permission_denied_text_message(
                    messages, tg_user
                )
            ]

        try:
            support_user_dto = (
                await self.__support_user_controller.add_support_user(
                    support_user,
                    TgUserId(regular_user_id),
                    RoleIdType(role_id),
                    descriptive_name,
                )
            )

        except PermissionDeniedError:
            return [
                await self.__get_permission_denied_text_message(
                    messages, tg_user
                )
            ]

        return [
            self.__msgs_to_send_factory.get_text_to_send(
                await messages.get_successful_support_user_addition_message(
                    support_user_dto
                )
            )
        ]

    async def handle_activate_support_user(
        self, tg_user: TgUser, inline_args: list[str]
    ) -> list[MessageToSend]:
        messages = self.__msgs_content_factory.get_messages_content(
            tg_user.language_code
        )

        if not (
            ArgumentsValidator(inline_args)
            .convertable(self.__support_user_id_type)
            .is_valid()
        ):
            return [
                self.__msgs_to_send_factory.get_text_to_send(
                    await messages.get_incorrect_arguments_passed_message(
                        [messages.support_user_id_argument_name], inline_args
                    )
                )
            ]

        id = self.__support_user_id_type(inline_args[0])

        try:
            support_user = (
                await self.__support_user_controller.authorize_support_user(
                    tg_user.tg_user_id
                )
            )
        except UserIsNotAuthorizedError:
            return [
                await self.__get_permission_denied_text_message(
                    messages, tg_user
                )
            ]

        try:
            activated_support_user = (
                await self.__support_user_controller.activate_support_user(
                    support_user, TgUserId(id)
                )
            )
        except PermissionDeniedError:
            return [
                await self.__get_permission_denied_text_message(
                    messages, tg_user
                )
            ]

        return [
            self.__msgs_to_send_factory.get_text_to_send(
                await messages.get_support_user_activation_message(
                    activated_support_user
                )
            )
        ]

    async def handle_deactivate_support_user(
        self, tg_user: TgUser, inline_args: list[str]
    ) -> list[MessageToSend]:
        messages = self.__msgs_content_factory.get_messages_content(
            tg_user.language_code
        )

        if not (
            ArgumentsValidator(inline_args)
            .convertable(self.__support_user_id_type)
            .is_valid()
        ):
            return [
                self.__msgs_to_send_factory.get_text_to_send(
                    await messages.get_incorrect_arguments_passed_message(
                        [messages.support_user_id_argument_name], inline_args
                    )
                )
            ]

        id = self.__support_user_id_type(inline_args[0])

        try:
            support_user = (
                await self.__support_user_controller.authorize_support_user(
                    tg_user.tg_user_id
                )
            )
        except UserIsNotAuthorizedError:
            return [
                await self.__get_permission_denied_text_message(
                    messages, tg_user
                )
            ]

        try:
            support_user_deactivated = (
                await self.__support_user_controller.deactivate_support_user(
                    support_user, id
                )
            )

        except PermissionDeniedError:
            return [
                await self.__get_permission_denied_text_message(
                    messages, tg_user
                )
            ]

        return [
            self.__msgs_to_send_factory.get_text_to_send(
                await messages.get_support_user_deactivation_message(
                    support_user_deactivated
                )
            )
        ]

    async def handle_get_support_user_info(
        self, tg_user: TgUser, inline_args: list[str]
    ) -> list[MessageToSend]:
        """
        Handles /getsupuser command
        """

        messages = self.__msgs_content_factory.get_messages_content(
            tg_user.language_code
        )

        if not (
            ArgumentsValidator(inline_args)
            .convertable(self.__support_user_id_type)
            .is_valid()
        ):
            return [
                self.__msgs_to_send_factory.get_text_to_send(
                    await messages.get_incorrect_arguments_passed_message(
                        [messages.support_user_id_argument_name], inline_args
                    )
                )
            ]

        id = self.__support_user_id_type(inline_args[0])

        try:
            support_user = (
                await self.__support_user_controller.authorize_support_user(
                    tg_user.tg_user_id
                )
            )
        except UserIsNotAuthorizedError:
            return [
                await self.__get_permission_denied_text_message(
                    messages, tg_user
                )
            ]

        try:
            support_user_info = await self.__support_user_controller.get_support_user_info_by_id(  # noqa: E501
                support_user, TgUserId(id)
            )

        except PermissionDeniedError:
            return [
                await self.__get_permission_denied_text_message(
                    messages, tg_user
                )
            ]

        except NoSuchSupportUser:
            return [
                await self.__get_no_such_support_user_text_message(
                    messages, id
                )
            ]

        return [
            self.__msgs_to_send_factory.get_text_to_send(
                await messages.get_support_user_info_message(support_user_info)
            )
        ]

    async def handle_get_all_suppurt_users(
        self,
        tg_user: TgUser,
    ) -> list[MessageToSend]:
        """
        Handles /allsupusers command
        """

        messages = self.__msgs_content_factory.get_messages_content(
            tg_user.language_code
        )

        try:
            support_user = (
                await self.__support_user_controller.authorize_support_user(
                    tg_user.tg_user_id
                )
            )

        except UserIsNotAuthorizedError:
            return [
                await self.__get_permission_denied_text_message(
                    messages, tg_user
                )
            ]

        try:
            support_users_dtos = (
                await self.__support_user_controller.get_all_support_users(
                    support_user
                )
            )

        except PermissionDeniedError:
            return [
                await self.__get_permission_denied_text_message(
                    messages, tg_user
                )
            ]

        return [
            self.__msgs_to_send_factory.get_text_to_send(
                await messages.get_support_users_list_message(
                    support_users_dtos
                )
            )
        ]

    async def handle_get_question(
        self, tg_user: TgUser, inline_args: list[str]
    ) -> list[MessageToSend]:
        """
        Handles /question command
        """

        messages = self.__msgs_content_factory.get_messages_content(
            tg_user.language_code
        )

        try:
            support_user = (
                await self.__support_user_controller.authorize_support_user(
                    tg_user.tg_user_id
                )
            )
        except UserIsNotAuthorizedError:
            return [
                await self.__get_permission_denied_text_message(
                    messages, tg_user
                )
            ]

        if not inline_args:
            question_info = (
                await self.__support_user_controller.get_question_to_answer(
                    support_user
                )
            )

            if not question_info:
                no_quetstions_to_answer_left_message = (
                    await messages.get_no_quetstions_to_answer_left_message()
                )

                return [
                    self.__msgs_to_send_factory.get_text_to_send(
                        no_quetstions_to_answer_left_message
                    )
                ]

            return [
                await self.__get_question_info_text_message(
                    question_info, messages
                )
            ]

        if (
            not ArgumentsValidator(inline_args)
            .convertable(self.__question_id_type)
            .is_valid()
        ):
            return [
                self.__msgs_to_send_factory.get_text_to_send(
                    await messages.get_incorrect_arguments_passed_message(
                        [messages.question_id_argument_name], inline_args
                    )
                )
            ]

        id = self.__question_id_type(inline_args[0])

        try:
            question_info = (
                await self.__support_user_controller.get_question_info_by_id(
                    support_user, TgMessageIdType(id)
                )
            )

        except PermissionDeniedError:
            return [
                await self.__get_permission_denied_text_message(
                    messages, tg_user
                )
            ]

        except NoSuchQuestion:
            return [
                await self.__get_no_such_question_text_message(messages, id)
            ]

        if not question_info:
            return [
                await self.__get_no_such_question_text_message(messages, id)
            ]

        return [
            await self.__get_question_info_text_message(
                question_info, messages
            )
        ]

    async def handle_get_question_answers(
        self, tg_user: TgUser, inline_args: list[str]
    ) -> list[MessageToSend]:
        """
        Handles /answers [question_id: int] command
        """

        messages = self.__msgs_content_factory.get_messages_content(
            tg_user.language_code
        )

        if not (
            ArgumentsValidator(inline_args)
            .convertable(self.__question_id_type)
            .is_valid()
        ):
            return [
                self.__msgs_to_send_factory.get_text_to_send(
                    await messages.get_incorrect_arguments_passed_message(
                        [messages.question_id_argument_name], inline_args
                    )
                )
            ]

        id = self.__question_id_type(inline_args[0])

        try:
            support_user = (
                await self.__support_user_controller.authorize_support_user(
                    tg_user.tg_user_id
                )
            )
        except UserIsNotAuthorizedError:
            return [
                await self.__get_permission_denied_text_message(
                    messages, tg_user
                )
            ]

        try:
            question_answers = (
                await self.__support_user_controller.get_question_answers(
                    support_user, TgMessageIdType(id)
                )
            )

        except PermissionDeniedError:
            return [
                await self.__get_permission_denied_text_message(
                    messages, tg_user
                )
            ]

        except NoSuchQuestion:
            return [
                await self.__get_no_such_question_text_message(messages, id)
            ]

        return [
            self.__msgs_to_send_factory.get_text_to_send(
                await messages.get_answers_list_message(question_answers)
            )
        ]

    async def handle_bind_question(
        self, tg_user: TgUser, inline_args: list[str]
    ) -> list[MessageToSend]:
        """
        Handles /bind command
        """

        messages = self.__msgs_content_factory.get_messages_content(
            tg_user.language_code
        )

        if not (
            ArgumentsValidator(inline_args)
            .convertable(self.__question_id_type)
            .is_valid()
        ):
            return [
                self.__msgs_to_send_factory.get_text_to_send(
                    await messages.get_incorrect_arguments_passed_message(
                        [messages.question_id_argument_name], inline_args
                    )
                )
            ]

        id = self.__question_id_type(inline_args[0])

        try:
            support_user = (
                await self.__support_user_controller.authorize_support_user(
                    tg_user.tg_user_id
                )
            )
        except UserIsNotAuthorizedError:
            return [
                await self.__get_permission_denied_text_message(
                    messages, tg_user
                )
            ]

        try:
            bound_question = (
                await self.__support_user_controller.bind_question(
                    support_user, id
                )
            )

        except PermissionDeniedError:
            return [
                await self.__get_permission_denied_text_message(
                    messages, tg_user
                )
            ]

        except NoSuchQuestion:
            return [
                await self.__get_no_such_question_text_message(messages, id)
            ]

        return [
            self.__msgs_to_send_factory.get_text_to_send(
                await messages.get_successful_binding_message(bound_question)
            )
        ]

    async def handle_unbind_question(
        self, tg_user: TgUser, inline_args: list[str]
    ) -> list[MessageToSend]:
        """
        Handles /unbind command
        """

        messages = self.__msgs_content_factory.get_messages_content(
            tg_user.language_code
        )

        try:
            support_user = (
                await self.__support_user_controller.authorize_support_user(
                    tg_user.tg_user_id
                )
            )
        except UserIsNotAuthorizedError:
            return [
                await self.__get_permission_denied_text_message(
                    messages, tg_user
                )
            ]

        try:
            await self.__support_user_controller.unbind_question(support_user)

        except PermissionDeniedError:
            return [
                await self.__get_permission_denied_text_message(
                    messages, tg_user
                )
            ]

        except NoBoundQuestion:
            return [
                self.__msgs_to_send_factory.get_text_to_send(
                    await messages.get_no_bound_question_message()
                )
            ]

        return [
            self.__msgs_to_send_factory.get_text_to_send(
                await messages.get_successful_unbinding_message()
            )
        ]

    # ANSWERS

    async def handle_get_answer_info(
        self, tg_user: TgUser, inline_args: list[str]
    ) -> list[MessageToSend]:
        """
        Handles /answer [answerId] command
        """

        messages = self.__msgs_content_factory.get_messages_content(
            tg_user.language_code
        )

        if not (
            ArgumentsValidator(inline_args)
            .convertable(self.__answer_id_type)
            .is_valid()
        ):
            return [
                self.__msgs_to_send_factory.get_text_to_send(
                    await messages.get_incorrect_arguments_passed_message(
                        [messages.answer_id_argument_name], inline_args
                    )
                )
            ]

        id = self.__answer_id_type(inline_args[0])

        try:
            support_user = (
                await self.__support_user_controller.authorize_support_user(
                    tg_user.tg_user_id
                )
            )
        except UserIsNotAuthorizedError:
            return [
                await self.__get_permission_denied_text_message(
                    messages, tg_user
                )
            ]

        try:
            answer_info = await self.__support_user_controller.get_answer_info(
                support_user, TgMessageIdType(id)
            )

        except NoSuchAnswer:
            return [
                self.__msgs_to_send_factory.get_text_to_send(
                    await messages.get_no_object_with_this_id_message(str(id))
                )
            ]

        return [
            self.__msgs_to_send_factory.get_text_to_send(
                await messages.get_answer_info_message(answer_info)
            )
        ]

    # MESSAGE HANDLERS

    async def handle_message(
        self,
        tg_user: TgUser,
        tg_message: TgMessage,
        inline_args: list[str],
    ) -> list[MessageToSend]:
        """
        Handles all text messages
        """

        messages = self.__msgs_content_factory.get_messages_content(
            tg_user.language_code
        )

        try:
            support_user = (
                await self.__support_user_controller.authorize_support_user(
                    tg_user.tg_user_id
                )
            )

            # FIXME: Add special domain event

            answering_event = (
                await self.__support_user_controller.answer_bound_question(
                    support_user,
                    tg_message.message_text,
                    tg_message.tg_message_id,
                )
            )

            return [
                self.__msgs_to_send_factory.get_text_to_send(
                    await messages.get_successful_answering_message(
                        answering_event.question_dto,
                        answering_event.answer_dto,
                    )
                ),
                self.__msgs_to_send_factory.get_text_to_send(
                    await messages.get_answer_for_regular_user_message(
                        answering_event.question_dto,
                        answering_event.answer_dto,
                    ),
                    chat_id=int(
                        answering_event.regular_user_asked_dto.tg_bot_id
                    ),
                ),
            ]

        except NoBoundQuestion:
            return [
                self.__msgs_to_send_factory.get_text_to_send(
                    await messages.get_no_bound_question_message()
                ),
            ]

        except UserIsNotAuthorizedError:
            regular_user = (
                await self.__regular_user_controller.authorize_regular_user(
                    tg_user.tg_user_id
                )
            )

            question = await self.__regular_user_controller.ask_question(
                regular_user,
                tg_message.message_text,
                tg_message.tg_message_id,
            )

            return [
                self.__msgs_to_send_factory.get_text_to_send(
                    await messages.get_successful_asking_message(question)
                )
            ]

    async def handle_file(
        self,
        tg_user: TgUser,
        tg_file: TgFile | None,
    ) -> list[MessageToSend]:
        """Implements the bot logic when a file is sent

        Args:
            tg_user (TgUser): A Telegram user that sent the file
            tg_file (TgFile | None): A Telgram file or None
            if sent file type is not supported

        Returns:
            list[MessageToSend]: list with messages the bot should send
        """
        messages = self.__msgs_content_factory.get_messages_content(
            tg_user.language_code
        )

        if not tg_file:
            return [
                self.__msgs_to_send_factory.get_text_to_send(
                    await messages.get_unsupported_message_type_message()
                )
            ]

        try:
            support_user = (
                await self.__support_user_controller.authorize_support_user(
                    tg_user.tg_user_id
                )
            )

            event = await self.__support_user_controller.add_attachment_to_last_answer(  # noqa: E501
                support_user,
                tg_file.file_id,
                tg_file.file_type,
                tg_file.caption,
            )

            return [
                self.__msgs_to_send_factory.get_text_to_send(
                    await messages.get_answer_attachment_addition_message(
                        event.attachment_dto
                    )
                ),
                self.__transform_attachment_dto_to_file(
                    event.attachment_dto,
                    chat_id=event.regular_user_asked.tg_bot_id,
                ),
            ]

        except UserIsNotAuthorizedError:
            pass

        regular_user = (
            await self.__regular_user_controller.authorize_regular_user(
                tg_user.tg_user_id
            )
        )

        attachment_dto = await self.__regular_user_controller.add_attachment_to_last_asked_question(  # noqa: E501
            regular_user,
            tg_file.file_id,
            tg_file.file_type,
            tg_file.caption,
        )

        return [
            self.__msgs_to_send_factory.get_text_to_send(
                await messages.get_answer_attachment_addition_message(
                    attachment_dto
                )
            ),
        ]

    async def handle_unsuppported_message_type(
        self,
        tg_user: TgUser,
    ) -> list[MessageToSend]:
        messages = self.__msgs_content_factory.get_messages_content(
            tg_user.language_code
        )

        return [
            self.__msgs_to_send_factory.get_text_to_send(
                await messages.get_unsupported_message_type_message()
            )
        ]

    async def handle_unknown_command(
        self,
        tg_user: TgUser,
    ) -> list[MessageToSend]:
        messages = self.__msgs_content_factory.get_messages_content(
            tg_user.language_code
        )

        return [
            self.__msgs_to_send_factory.get_text_to_send(
                await messages.get_unknown_command_message()
            )
        ]

    # BUTTONS HANDLERS

    # TODO: Write button handlers

    async def handle_bind_question_button(
        self, tg_user: TgUser, callback_data: str
    ) -> list[MessageToSend]:
        messages = self.__msgs_content_factory.get_messages_content(
            tg_user.language_code
        )

        if not ArgumentsValidator([callback_data]).convertable(
            self.__question_id_type
        ):
            raise IncorrectCallbackDataError()

        id = self.__question_id_type(callback_data)

        try:
            support_user = (
                await self.__support_user_controller.authorize_support_user(
                    tg_user.tg_user_id
                )
            )
        except UserIsNotAuthorizedError:
            return [
                await self.__get_permission_denied_text_message(
                    messages, tg_user
                )
            ]

        try:
            bound_question = (
                await self.__support_user_controller.bind_question(
                    support_user, id
                )
            )

        except PermissionDeniedError:
            return [
                await self.__get_permission_denied_text_message(
                    messages, tg_user
                )
            ]

        except NoSuchQuestion:
            return [
                await self.__get_no_such_question_text_message(messages, id)
            ]

        return [
            self.__msgs_to_send_factory.get_text_to_send(
                await messages.get_successful_binding_message(bound_question)
            )
        ]

    async def handle_unbind_question_button(
        self, tg_user: TgUser, callback_data: str
    ) -> list[MessageToSend]:
        messages = self.__msgs_content_factory.get_messages_content(
            tg_user.language_code
        )

        if not ArgumentsValidator([callback_data]).convertable(
            self.__question_id_type
        ):
            raise IncorrectCallbackDataError()

        try:
            support_user = (
                await self.__support_user_controller.authorize_support_user(
                    tg_user.tg_user_id
                )
            )
        except UserIsNotAuthorizedError:
            return [
                await self.__get_permission_denied_text_message(
                    messages, tg_user
                )
            ]

        try:
            await self.__support_user_controller.unbind_question(support_user)

        except PermissionDeniedError:
            return [
                await self.__get_permission_denied_text_message(
                    messages, tg_user
                )
            ]

        except NoBoundQuestion:
            return [
                self.__msgs_to_send_factory.get_text_to_send(
                    await messages.get_no_bound_question_message()
                )
            ]

        return [
            self.__msgs_to_send_factory.get_text_to_send(
                await messages.get_successful_unbinding_message()
            )
        ]

    async def handle_estimate_question_as_useful_button(
        self, tg_user: TgUser, callback_data: str
    ) -> list[MessageToSend]:
        messages = self.__msgs_content_factory.get_messages_content(
            tg_user.language_code
        )

        if not ArgumentsValidator([callback_data]).convertable(
            self.__question_id_type
        ):
            raise IncorrectCallbackDataError()

        id = self.__question_id_type(callback_data)

        regular_user = (
            await self.__regular_user_controller.authorize_regular_user(
                tg_user.tg_user_id
            )
        )

        try:
            estimation_event = (
                await self.__regular_user_controller.estimate_answer_as_useful(
                    regular_user, id
                )
            )

            messages_to_send: list[MessageToSend] = [
                self.__msgs_to_send_factory.get_text_to_send(
                    await messages.get_answer_estimated_as_useful_message(
                        estimation_event.answer_dto
                    )
                )
            ]

            if not estimation_event.support_user_answered:
                return messages_to_send

            return [
                self.__msgs_to_send_factory.get_text_to_send(
                    await messages.get_answer_estimated_as_useful_message(
                        estimation_event.answer_dto
                    )
                )
            ]

        except NoSuchAnswer:
            return [
                self.__msgs_to_send_factory.get_text_to_send(
                    await messages.get_unavailable_or_deleted_object_message()
                )
            ]

    async def handle_estimate_question_as_unuseful_button(
        self, tg_user: TgUser, callback_data: str
    ) -> list[MessageToSend]:
        messages = self.__msgs_content_factory.get_messages_content(
            tg_user.language_code
        )

        if not ArgumentsValidator([callback_data]).convertable(
            self.__question_id_type
        ):
            raise IncorrectCallbackDataError()

        id = self.__question_id_type(callback_data)

        regular_user = (
            await self.__regular_user_controller.authorize_regular_user(
                tg_user.tg_user_id
            )
        )

        estimation_event = (
            await self.__regular_user_controller.estimate_answer_as_unuseful(
                regular_user, id
            )
        )

        return [
            self.__msgs_to_send_factory.get_text_to_send(
                await messages.get_answer_estimated_as_unuseful_message(
                    estimation_event.answer_dto
                )
            )
        ]

    # FIXME: Make this private and add a single handler for button or...
    async def handle_show_question_attachments_button(
        self, tg_user: TgUser, callback_data: str
    ) -> list[MessageToSend]:
        messages = self.__msgs_content_factory.get_messages_content(
            tg_user.language_code
        )

        if not ArgumentsValidator([callback_data]).convertable(
            self.__question_id_type
        ):
            raise IncorrectCallbackDataError()

        id = self.__question_id_type(callback_data)

        try:
            support_user = (
                await self.__support_user_controller.authorize_support_user(
                    tg_user.tg_user_id
                )
            )

            attachments = await self.__support_user_controller.get_attachments_for_question(  # noqa: E501; I have no idea why black doesn't format this line
                support_user, id
            )

            return self.__transform_attachments_to_messages(attachments)

        except NoSuchQuestion:
            return [
                self.__msgs_to_send_factory.get_text_to_send(
                    await messages.get_unavailable_or_deleted_object_message()
                )
            ]

        except PermissionDeniedError:
            return [
                await self.__get_permission_denied_text_message(
                    messages, tg_user
                )
            ]

    def __transform_attachments_to_messages(
        self,
        attachments: list[AttachmentDTO],
    ) -> list[MessageToSend]:
        return list(
            map(
                lambda attachment: self.__transform_attachment_dto_to_file(
                    attachment
                ),
                attachments,
            )
        )

    def __transform_attachment_dto_to_file(
        self,
        attachment: AttachmentDTO,
        chat_id: int | None = None,
        reply_to: int | None = None,
    ) -> FileToSend:
        match attachment.attachment_type:
            case TgFileType.IMAGE:
                return self.__msgs_to_send_factory.get_image_to_send(
                    attachment.tg_file_id,
                    chat_id=chat_id,
                    reply_to=reply_to,
                    caption=attachment.caption,
                )

            case TgFileType.VIDEO:
                return self.__msgs_to_send_factory.get_video_to_send(
                    attachment.tg_file_id,
                    chat_id=chat_id,
                    reply_to=reply_to,
                    caption=attachment.caption,
                )

            case TgFileType.AUDIO:
                return self.__msgs_to_send_factory.get_audio_to_send(
                    attachment.tg_file_id,
                    chat_id=chat_id,
                    reply_to=reply_to,
                    caption=attachment.caption,
                )

            case TgFileType.VOICE:
                return self.__msgs_to_send_factory.get_voice_to_send(
                    attachment.tg_file_id,
                    chat_id=chat_id,
                    reply_to=reply_to,
                    caption=attachment.caption,
                )

            case TgFileType.DOCUMENT:
                return self.__msgs_to_send_factory.get_document_to_send(
                    attachment.tg_file_id,
                    chat_id=chat_id,
                    reply_to=reply_to,
                    caption=attachment.caption,
                )

        raise ValueError(
            f"Incorrect type of attachment, given type: "
            f"{attachment.attachment_type}"
        )

    async def __get_no_such_question_text_message(
        self, messages_content: MessagesContent, id: Any
    ) -> TextToSend:
        return self.__msgs_to_send_factory.get_text_to_send(
            await messages_content.get_no_object_with_this_id_message(str(id))
        )

    async def __get_no_such_support_user_text_message(
        self, messages_content: MessagesContent, id: Any
    ) -> TextToSend:
        return self.__msgs_to_send_factory.get_text_to_send(
            await messages_content.get_no_object_with_this_id_message(str(id))
        )

    async def __get_no_such_answer_text_message(
        self, messages_content: MessagesContent, id: Any
    ) -> TextToSend:
        return self.__msgs_to_send_factory.get_text_to_send(
            await messages_content.get_no_object_with_this_id_message(str(id))
        )

    async def __get_no_such_regular_user_text_message(
        self, messages_content: MessagesContent, id: Any
    ) -> TextToSend:
        return self.__msgs_to_send_factory.get_text_to_send(
            await messages_content.get_no_object_with_this_id_message(str(id))
        )

    async def __get_no_such_role_text_message(
        self, messages_content: MessagesContent, id: Any
    ) -> TextToSend:
        return self.__msgs_to_send_factory.get_text_to_send(
            await messages_content.get_no_object_with_this_id_message(str(id))
        )

    async def __get_permission_denied_text_message(
        self, messages_content: MessagesContent, tg_user: TgUser
    ) -> TextToSend:
        return self.__msgs_to_send_factory.get_text_to_send(
            await messages_content.get_permission_denied_message(tg_user)
        )

    # def __permition_denied_handler(
    #     self,
    #     func: Callable[
    #         [TgUser, str, list[str]], Awaitable[list[MessageToSend]]
    #     ],
    # ):
    #     async def wrapper(*args, **kwargs) -> list[MessageToSend]:
    #         language_code = (kwargs.get("tg_user") or args[0]).language_code
    #         try:
    #             return await func(*args, **kwargs)
    #         except PermissionDeniedError:
    #             messages = self.__msgs_content_factory.get_messages_content(
    #                 language_code
    #             )
    #             return [
    #                 self.__msgs_to_send_factory.get_text_to_send(
    #                     await messages.get_permission_denied_message(args[0])
    #                 )
    #             ]

    #     return wrapper

    async def __get_question_info_text_message(
        self, question_info: QuestionInfo, messages_content: MessagesContent
    ) -> TextToSend:
        return self.__msgs_to_send_factory.get_text_to_send(
            await messages_content.get_question_info_message(question_info),
            # JSON used here to pass an object as the callback data
            self.__markup_provider.get_question_info_buttons_markup(
                json.dumps(
                    {
                        "id": question_info.question_dto.tg_message_id,
                        "action": States.BIND_ACTION,
                    }
                ),
                json.dumps(
                    {
                        "id": question_info.question_dto.tg_message_id,
                        "action": States.UNBIND_ACTION,
                    }
                ),
                json.dumps(
                    {
                        "id": question_info.question_dto.tg_message_id,
                        "action": States.SHOW_ATTACHMENTS_ACTION,
                    }
                ),
                messages_content,
            ),
        )
