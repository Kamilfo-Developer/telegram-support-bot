from bot.entities.regular_user import RegularUser
from bot.settings import RepositoryClass
from bot.entities.support_user import SupportUser
from bot.entities.question import Question
from bot.entities.role import Role
from bot.localization.get_messages import get_messages
from bot.utils import send_text_messages
from bot.settings import (
    OWNER_ID,
    OWNER_DEFAULT_ROLE_NAME,
    OWNER_DEFAULT_ROLE_DESCRIPTION,
    OWNER_DEFAULT_DESCRIPTIVE_NAME,
)
from telegram import Update


async def handle_start(update, context):
    """
    Handles /start command
    """

    user = update.effective_user
    repo = RepositoryClass()

    messages = get_messages(user.language_code)

    regular_user = await repo.get_regular_user_by_tg_bot_user_id(user.id)

    if user.id == OWNER_ID:

        print("hello")
        start_messages = await messages.get_owner_start_message(user)

        await send_text_messages(start_messages, update)

        return

    if regular_user:
        start_messages = await messages.get_start_reg_user_message(
            user, regular_user
        )

        await send_text_messages(start_messages, update)

        return

    support_user = await repo.get_support_user_by_tg_bot_user_id(user.id)

    if support_user:
        start_messages = await messages.get_start_sup_user_message(
            user, support_user
        )

        await send_text_messages(start_messages, update)

        return


async def handle_init_owner(update, context):
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

    if support_user.is_owner:
        start_messages = await messages.get_already_inited_owner_message(
            user, support_user
        )

        await send_text_messages(start_messages, update)

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


async def handle_get_id(update, context):
    """
    Handles /getid command
    """
    messages = get_messages(update.effective_user.language_code)

    get_id_messages = await messages.get_id_message(update.effective_user.id)

    await send_text_messages(get_id_messages, update)


async def handle_get_support_user(update, context):
    """
    Handles /getsupuser command
    """
    messages = get_messages(update.effective_user.language_code)

    repo = RepositoryClass()

    try:
        id = int(context.args[0])

    except ValueError:
        await update.message.reply_text(messages.get_incorrect_id_message())

        return

    support_user = await repo.get_support_user_by_tg_bot_user_id(id)

    await update.message.reply_text(
        messages.get_support_user_info_message(
            update.effective_user, await support_user.get_role(repo)
        )
    )


async def handle_get_all_suppurt_users(update, context):
    """
    Handles /getallsupusers command
    """
    messages = get_messages(update.effective_user.language_code)

    repo = RepositoryClass()

    all_support_users = await repo.get_all_support_users()

    message = await messages.get_all_support_users_list_message(
        all_support_users
    )

    await send_text_messages(message, update)


async def handle_get_question(update, context):
    """
    Handles /getquestion command
    """
    user = update.effective_user

    messages = get_messages(user.language_code)

    repo = RepositoryClass()

    sup_user = await repo.get_support_user_by_tg_bot_user_id(user.id)

    if not sup_user:
        await send_text_messages(
            await messages.get_permission_denied_message(user),
            update,
        )

        return

    role = await sup_user.get_role(repo)

    if not role or not role.can_answer_questions:
        await send_text_messages(
            await messages.get_permission_denied_message(user),
            update,
        )

        return

    if context.args:
        try:
            id = int(context.args[0])
        except ValueError:
            await update.message.reply_text(
                messages.get_incorrect_id_message()
            )

            return

        question = await repo.get_question_by_tg_message_id(id)

    else:
        question = await repo.get_random_unbinded_question()

    await sup_user.bind_question(question.id, repo)

    await send_text_messages(
        await messages.get_question_info_message(
            question, await question.get_regular_user_asked(repo)
        ),
        update,
    )


async def handle_unbind_question(update, context):
    """
    Handles /unbindquestion command
    """
    user = update.effective_user

    messages = get_messages(user.language_code)

    repo = RepositoryClass()

    support_user = await repo.get_support_user_by_tg_bot_user_id(user.id)

    if support_user.current_question_id:
        await support_user.unbind_question(repo)

        await send_text_messages(
            await messages.get_successful_unbinding_message(), update
        )

        return

    await send_text_messages(
        await messages.get_no_binded_question_message(), update
    )


async def handle_message(update: Update, context):
    """
    Handles all text messages
    """
    user = update.effective_user

    messages = get_messages(user.language_code)

    repo = RepositoryClass()

    message = update.message

    regular_user = await repo.get_regular_user_by_tg_bot_user_id(user.id)

    if regular_user:
        await regular_user.ask_question(message.text, message.id, repo)

        return

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
            message.text, message.id, repo
        )

        if answer:
            await send_text_messages(
                await messages.get_answer_info_message(answer, question),
                update,
                chat_id=regular_user_asked.tg_bot_user_id,
            )

        return


async def handle_unsuppported_message_type(update, context):
    user = update.effective_user

    messages = get_messages(user.language_code)

    await send_text_messages(
        await messages.get_unsupported_message_type_message(), update
    )
