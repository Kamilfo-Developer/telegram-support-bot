from bot.entities.regular_user import RegularUser
from bot.settings import RepositoryClass
from bot.entities.support_user import SupportUser
from bot.localization.get_messages import get_messages
from bot.utils import (
    send_text_messages,
    get_file_type_and_file_id,
    is_string_int,
    TextToSend,
)
from bot.settings import (
    OWNER_PASSWORD,
    OWNER_DEFAULT_DESCRIPTIVE_NAME,
)
from bot.managers.support_user_manager import SupportUserManager
from bot.managers.regular_user_manager import RegularUserManager
from telegram.ext import ContextTypes, CallbackContext
import json


async def handle_start(update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles /start command
    """

    user = update.effective_user
    repo = RepositoryClass()

    messages = get_messages(user.language_code)

    support_user = await repo.get_support_user_by_tg_bot_user_id(user.id)

    if support_user:
        if support_user.is_owner:
            await TextToSend(
                await messages.get_start_owner_message(user, support_user)
            ).send(update)

            return

        if support_user.is_active:
            await TextToSend(
                await messages.get_start_support_user_message(
                    user, support_user
                )
            ).send(update)

            return

    regular_user = await repo.get_regular_user_by_tg_bot_user_id(
        user.id
    ) or await RegularUser.add_regular_user(user.id, repo)

    if regular_user:
        await TextToSend(
            await messages.get_start_regular_user_message(user, regular_user)
        ).send(update)

        return


async def handle_init_owner(update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles /initowner command
    """
    user = update.effective_user
    messages = get_messages(update.effective_user.language_code)
    repo = RepositoryClass()

    support_user = await repo.get_owner()

    if support_user:
        await TextToSend(
            await messages.get_already_inited_owner_message(user, support_user)
        ).send(update)

        return

    if not context.args:
        await TextToSend(
            await messages.get_incorrect_num_of_arguments_message(
                [messages.owner_password_argument_name], user
            )
        ).send(update)

        return

    password = context.args[0]

    if password != OWNER_PASSWORD:
        await TextToSend(
            await messages.get_incorrect_owner_password_message()
        ).send(update)

        return

    support_user = await SupportUser.add_support_user(
        user.id, OWNER_DEFAULT_DESCRIPTIVE_NAME, repo, is_owner=True
    )

    await TextToSend(
        await messages.get_successful_owner_init_message(user, support_user)
    ).send(update)


async def handle_help_command(update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    messages = get_messages(user.language_code)

    repo = RepositoryClass()

    support_user = await repo.get_support_user_by_tg_bot_user_id(user.id)

    if support_user and support_user.is_active:
        if support_user.is_owner:
            await TextToSend(
                await messages.get_inited_owner_help_message(
                    user, support_user
                )
            ).send(update)

            return

        await TextToSend(
            await messages.get_support_user_help_message(user, support_user)
        ).send(update)

        return

    regular_user = await repo.get_regular_user_by_tg_bot_user_id(user.id)

    if regular_user:
        await TextToSend(
            await messages.get_regular_user_help_message(user)
        ).send(update)

        return


async def handle_get_id(update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles /getid command
    """
    messages = get_messages(update.effective_user.language_code)

    get_id_messages = await messages.get_id_message(update.effective_user.id)

    await TextToSend(get_id_messages).send(update)


# STATISTICS


async def handle_global_statistics(update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles /globalstats command
    """
    user = update.effective_user

    messages = get_messages(update.effective_user.language_code)

    repo = RepositoryClass()

    support_user = await repo.get_support_user_by_tg_bot_user_id(user.id)

    support_user_manager = SupportUserManager(
        user, support_user, messages, repo
    )

    messages_to_send = await support_user_manager.get_global_statistics()

    for message in messages_to_send:
        await message.send(update)


# ROLES


async def handle_add_role(update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    messages = get_messages(update.effective_user.language_code)

    repo = RepositoryClass()

    support_user = await repo.get_support_user_by_tg_bot_user_id(user.id)

    if not context.args or len(context.args) < 3 or len(context.args) > 3:
        await TextToSend(
            await messages.get_incorrect_num_of_arguments_message(
                [
                    messages.role_name_argument_name,
                    messages.can_manage_support_users_role_argument_name,
                    messages.can_answer_questions_argument_name,
                ]
            )
        ).send(update)

        return

    if not (is_string_int(context.args[1]) and is_string_int(context.args[2])):
        await TextToSend(
            await messages.get_incorrect_arguments_passed_message()
        ).send(update)

        return

    role_name = context.args[0]
    can_answer_questions = bool(int(context.args[1]))
    can_manage_support_users = bool(int(context.args[2]))

    manager = SupportUserManager(user, support_user, messages, repo)

    messages_to_send = await manager.add_role(
        role_name,
        can_answer_questions,
        can_manage_support_users,
        update.message.date,
    )

    for message in messages_to_send:
        await message.send(update)


async def handle_get_role(update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    messages = get_messages(user.language_code)

    repo = RepositoryClass()

    support_user = await repo.get_support_user_by_tg_bot_user_id(user.id)

    if not context.args:
        await send_text_messages(
            TextToSend(
                await messages.get_incorrect_num_of_arguments_message(
                    [messages.answer_id_argument_name]
                )
            ),
            update,
        )

        return

    if not is_string_int(context.args[0]):
        await update.message.reply_text(
            messages.get_incorrect_arguments_passed_message()
        )

        return

    id = int(context.args[0])

    manager = SupportUserManager(user, support_user, messages, repo)

    messages_to_send = await manager.get_role(id)

    for message in messages_to_send:
        await message.send(update)


async def handle_get_all_roles(update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles /allroles command
    """
    user = update.effective_user

    repo = RepositoryClass()

    messages = get_messages(update.effective_user.language_code)

    support_user = await repo.get_support_user_by_tg_bot_user_id(user.id)

    manager = SupportUserManager(user, support_user, messages, repo)

    messages_to_send = await manager.get_all_roles()

    for message in messages_to_send:
        await message.send(update)


async def handle_delete_role(update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    messages = get_messages(user.language_code)

    repo = RepositoryClass()

    support_user = await repo.get_support_user_by_tg_bot_user_id(user.id)

    if not context.args:
        await send_text_messages(
            TextToSend(
                await messages.get_incorrect_num_of_arguments_message(
                    [messages.answer_id_argument_name]
                )
            ),
            update,
        )

        return

    if not is_string_int(context.args[0]):
        await update.message.reply_text(
            messages.get_incorrect_arguments_passed_message()
        )

        return

    id = int(context.args[0])

    manager = SupportUserManager(user, support_user, messages, repo)

    messages_to_send = await manager.get_role(id)

    for message in messages_to_send:
        await message.send(update)


# SUPPORT USERS


async def handle_add_support_user(update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    messages = get_messages(update.effective_user.language_code)

    repo = RepositoryClass()

    support_user = await repo.get_support_user_by_tg_bot_user_id(user.id)

    manager = SupportUserManager(user, support_user, messages, repo)

    if not context.args or len(context.args) < 3 or len(context.args) > 3:
        await TextToSend(
            await messages.get_incorrect_num_of_arguments_message(
                [
                    messages.regular_user_id_argument_name,
                    messages.role_id_argument_name,
                    messages.support_user_descriptive_name,
                ]
            )
        ).send(update)

        return

    if not (is_string_int(context.args[0]) and is_string_int(context.args[1])):
        await TextToSend(
            await messages.get_incorrect_arguments_passed_message()
        ).send(update)

        return

    regular_user_tg_bot_id = int(context.args[0])
    role_id = int(context.args[1])
    descriptive_name = context.args[2]

    messages_to_send = await manager.add_support_user(
        regular_user_tg_bot_id, role_id, descriptive_name, update.message.date
    )

    for message in messages_to_send:
        await message.send(update)


async def handle_activate_support_user(
    update, context: ContextTypes.DEFAULT_TYPE
):
    user = update.effective_user

    messages = get_messages(update.effective_user.language_code)

    repo = RepositoryClass()

    support_user = await repo.get_support_user_by_tg_bot_user_id(user.id)

    manager = SupportUserManager(user, support_user, messages, repo)

    if not context.args or not len(context.args) == 1:
        await TextToSend(
            await messages.get_incorrect_num_of_arguments_message(
                [messages.support_user_id_argument_name]
            )
        ).send(update)
        return

    if not is_string_int(context.args[0]):
        await TextToSend(
            await messages.get_incorrect_arguments_passed_message()
        ).send(update)

        return

    id = int(context.args[0])

    messages_to_send = await manager.activate_support_user(id)

    for message in messages_to_send:
        await message.send(update)


async def handle_deactivate_support_user(
    update, context: ContextTypes.DEFAULT_TYPE
):
    user = update.effective_user

    messages = get_messages(update.effective_user.language_code)

    repo = RepositoryClass()

    support_user = await repo.get_support_user_by_tg_bot_user_id(user.id)

    manager = SupportUserManager(user, support_user, messages, repo)

    if not context.args or not len(context.args) == 1:
        await TextToSend(
            await messages.get_incorrect_num_of_arguments_message(
                [messages.support_user_id_argument_name]
            )
        ).send(update)

        return

    if not is_string_int(context.args[0]):
        await TextToSend(
            await messages.get_incorrect_arguments_passed_message()
        ).send(update)

        return

    id = int(context.args[0])

    messages_to_send = await manager.deactivate_support_user(id)

    for message in messages_to_send:
        await message.send(update)


async def handle_get_support_user(update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles /getsupuser command
    """
    user = update.effective_user

    messages = get_messages(update.effective_user.language_code)

    repo = RepositoryClass()

    support_user = await repo.get_support_user_by_tg_bot_user_id(user.id)

    manager = SupportUserManager(user, support_user, messages, repo)

    if not context.args or not len(context.args) == 1:
        await TextToSend(
            await messages.get_incorrect_num_of_arguments_message(
                [messages.support_user_id_argument_name]
            )
        ).send(update)

        return

    if not is_string_int(context.args[0]):
        await TextToSend(
            await messages.get_incorrect_arguments_passed_message()
        ).send(update)

        return

    id = int(context.args[0])

    messages_to_send = await manager.get_support_user(id)

    for message in messages_to_send:
        await message.send(update)


async def handle_get_all_suppurt_users(
    update, context: ContextTypes.DEFAULT_TYPE
):
    """
    Handles /allsupusers command
    """
    user = update.effective_user

    repo = RepositoryClass()

    messages = get_messages(update.effective_user.language_code)

    support_user = await repo.get_support_user_by_tg_bot_user_id(user.id)

    manager = SupportUserManager(user, support_user, messages, repo)

    messages_to_send = await manager.get_all_support_users()

    for message in messages_to_send:
        await message.send(update)


# QUESTIONS


async def handle_get_question(update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles /question command
    """
    user = update.effective_user

    messages = get_messages(user.language_code)

    repo = RepositoryClass()

    support_user = await repo.get_support_user_by_tg_bot_user_id(user.id)

    manager = SupportUserManager(user, support_user, messages, repo)

    if context.args:
        if not is_string_int(context.args[0]):
            await TextToSend(
                await messages.get_incorrect_arguments_passed_message()
            ).send(update)

            return

        id = int(context.args[0])

        messages_to_send = await manager.get_question_by_id(id)

        for message in messages_to_send:
            await message.send(update)

        return

    messages_to_send = await manager.get_random_unanswered_question()

    for message in messages_to_send:
        await message.send(update)

    return


async def handle_get_question_answers(
    update, context: ContextTypes.DEFAULT_TYPE
):
    """
    Handles /answers [question_id: int] command
    """
    user = update.effective_user

    repo = RepositoryClass()

    messages = get_messages(update.effective_user.language_code)

    support_user = await repo.get_support_user_by_tg_bot_user_id(user.id)

    manager = SupportUserManager(user, support_user, messages, repo)

    if not context.args:
        await TextToSend(
            await messages.get_incorrect_num_of_arguments_message(
                [messages.question_id_argument_name]
            )
        ).send(update)

        return

    if not is_string_int(context.args[0]):
        await TextToSend(
            await messages.get_incorrect_arguments_passed_message()
        ).send(update)

        return

    id = int(context.args[0])

    messages_to_send = await manager.get_question_answers(id)

    for message in messages_to_send:
        await message.send(update)


async def handle_bind_question(update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles /bind command
    """
    user = update.effective_user

    messages = get_messages(user.language_code)

    repo = RepositoryClass()

    support_user = await repo.get_support_user_by_tg_bot_user_id(user.id)

    manager = SupportUserManager(user, support_user, messages, repo)

    if not context.args or len(context.args) > 1:
        await TextToSend(
            await messages.get_incorrect_num_of_arguments_message(
                [messages.question_id_argument_name]
            )
        ).send(update)

        return

    if not is_string_int(context.args[0]):
        await TextToSend(
            await messages.get_incorrect_arguments_passed_message()
        ).send(update)

        return

    id = int(context.args[0])

    messages_to_send = await manager.bind_question(id)

    for message in messages_to_send:
        await message.send(update)


async def handle_unbind_question(update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles /unbind command
    """
    user = update.effective_user

    messages = get_messages(user.language_code)

    repo = RepositoryClass()

    support_user = await repo.get_support_user_by_tg_bot_user_id(user.id)

    manager = SupportUserManager(user, support_user, messages, repo)

    messages_to_send = await manager.unbind_question()

    for message in messages_to_send:
        await message.send(update)


# ANSWERS


async def handle_get_answer(update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles /answer [answerId] command
    """
    user = update.effective_user

    messages = get_messages(user.language_code)

    repo = RepositoryClass()

    support_user = await repo.get_support_user_by_tg_bot_user_id(user.id)

    manager = SupportUserManager(user, support_user, messages, repo)

    if not context.args:
        await send_text_messages(
            TextToSend(
                await messages.get_incorrect_num_of_arguments_message(
                    [messages.answer_id_argument_name]
                )
            ),
            update,
        )

        return

    if not is_string_int(context.args[0]):
        await update.message.reply_text(
            messages.get_incorrect_arguments_passed_message()
        )

        return

    id = int(context.args[0])

    messages_to_send = await manager.get_answer_by_id(id)

    for message in messages_to_send:
        await message.send(update)

    return


# MESSAGE HANDLERS


async def handle_message(update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles all text messages
    """

    user = update.effective_user

    messages = get_messages(user.language_code)

    repo = RepositoryClass()

    message = update.message

    support_user = await repo.get_support_user_by_tg_bot_user_id(user.id)

    if support_user:
        support_user_manager = SupportUserManager(
            user, support_user, messages, repo
        )

        messages_to_send = await support_user_manager.answer_binded_question(
            message.text, message.id, message.date
        )

        for message in messages_to_send:
            await message.send(update)

        return

    regular_user = await repo.get_regular_user_by_tg_bot_user_id(user.id)

    regular_user_manager = RegularUserManager(
        user, regular_user, messages, repo
    )

    messages_for_regular_user = await regular_user_manager.ask_question(
        message.text, message.id, message.date
    )

    for message in messages_for_regular_user:
        await message.send(update)

    return


async def handle_file(update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    messages = get_messages(user.language_code)

    repo = RepositoryClass()

    file_type, file_id = get_file_type_and_file_id(update)

    if not (file_type and file_id):
        await send_text_messages(
            TextToSend(await messages.get_unsupported_message_type_message()),
            update,
        )

        return

    suppport_user = await repo.get_support_user_by_tg_bot_user_id(user.id)

    if suppport_user:
        support_user_manager = SupportUserManager(
            user, suppport_user, messages, repo
        )

        messages_to_send = (
            await support_user_manager.add_attachment_to_last_answer(
                file_id, file_type, update.message.date
            )
        )

        for message in messages_to_send:
            await message.send(update)

        return

    regular_user = await repo.get_regular_user_by_tg_bot_user_id(user.id)

    if regular_user:
        regular_user_manager = RegularUserManager(
            user, regular_user, messages, repo
        )

        messages_to_send = (
            await regular_user_manager.add_attachment_to_last_asked_question(
                file_id, file_type, update.message.date
            )
        )

        for message in messages_to_send:
            await message.send(update)

        return


async def handle_unsuppported_message_type(
    update, context: ContextTypes.DEFAULT_TYPE
):
    user = update.effective_user

    messages = get_messages(user.language_code)

    await TextToSend(
        await messages.get_unsupported_message_type_message()
    ).send(update)


async def handle_unknown_command(update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    messages = get_messages(user.language_code)

    await TextToSend(await messages.get_unknown_command_message()).send(update)


# BUTTONS HANDLERS


async def handle_bind_question_button(update, context: CallbackContext):
    user = update.effective_user

    messages = get_messages(user.language_code)

    repo = RepositoryClass()

    support_user = await repo.get_support_user_by_tg_bot_user_id(user.id)

    manager = SupportUserManager(user, support_user, messages, repo)

    query = update.callback_query

    data = json.loads(update.callback_query.data)

    messages_to_send = await manager.bind_question(data["id"])

    for message in messages_to_send:
        await message.send(update)

    await query.answer()


async def handle_unbind_question_button(update, context: CallbackContext):
    user = update.effective_user

    messages = get_messages(user.language_code)

    repo = RepositoryClass()

    support_user = await repo.get_support_user_by_tg_bot_user_id(user.id)

    manager = SupportUserManager(user, support_user, messages, repo)

    query = update.callback_query

    messages_to_send = await manager.unbind_question()

    for message in messages_to_send:
        await message.send(update)

    await query.answer()

    return


async def handle_estimate_question_as_useful_button(
    update, context: CallbackContext
):
    user = update.effective_user

    messages = get_messages(user.language_code)

    repo = RepositoryClass()

    regular_user = await repo.get_regular_user_by_tg_bot_user_id(user.id)

    manager = RegularUserManager(user, regular_user, messages, repo)

    query = update.callback_query

    data = json.loads(query.data)

    messages_to_send = await manager.estimate_answer_as_useful(data["id"])

    for message in messages_to_send:
        await message.send(update)

    await query.answer()


async def handle_estimate_question_as_unuseful_button(
    update, context: CallbackContext
):
    user = update.effective_user

    messages = get_messages(user.language_code)

    repo = RepositoryClass()

    regular_user = await repo.get_regular_user_by_tg_bot_user_id(user.id)

    manager = RegularUserManager(user, regular_user, messages, repo)

    query = update.callback_query

    data = json.loads(query.data)

    messages_to_send = await manager.estimate_answer_as_unuseful(data["id"])

    for message in messages_to_send:
        await message.send(update)

    await query.answer()


async def handle_show_attachments_button(update, context: CallbackContext):
    user = update.effective_user

    messages = get_messages(user.language_code)

    repo = RepositoryClass()

    support_user = await repo.get_support_user_by_tg_bot_user_id(user.id)

    manager = SupportUserManager(user, support_user, messages, repo)

    query = update.callback_query

    data = json.loads(query.data)

    messages_to_send = await manager.get_attachments_for_question(data["id"])

    for message in messages_to_send:
        await message.send(update)

    await query.answer()

    return
