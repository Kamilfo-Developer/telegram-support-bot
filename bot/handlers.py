from bot.entities.regular_user import RegularUser
from bot.settings import RepositoryClass
from bot.entities.support_user import SupportUser
from bot.entities.question import Question
from bot.entities.role import Role
from bot.entities.answer import Answer
from bot.localization.get_messages import get_messages
from bot.utils import send_text_messages, is_string_uuid, is_string_int
from bot.settings import (
    OWNER_ID,
    OWNER_DEFAULT_DESCRIPTIVE_NAME,
)
from telegram import Update
from telegram.error import BadRequest
from telegram.ext import ContextTypes
from uuid import UUID


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
            await send_text_messages(
                await messages.get_start_owner_message(user, support_user),
                update,
            )

            return

        await send_text_messages(
            await messages.get_start_support_user_message(user, support_user),
            update,
        )

        return

    if user.id == OWNER_ID:
        await send_text_messages(
            await messages.get_start_support_user_message(user, support_user),
            update,
        )

        await send_text_messages(
            await messages.get_not_inited_owner_message(user), update
        )

        return

    regular_user = await repo.get_regular_user_by_tg_bot_user_id(
        user.id
    ) or await RegularUser.add_regular_user(user.id, repo)

    if regular_user:
        await send_text_messages(
            await messages.get_start_regular_user_message(user, regular_user),
            update,
        )

        return


async def handle_init_owner(update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles /initowner command
    """
    user = update.effective_user
    messages = get_messages(update.effective_user.language_code)
    repo = RepositoryClass()

    if user.id != OWNER_ID:
        await send_text_messages(
            await messages.get_permission_denied_message(user),
            update,
        )

        return

    support_user = await repo.get_support_user_by_tg_bot_user_id(user.id)

    if support_user:
        if support_user.is_owner:
            await send_text_messages(
                await messages.get_already_inited_owner_message(
                    user, support_user
                ),
                update,
            )

            return

        await support_user.make_owner(repo)

        await send_text_messages(
            await messages.get_successful_owner_init_message(
                user, support_user
            ),
            update,
        )

        return

    regular_user = await repo.get_regular_user_by_tg_bot_user_id(user.id)

    if regular_user:
        await repo.delete_regular_user_with_id(regular_user.id)

    support_user = await SupportUser.add_support_user(
        user.id, OWNER_DEFAULT_DESCRIPTIVE_NAME, repo, is_owner=True
    )

    await send_text_messages(
        await messages.get_successful_owner_init_message(user, support_user),
        update,
    )


async def handle_help_command(update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    messages = get_messages(user.language_code)

    repo = RepositoryClass()

    support_user = await repo.get_support_user_by_tg_bot_user_id(user.id)

    if support_user:
        if support_user.is_owner:
            await send_text_messages(
                await messages.get_inited_owner_help_message(
                    user, support_user
                ),
                update,
            )

            return

        await send_text_messages(
            await messages.get_support_user_help_message(user, support_user),
            update,
        )

        return

    if user.id == OWNER_ID:
        await send_text_messages(
            await messages.get_not_inited_owner_help_message(user),
            update,
        )

        return

    regular_user = await repo.get_regular_user_by_tg_bot_user_id(user.id)

    if regular_user:
        await send_text_messages(
            await messages.get_regular_user_help_message(user),
            update,
        )

        return


async def handle_get_id(update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles /getid command
    """
    messages = get_messages(update.effective_user.language_code)

    get_id_messages = await messages.get_id_message(update.effective_user.id)

    await send_text_messages(get_id_messages, update)


# ROLES


async def handle_add_role(update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    messages = get_messages(update.effective_user.language_code)

    repo = RepositoryClass()

    permission_denied = True

    support_user = await repo.get_support_user_by_tg_bot_user_id(user.id)

    if support_user:
        role = await support_user.get_role(repo)

        if support_user.is_owner or (role and role.can_manage_support_users):
            permission_denied = False

    if permission_denied:
        await send_text_messages(
            await messages.get_permission_denied_message(user),
            update,
        )

        return

    if not context.args or len(context.args) < 3 or len(context.args) > 3:
        await send_text_messages(
            await messages.get_incorrect_num_of_arguments_message(
                [
                    messages.role_name_argument_name,
                    messages.can_manage_support_users_role_argument_name,
                    messages.can_answer_questions_argument_name,
                ]
            ),
            update,
        )

        return

    if not (is_string_int(context.args[1]) and is_string_int(context.args[2])):
        await send_text_messages(
            await messages.get_incorrect_arguments_passed_message(), update
        )

        return

    role_name = context.args[0]
    can_answer_questions = bool(int(context.args[1]))
    can_manage_support_users = bool(int(context.args[2]))

    role = await repo.get_role_by_name(role_name)

    if role:
        await send_text_messages(
            await messages.get_role_name_duplicate_message(), update
        )

        return

    new_role = await Role.add_role(
        role_name,
        can_answer_questions,
        can_manage_support_users,
        repo=repo,
        adding_date=update.message.date,
    )

    await send_text_messages(
        await messages.get_successful_role_addition_message(new_role),
        update,
    )


async def handle_get_role(update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    messages = get_messages(user.language_code)

    repo = RepositoryClass()

    support_user = await repo.get_support_user_by_tg_bot_user_id(user.id)

    permission_denied = True

    if support_user:
        role = await support_user.get_role(repo)

        if (role and role.can_manage_support_users) or support_user.is_owner:
            permission_denied = False

    if permission_denied:
        await send_text_messages(
            await messages.get_permission_denied_message(user),
            update,
        )

        return

    if not context.args:
        await send_text_messages(
            await messages.get_incorrect_num_of_arguments_message(
                [messages.answer_id_argument_name]
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

    role = await repo.get_role_by_id(id)

    if not role:
        await send_text_messages(
            await messages.get_no_object_with_this_id_message(str(id)),
            update,
        )

        return

    await send_text_messages(
        await messages.get_role_info_message(role),
        update,
    )

    return


# SUPPORT USERS


async def handle_add_support_user(update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    messages = get_messages(update.effective_user.language_code)

    repo = RepositoryClass()

    permission_denied = True

    support_user = await repo.get_support_user_by_tg_bot_user_id(user.id)

    if support_user:
        role = await support_user.get_role(repo)

        if support_user.is_owner or (role and role.can_manage_support_users):
            permission_denied = False

    if permission_denied:
        await send_text_messages(
            await messages.get_permission_denied_message(user),
            update,
        )

        return

    if not context.args or len(context.args) < 3 or len(context.args) > 3:
        await send_text_messages(
            await messages.get_incorrect_num_of_arguments_message(
                [
                    messages.regular_user_id_argument_name,
                    messages.role_id_argument_name,
                    messages.support_user_descriptive_name,
                ]
            ),
            update,
        )

        return

    if not (
        is_string_int(context.args[0]) and is_string_uuid(context.args[1])
    ):
        await send_text_messages(
            await messages.get_incorrect_arguments_passed_message(), update
        )

        return

    regular_user_tg_bot_id = int(context.args[0])
    role_id = UUID(context.args[1])
    descriptive_name = context.args[2]

    role_for_user = await repo.get_role_by_id(role_id)

    if not role_for_user:
        await send_text_messages(
            await messages.get_no_object_with_this_id_message(
                str(regular_user_tg_bot_id)
            ),
            update,
        )

        return

    regular_user = await repo.get_regular_user_by_tg_bot_user_id(
        regular_user_tg_bot_id
    )

    if not regular_user:
        await send_text_messages(
            await messages.get_no_object_with_this_id_message(str(role_id)),
            update,
        )

        return

    new_support_user = await SupportUser.add_support_user(
        user.id,
        descriptive_name,
        repo,
        role_id=role_for_user.id,
        addition_time=update.message.date,
    )

    await send_text_messages(
        await messages.get_successful_support_user_addition_message(
            new_support_user, role_for_user
        ),
        update,
    )


async def handle_get_support_user(update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles /getsupuser command
    """
    user = update.effective_user

    messages = get_messages(update.effective_user.language_code)

    repo = RepositoryClass()

    permission_denied = True

    support_user = await repo.get_support_user_by_tg_bot_user_id(user.id)

    if support_user:
        role = await support_user.get_role(repo)

        if (role and role.can_answer_questions) or support_user.is_owner:
            permission_denied = False

    if permission_denied:
        await send_text_messages(
            await messages.get_permission_denied_message(user),
            update,
        )

        return

    if not context.args or not len(context.args) == 1:
        await send_text_messages(
            await messages.get_incorrect_num_of_arguments_message(
                [messages.support_user_id_argument_name]
            ),
            update,
        )

        return

    if not is_string_int(context.args[0]):
        await send_text_messages(
            await messages.get_incorrect_arguments_passed_message(), update
        )

        return

    id = int(context.args[0])

    support_user_for_info = await repo.get_support_user_by_tg_bot_user_id(id)

    if not support_user_for_info:
        await send_text_messages(
            await messages.get_no_object_with_this_id_message(str(id)), update
        )

        return

    await update.message.reply_text(
        messages.get_support_user_info_message(
            support_user_for_info, await support_user_for_info.get_role(repo)
        )
    )


async def handle_get_all_suppurt_users(
    update, context: ContextTypes.DEFAULT_TYPE
):
    """
    Handles /allsupusers command
    """
    user = update.effective_user

    repo = RepositoryClass()

    messages = get_messages(update.effective_user.language_code)

    permission_denied = True

    support_user = await repo.get_support_user_by_tg_bot_user_id(user.id)

    if support_user:
        role = await support_user.get_role(repo)

        if support_user.is_owner or (role and role.can_manage_support_users):
            permission_denied = False

    if permission_denied:
        await send_text_messages(
            await messages.get_permission_denied_message(user),
            update,
        )

        return

    messages = get_messages(update.effective_user.language_code)

    repo = RepositoryClass()

    all_support_users = await repo.get_all_support_users()

    message = await messages.get_all_support_users_list_message(
        all_support_users
    )

    await send_text_messages(message, update)


# QUESTIONS


async def handle_get_question(update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles /question command
    """
    user = update.effective_user

    messages = get_messages(user.language_code)

    repo = RepositoryClass()

    support_user = await repo.get_support_user_by_tg_bot_user_id(user.id)

    permission_denied = True

    if support_user:
        role = await support_user.get_role(repo)

        if (role and role.can_answer_questions) or support_user.is_owner:
            permission_denied = False

    if permission_denied:
        await send_text_messages(
            await messages.get_permission_denied_message(user),
            update,
        )

        return

    if context.args:
        if not is_string_int(context.args[0]):
            await update.message.reply_text(
                messages.get_incorrect_arguments_passed_message()
            )

            return

        id = int(context.args[0])

        question = await repo.get_question_by_tg_message_id(id)

        if not question:
            await send_text_messages(
                await messages.get_no_object_with_this_id_message(str(id)),
                update,
            )

            return

        await send_text_messages(
            await messages.get_question_info_message(
                question,
                await question.get_regular_user_asked(repo),  # type: ignore
            ),
            update,
        )

        return

    question = await repo.get_random_unanswered_unbinded_question()

    if question:
        await send_text_messages(
            await messages.get_question_info_message(
                question,
                await question.get_regular_user_asked(repo),  # type: ignore
            ),
            update,
        )

        return

    await send_text_messages(
        await messages.get_no_unbinded_quetstions_left_message(question),
        update,
    )


async def handle_bind_question(update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles /bind command
    """
    user = update.effective_user

    messages = get_messages(user.language_code)

    repo = RepositoryClass()

    support_user = await repo.get_support_user_by_tg_bot_user_id(user.id)

    if not support_user:
        await send_text_messages(
            await messages.get_permission_denied_message(user), update
        )

        return

    role = await support_user.get_role(repo)

    if not support_user.is_owner and (role and not role.can_answer_questions):
        await send_text_messages(
            await messages.get_permission_denied_message(user), update
        )

    if not context.args or len(context.args) > 1:
        await send_text_messages(
            await messages.get_incorrect_num_of_arguments_message(
                [messages.question_id_argument_name]
            ),
            update,
        )

        return

    if not is_string_int(context.args[0]):
        await send_text_messages(
            await messages.get_incorrect_arguments_passed_message(), update
        )

        return

    id = int(context.args[0])

    question = await repo.get_question_by_tg_message_id(id)

    if question:
        await support_user.bind_question(question.id, repo)

        return

    await send_text_messages(
        await messages.get_no_object_with_this_id_message(user), update
    )


async def handle_unbind_question(update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles /unbind command
    """
    user = update.effective_user

    messages = get_messages(user.language_code)

    repo = RepositoryClass()

    support_user = await repo.get_support_user_by_tg_bot_user_id(user.id)

    if not support_user:
        await send_text_messages(
            await messages.get_permission_denied_message(user), update
        )

        return

    if support_user.current_question_id:
        await support_user.unbind_question(repo)

        await send_text_messages(
            await messages.get_successful_unbinding_message(), update
        )

        return

    await send_text_messages(
        await messages.get_no_binded_question_message(), update
    )


# ANSWERS


async def handle_get_answer(update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles /answer [answerId] command
    """
    user = update.effective_user

    messages = get_messages(user.language_code)

    repo = RepositoryClass()

    support_user = await repo.get_support_user_by_tg_bot_user_id(user.id)

    permission_denied = True

    if support_user:
        role = await support_user.get_role(repo)

        if (role and role.can_answer_questions) or support_user.is_owner:
            permission_denied = False

    if permission_denied:
        await send_text_messages(
            await messages.get_permission_denied_message(user),
            update,
        )

        return

    if not context.args:
        await send_text_messages(
            await messages.get_incorrect_num_of_arguments_message(
                [messages.answer_id_argument_name]
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

    answer = await repo.get_answer_by_tg_bot_user_id(id)

    if not answer:
        await send_text_messages(
            await messages.get_no_object_with_this_id_message(str(id)),
            update,
        )

        return

    await send_text_messages(
        await messages.get_answer_info_message(
            answer,
            await answer.get_support_user(repo),  # type: ignore
            await answer.get_question(repo),  # type: ignore
        ),
        update,
    )

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
        question = await support_user.get_current_question(repo)

        if not question:
            await send_text_messages(
                await messages.get_no_binded_question_message(), update
            )

            return

        regular_user_asked = await question.get_regular_user_asked(repo)

        answer = await support_user.answer_current_question(
            message.text, message.id, repo, answer_date=message.date
        )

        if answer and regular_user_asked:
            try:
                await send_text_messages(
                    await messages.get_answer_for_regular_user_message(
                        answer, question
                    ),
                    update,
                    chat_id=regular_user_asked.tg_bot_user_id,
                    reply_to_message_id=question.tg_message_id,
                )
            except BadRequest:
                await send_text_messages(
                    await messages.get_answer_for_regular_user_message(
                        answer, question, True
                    ),
                    update,
                    chat_id=regular_user_asked.tg_bot_user_id,
                )

            return

    regular_user = await repo.get_regular_user_by_tg_bot_user_id(user.id)

    if regular_user:
        await regular_user.ask_question(
            message.text, message.id, repo, question_date=message.date
        )

    return


async def handle_unsuppported_message_type(
    update, context: ContextTypes.DEFAULT_TYPE
):
    user = update.effective_user

    messages = get_messages(user.language_code)

    await send_text_messages(
        await messages.get_unsupported_message_type_message(), update
    )


async def handle_unknown_command(update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    messages = get_messages(user.language_code)

    await send_text_messages(
        await messages.get_unknown_command_message(), update
    )
