from bot.localization.messages import Messages
from bot.entities.support_user import SupportUser
from bot.entities.role import Role
from bot.entities.question import Question
from bot.states import States
from bot.markup import Markup
from bot.typing import RepoType
from telegram import User, Message
from datetime import datetime
from bot.utils import MessageToSend
import json


class SupportUserManager:
    def __init__(
        self,
        tg_user: User,
        support_user: SupportUser | None,
        messages: Messages,
        repo: RepoType,
    ):
        self.tg_user = tg_user
        self.support_user = support_user
        self.messages = messages
        self.repo = repo
        self.markup = Markup(messages)

    async def bind_question(
        self, question_tg_message_id: int
    ) -> MessageToSend:
        if self.is_answer_questions_permission_denied():
            return MessageToSend(
                await self.messages.get_permission_denied_message(
                    self.tg_user
                ),
                None,
            )

        question = await self.repo.get_question_by_tg_message_id(
            question_tg_message_id
        )

        if not question:
            return MessageToSend(
                await self.messages.get_no_object_with_this_id_message(
                    str(question_tg_message_id)
                ),
                None,
            )

        await self.support_user.bind_question(question, self.repo)

        return MessageToSend(
            await self.messages.get_successful_binding_message(question), None
        )

    async def unbind_question(self) -> MessageToSend:
        if self.is_answer_questions_permission_denied():
            return MessageToSend(
                await self.messages.get_permission_denied_message(
                    self.tg_user
                ),
                None,
            )

        if not self.support_user.current_question:
            return MessageToSend(
                await self.messages.get_no_binded_question_message(), None
            )

        await self.support_user.unbind_question(self.repo)

        return MessageToSend(
            await self.messages.get_successful_unbinding_message(), None
        )

    async def add_role(
        self,
        role_name: str,
        can_answer_questions: bool,
        can_manage_support_users: bool,
        date: datetime,
    ) -> MessageToSend:
        if self.is_manage_permission_denied():
            return MessageToSend(
                await self.messages.get_permission_denied_message(
                    self.tg_user
                ),
                None,
            )

        role = await self.repo.get_role_by_name(role_name)

        if role:
            return MessageToSend(
                await self.messages.get_role_name_duplicate_message(), None
            )

        new_role = await Role.add_role(
            role_name,
            can_answer_questions,
            can_manage_support_users,
            repo=self.repo,
            adding_date=date,
        )

        return MessageToSend(
            await self.messages.get_successful_role_addition_message(new_role),
            None,
        )

    async def get_role(self, role_id: int) -> MessageToSend:
        if self.is_manage_permission_denied():
            return MessageToSend(
                await self.messages.get_permission_denied_message(
                    self.tg_user
                ),
                None,
            )
        role = await self.repo.get_role_by_id(role_id)

        if not role:
            return MessageToSend(
                await self.messages.get_no_object_with_this_id_message(
                    str(role_id)
                ),
                None,
            )

        return MessageToSend(await self.messages.get_role_info_message(role))

    async def get_all_roles(self) -> MessageToSend:
        if self.is_manage_permission_denied():
            return MessageToSend(
                await self.messages.get_permission_denied_message(
                    self.tg_user
                ),
            )

        roles = await self.repo.get_all_roles()

        return MessageToSend(await self.messages.get_roles_list_message(roles))

    async def delete_role(self, role_id: int):
        if self.is_manage_permission_denied():
            return MessageToSend(
                await self.messages.get_permission_denied_message(
                    self.tg_user
                ),
                None,
            )

        role = await self.repo.get_role_by_id(role_id)

        if not role:
            return MessageToSend(
                await self.messages.get_no_object_with_this_id_message(
                    str(role_id)
                ),
                None,
            )

        await self.repo.delete_role_with_id(role.id)

        return MessageToSend(await self.messages.get_role_info_message(role))

    async def add_support_user(
        self,
        regular_user_tg_bot_id: int,
        role_id: int,
        descriptive_name: str,
        message_date: datetime,
    ) -> MessageToSend:
        if self.is_manage_permission_denied():
            return MessageToSend(
                await self.messages.get_permission_denied_message(
                    self.tg_user
                ),
            )

        role_for_user = await self.repo.get_role_by_id(role_id)

        if not role_for_user:
            return MessageToSend(
                await self.messages.get_no_object_with_this_id_message(
                    str(role_id)
                )
            )

        regular_user = await self.repo.get_regular_user_by_tg_bot_user_id(
            regular_user_tg_bot_id
        )

        if not regular_user:
            return MessageToSend(
                await self.messages.get_no_object_with_this_id_message(
                    str(regular_user_tg_bot_id)
                )
            )

        support_user = await self.repo.get_support_user_by_tg_bot_user_id(
            regular_user.tg_bot_user_id
        )

        if support_user:
            return MessageToSend(
                await self.messages.get_support_user_already_exists_message(
                    support_user
                )
            )

        new_support_user = await SupportUser.add_support_user(
            regular_user.tg_bot_user_id,
            descriptive_name,
            self.repo,
            role=role_for_user,
            addition_time=message_date,
        )

        return MessageToSend(
            await self.messages.get_successful_support_user_addition_message(
                new_support_user
            )
        )

    async def get_support_user(self, support_user_tg_id: int) -> MessageToSend:
        if self.is_manage_permission_denied():
            return MessageToSend(
                await self.messages.get_permission_denied_message(
                    self.tg_user
                ),
            )

        support_user = await self.repo.get_support_user_by_tg_bot_user_id(
            support_user_tg_id
        )

        if not support_user:
            return MessageToSend(
                await self.messages.get_no_object_with_this_id_message(
                    str(support_user_tg_id)
                )
            )

        return MessageToSend(
            await self.messages.get_support_user_info_message(support_user)
        )

    async def get_all_support_users(self) -> MessageToSend:
        if self.is_manage_permission_denied():
            return MessageToSend(
                await self.messages.get_permission_denied_message(
                    self.tg_user
                ),
            )

        all_support_users = await self.repo.get_all_support_users()

        return MessageToSend(
            await self.messages.get_support_users_list_message(
                all_support_users
            )
        )

    async def get_question_by_id(
        self, question_tg_message_id: int
    ) -> MessageToSend:
        if self.is_answer_questions_permission_denied():
            return MessageToSend(
                await self.messages.get_permission_denied_message(
                    self.tg_user
                ),
                None,
            )

        question = await self.repo.get_question_by_tg_message_id(
            question_tg_message_id
        )

        if not question:
            return MessageToSend(
                await self.messages.get_no_object_with_this_id_message(
                    str(question_tg_message_id)
                )
            )

        return MessageToSend(
            await self.messages.get_question_info_message(question),
            self.markup.get_question_binding_buttons_markup(
                json.dumps(
                    {
                        "question_tg_message_id": question.tg_message_id,
                        "action": States.BIND_ACTION,
                    }
                ),
                json.dumps(
                    {
                        "question_tg_message_id": question.tg_message_id,
                        "action": States.UNBIND_ACTION,
                    }
                ),
            ),
        )

    async def get_random_unanswered_question(self) -> MessageToSend:
        if self.is_answer_questions_permission_denied():
            return MessageToSend(
                await self.messages.get_permission_denied_message(
                    self.tg_user
                ),
                None,
            )

        question = await self.repo.get_random_unanswered_unbinded_question()

        if not question:
            return MessageToSend(
                await self.messages.get_no_unbinded_quetstions_left_message()
            )

        return MessageToSend(
            await self.messages.get_question_info_message(question),
            self.markup.get_question_binding_buttons_markup(
                json.dumps(
                    {
                        "id": question.tg_message_id,
                        "action": States.BIND_ACTION,
                    }
                ),
                json.dumps(
                    {
                        "id": question.tg_message_id,
                        "action": States.UNBIND_ACTION,
                    }
                ),
            ),
        )

    async def get_answer_by_id(
        self, answer_tg_message_id: int
    ) -> MessageToSend:
        if self.is_answer_questions_permission_denied():
            return MessageToSend(
                await self.messages.get_permission_denied_message(
                    self.tg_user
                ),
                None,
            )

        answer = await self.repo.get_answer_by_tg_message_id(
            answer_tg_message_id
        )

        if not answer:
            return MessageToSend(
                await self.messages.get_no_object_with_this_id_message(
                    str(answer_tg_message_id)
                )
            )

        return MessageToSend(
            await self.messages.get_answer_info_message(answer)
        )

    async def get_question_answers(
        self, question_tg_message_id: int
    ) -> MessageToSend:
        question = await self.repo.get_question_by_tg_message_id(
            question_tg_message_id
        )

        if not question:
            return MessageToSend(
                await self.messages.get_no_object_with_this_id_message(
                    str(question_tg_message_id)
                )
            )

        answers = await self.repo.get_answers_with_question_id(
            question_id=question.id
        )

        return MessageToSend(
            await self.messages.get_answers_list_message(answers)
        )

    async def activate_support_user(
        self, support_user_tg_id: int
    ) -> MessageToSend:
        if self.is_manage_permission_denied():
            return MessageToSend(
                await self.messages.get_permission_denied_message(
                    self.tg_user
                ),
                None,
            )

        support_user = await self.repo.get_support_user_by_tg_bot_user_id(
            support_user_tg_id
        )

        if not support_user:
            return MessageToSend(
                await self.messages.get_no_object_with_this_id_message(
                    str(support_user_tg_id)
                )
            )

        await support_user.activate(self.repo)

        return MessageToSend(
            await self.messages.get_support_user_activation_message(
                support_user
            )
        )

    async def deactivate_support_user(
        self, support_user_tg_id: int
    ) -> MessageToSend:
        if self.is_manage_permission_denied():
            return MessageToSend(
                await self.messages.get_permission_denied_message(
                    self.tg_user
                ),
                None,
            )

        support_user = await self.repo.get_support_user_by_tg_bot_user_id(
            support_user_tg_id
        )

        if not support_user:
            return MessageToSend(
                await self.messages.get_no_object_with_this_id_message(
                    str(support_user_tg_id)
                )
            )

        await support_user.activate(self.repo)

        return MessageToSend(
            await self.messages.get_support_user_activation_message(
                support_user
            )
        )

    async def answer_binded_question(
        self, answer_text: str, message_id: int, message_date: datetime
    ) -> tuple[MessageToSend | None, MessageToSend | None]:
        if self.is_answer_questions_permission_denied():
            return (
                MessageToSend(
                    await self.messages.get_permission_denied_message(
                        self.tg_user
                    )
                ),
                None,
            )

        question = self.support_user.current_question

        if not question:
            return (
                MessageToSend(
                    await self.messages.get_no_binded_question_message(
                        self.tg_user
                    )
                ),
                None,
            )

        answer = await self.support_user.answer_current_question(
            answer_text, message_id, self.repo, answer_date=message_date
        )

        return (
            MessageToSend(
                await self.messages.get_successful_answering_message(
                    question, answer
                )
            ),
            MessageToSend(
                await self.messages.get_answer_for_regular_user_message(
                    answer
                ),
                chat_id=question.regular_user.tg_bot_user_id,
                reply_to=question.tg_message_id,
                markup=self.markup.get_answer_estimation_buttons_markup(
                    json.dumps(
                        {
                            "id": answer.tg_message_id,
                            "action": States.ESTIMATE_AS_USEFUL_ACTION,
                        }
                    ),
                    json.dumps(
                        {
                            "id": answer.tg_message_id,
                            "action": States.ESTIMATE_AS_UNUSEFUL_ACTION,
                        }
                    ),
                ),
            ),
        )

    def is_manage_permission_denied(self) -> bool:
        support_user = self.support_user

        if (
            not support_user
            or not support_user.is_active
            or not (
                (
                    support_user.role
                    and support_user.role.can_manage_support_users
                )
                and not support_user.is_owner
            )
        ):

            return True

        return False

    def is_answer_questions_permission_denied(
        self,
    ) -> bool:
        support_user = self.support_user

        if (
            not support_user
            or not support_user.is_active
            or not (
                (
                    support_user.role
                    and support_user.role.can_manage_support_users
                )
                and not support_user.is_owner
            )
        ):

            return True

        return False
