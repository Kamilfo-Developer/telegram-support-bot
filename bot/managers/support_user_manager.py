from bot.localization.messages_content import MessagesContent
from bot.entities.support_user import SupportUser
from bot.entities.role import Role, RolePermissions
from bot.entities.question import Question
from bot.entities.attachment import Attachment
from bot.states import States
from bot.markup import Markup
from bot.typing import Repo
from telegram import User
from datetime import datetime
from bot.utils import (
    AttachmentType,
)
from bot.bot_messages import (
    MessageToSend,
    TextToSend,
    get_file_to_send_from_attachment_entity,
)
from bot.services.statistics import GlobalStatistics

import json


class SupportUserManager:
    def __init__(
        self,
        tg_user: User,
        support_user: SupportUser | None,
        messages_content: MessagesContent,
        repo: Repo,
    ):
        self.tg_user = tg_user
        self.support_user = support_user
        self.msgs = messages_content
        self.repo = repo
        self.markup = Markup(messages_content)

    async def get_global_statistics(self) -> list[MessageToSend]:
        if self.is_manage_permission_denied():
            return [
                TextToSend(
                    await self.msgs.get_permission_denied_message(self.tg_user)
                )
            ]

        global_statistics = await GlobalStatistics.get_statistics(self.repo)

        return [
            TextToSend(
                await self.msgs.get_global_statistics_message(
                    global_statistics
                )
            )
        ]

    async def get_regular_user_info(self, tg_id: int) -> list[MessageToSend]:
        if self.is_answer_questions_permission_denied():
            return [
                TextToSend(
                    await self.msgs.get_permission_denied_message(self.tg_user)
                )
            ]

        regular_user = await self.repo.get_regular_user_by_tg_bot_user_id(
            tg_id
        )

        if not regular_user:
            return [
                TextToSend(
                    await self.msgs.get_no_object_with_this_id_message(
                        str(tg_id)
                    )
                )
            ]

        return [
            TextToSend(
                await self.msgs.get_regular_user_info_message(
                    regular_user, await regular_user.get_statistics(self.repo)
                )
            )
        ]

    async def bind_question(
        self, question_tg_message_id: int
    ) -> list[MessageToSend]:
        if self.is_answer_questions_permission_denied():
            return [
                TextToSend(
                    await self.msgs.get_permission_denied_message(self.tg_user)
                )
            ]

        question = await self.repo.get_question_by_tg_message_id(
            question_tg_message_id
        )

        if not question:
            return [
                TextToSend(
                    await self.msgs.get_no_object_with_this_id_message(
                        str(question_tg_message_id)
                    )
                )
            ]

        await self.support_user.bind_question(question, self.repo)  # type: ignore

        return [
            TextToSend(
                await self.msgs.get_successful_binding_message(question)
            )
        ]

    async def unbind_question(self) -> list[MessageToSend]:
        if self.is_answer_questions_permission_denied():
            return [
                TextToSend(
                    await self.msgs.get_permission_denied_message(self.tg_user)
                )
            ]

        if not self.support_user.current_question:  # type: ignore
            return [
                TextToSend(await self.msgs.get_no_binded_question_message())
            ]

        await self.support_user.unbind_question(self.repo)  # type: ignore

        return [TextToSend(await self.msgs.get_successful_unbinding_message())]

    async def add_role(
        self,
        role_name: str,
        can_answer_questions: bool,
        can_manage_support_users: bool,
        date: datetime,
    ) -> list[MessageToSend]:
        if self.is_manage_permission_denied():
            return [
                TextToSend(
                    await self.msgs.get_permission_denied_message(self.tg_user)
                )
            ]

        role = await self.repo.get_role_by_name(role_name)

        if role:
            return [
                TextToSend(await self.msgs.get_role_name_duplicate_message())
            ]

        new_role = await Role.add_role(
            role_name,
            RolePermissions(can_answer_questions, can_manage_support_users),
            repo=self.repo,
            adding_date=date,
        )

        return [
            TextToSend(
                await self.msgs.get_successful_role_addition_message(new_role)
            )
        ]

    async def get_role(self, role_id: int) -> list[MessageToSend]:
        if self.is_manage_permission_denied():
            return [
                TextToSend(
                    await self.msgs.get_permission_denied_message(self.tg_user)
                )
            ]

        role = await self.repo.get_role_by_id(role_id)

        if not role:
            return [
                TextToSend(
                    await self.msgs.get_no_object_with_this_id_message(
                        str(role_id)
                    )
                )
            ]

        return [
            TextToSend(
                await self.msgs.get_role_info_message(
                    role, await role.get_statistics(self.repo)
                )
            )
        ]

    async def get_all_roles(self) -> list[MessageToSend]:
        if self.is_manage_permission_denied():
            return [
                TextToSend(
                    await self.msgs.get_permission_denied_message(self.tg_user)
                )
            ]

        roles = await self.repo.get_all_roles()

        return [TextToSend(await self.msgs.get_roles_list_message(roles))]

    async def delete_role(self, role_id: int) -> list[MessageToSend]:
        if self.is_manage_permission_denied():
            return [
                TextToSend(
                    await self.msgs.get_permission_denied_message(self.tg_user)
                )
            ]

        role = await self.repo.get_role_by_id(role_id)

        if not role:
            return [
                TextToSend(
                    await self.msgs.get_no_object_with_this_id_message(
                        str(role_id)
                    )
                )
            ]

        await self.repo.delete_role_with_id(role.id)

        return [
            TextToSend(
                await self.msgs.get_role_info_message(
                    role, await role.get_statistics(self.repo)
                )
            )
        ]

    async def add_support_user(
        self,
        regular_user_tg_bot_id: int,
        role_id: int,
        descriptive_name: str,
        message_date: datetime,
    ) -> list[MessageToSend]:
        if self.is_manage_permission_denied():
            return [
                TextToSend(
                    await self.msgs.get_permission_denied_message(self.tg_user)
                )
            ]

        role_for_user = await self.repo.get_role_by_id(role_id)

        if not role_for_user:
            return [
                TextToSend(
                    await self.msgs.get_no_object_with_this_id_message(
                        str(role_id)
                    )
                )
            ]

        regular_user = await self.repo.get_regular_user_by_tg_bot_user_id(
            regular_user_tg_bot_id
        )

        if not regular_user:
            return [
                TextToSend(
                    await self.msgs.get_no_object_with_this_id_message(
                        str(regular_user_tg_bot_id)
                    )
                )
            ]

        support_user = await self.repo.get_support_user_by_tg_bot_user_id(
            regular_user.tg_bot_user_id
        )

        if support_user:
            return [
                TextToSend(
                    await self.msgs.get_support_user_already_exists_message(
                        support_user
                    )
                )
            ]

        new_support_user = await SupportUser.add_support_user(
            regular_user.tg_bot_user_id,
            descriptive_name,
            self.repo,
            role=role_for_user,
            addition_time=message_date,
        )

        return [
            TextToSend(
                await self.msgs.get_successful_support_user_addition_message(
                    new_support_user
                )
            )
        ]

    async def get_support_user(
        self, support_user_tg_id: int
    ) -> list[MessageToSend]:
        if self.is_manage_permission_denied():
            return [
                TextToSend(
                    await self.msgs.get_permission_denied_message(
                        self.tg_user
                    ),
                )
            ]

        support_user = await self.repo.get_support_user_by_tg_bot_user_id(
            support_user_tg_id
        )

        if not support_user:
            return [
                TextToSend(
                    await self.msgs.get_no_object_with_this_id_message(
                        str(support_user_tg_id)
                    )
                )
            ]

        return [
            TextToSend(
                await self.msgs.get_support_user_info_message(
                    support_user, await support_user.get_statistics(self.repo)
                )
            )
        ]

    async def get_all_support_users(self) -> list[MessageToSend]:
        if self.is_manage_permission_denied():
            return [
                TextToSend(
                    await self.msgs.get_permission_denied_message(
                        self.tg_user
                    ),
                )
            ]

        all_support_users = await self.repo.get_all_support_users()

        return [
            TextToSend(
                await self.msgs.get_support_users_list_message(
                    all_support_users
                )
            )
        ]

    async def get_question_by_id(
        self, question_tg_message_id: int
    ) -> list[MessageToSend]:
        if self.is_answer_questions_permission_denied():
            return [
                TextToSend(
                    await self.msgs.get_permission_denied_message(self.tg_user)
                )
            ]

        question = await self.repo.get_question_by_tg_message_id(
            question_tg_message_id
        )

        if not question:
            return [
                TextToSend(
                    await self.msgs.get_no_object_with_this_id_message(
                        str(question_tg_message_id)
                    )
                )
            ]

        return [
            TextToSend(
                await self.msgs.get_question_info_message(
                    question, await question.get_statistics(self.repo)
                ),
                # JSON used here to pass an object as the callback data
                self.markup.get_question_info_buttons_markup(
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
                    json.dumps(
                        {
                            "id": question.tg_message_id,
                            "action": States.SHOW_ATTACHMENTS_ACTION,
                        }
                    ),
                ),
            )
        ]

    async def get_random_unanswered_question(self) -> list[MessageToSend]:
        if self.is_answer_questions_permission_denied():
            return [
                TextToSend(
                    await self.msgs.get_permission_denied_message(self.tg_user)
                )
            ]

        question = await self.repo.get_random_unanswered_unbinded_question()

        if not question:
            return [
                TextToSend(
                    await self.msgs.get_no_unbinded_quetstions_left_message()
                )
            ]

        return [
            TextToSend(
                await self.msgs.get_question_info_message(
                    question, await question.get_statistics(self.repo)
                ),
                self.markup.get_question_info_buttons_markup(
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
                    json.dumps(
                        {
                            "id": question.tg_message_id,
                            "action": States.SHOW_ATTACHMENTS_ACTION,
                        }
                    ),
                ),
            )
        ]

    async def get_answer_by_id(
        self, answer_tg_message_id: int
    ) -> list[MessageToSend]:
        if self.is_answer_questions_permission_denied():
            return [
                TextToSend(
                    await self.msgs.get_permission_denied_message(self.tg_user)
                )
            ]

        answer = await self.repo.get_answer_by_tg_message_id(
            answer_tg_message_id
        )

        if not answer:
            return [
                TextToSend(
                    await self.msgs.get_no_object_with_this_id_message(
                        str(answer_tg_message_id)
                    )
                )
            ]

        return [
            TextToSend(
                await self.msgs.get_answer_info_message(
                    answer, await answer.get_statistics(self.repo)
                )
            )
        ]

    async def get_question_answers(
        self, question_tg_message_id: int
    ) -> list[MessageToSend]:
        if self.is_answer_questions_permission_denied():
            return [
                TextToSend(
                    await self.msgs.get_permission_denied_message(self.tg_user)
                )
            ]

        question = await self.repo.get_question_by_tg_message_id(
            question_tg_message_id
        )

        if not question:
            return [
                TextToSend(
                    await self.msgs.get_no_object_with_this_id_message(
                        str(question_tg_message_id)
                    )
                )
            ]

        answers = await self.repo.get_answers_with_question_id(
            question_id=question.id
        )

        return [TextToSend(await self.msgs.get_answers_list_message(answers))]

    async def activate_support_user(
        self, support_user_tg_id: int
    ) -> list[MessageToSend]:
        if self.is_manage_permission_denied():
            return [
                TextToSend(
                    await self.msgs.get_permission_denied_message(self.tg_user)
                )
            ]

        support_user = await self.repo.get_support_user_by_tg_bot_user_id(
            support_user_tg_id
        )

        if not support_user:
            return [
                TextToSend(
                    await self.msgs.get_no_object_with_this_id_message(
                        str(support_user_tg_id)
                    )
                )
            ]

        await support_user.activate(self.repo)

        return [
            TextToSend(
                await self.msgs.get_support_user_activation_message(
                    support_user
                )
            )
        ]

    async def deactivate_support_user(
        self, support_user_tg_id: int
    ) -> list[MessageToSend]:
        if self.is_manage_permission_denied():
            return [
                TextToSend(
                    await self.msgs.get_permission_denied_message(self.tg_user)
                )
            ]

        support_user = await self.repo.get_support_user_by_tg_bot_user_id(
            support_user_tg_id
        )

        if not support_user:
            return [
                TextToSend(
                    await self.msgs.get_no_object_with_this_id_message(
                        str(support_user_tg_id)
                    )
                )
            ]

        await support_user.deactivate(self.repo)

        return [
            TextToSend(
                await self.msgs.get_support_user_deactivation_message(
                    support_user
                )
            )
        ]

    async def answer_binded_question(
        self, answer_text: str, message_id: int, message_date: datetime
    ) -> list[MessageToSend]:
        if self.is_answer_questions_permission_denied():
            return [
                TextToSend(
                    await self.msgs.get_permission_denied_message(self.tg_user)
                )
            ]

        question = self.support_user.current_question  # type: ignore

        if not question:
            return [
                TextToSend(await self.msgs.get_no_binded_question_message())
            ]

        answer = await self.support_user.answer_current_question(  # type: ignore
            answer_text, message_id, self.repo, answer_date=message_date
        )

        if not answer:
            return [
                TextToSend(await self.msgs.get_no_binded_question_message())
            ]

        return [
            TextToSend(
                await self.msgs.get_successful_answering_message(
                    question, answer
                )
            ),
            TextToSend(
                await self.msgs.get_answer_for_regular_user_message(answer),
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
        ]

    async def add_attachment_to_last_answer(
        self, tg_file_id: str, attachment_type: AttachmentType, date: datetime
    ) -> list[MessageToSend]:
        if self.is_answer_questions_permission_denied():
            return [
                TextToSend(
                    await self.msgs.get_permission_denied_message(self.tg_user)
                )
            ]

        if not self.support_user.current_question:
            return [
                TextToSend(await self.msgs.get_no_binded_question_message())
            ]

        last_answer = await self.repo.get_question_last_answer(
            self.support_user.current_question.id
        )

        if not last_answer:
            return [
                TextToSend(
                    await self.msgs.get_no_last_answer_message(
                        self.support_user
                    )
                )
            ]

        if (
            not self.support_user.current_question
            or self.support_user.current_question != last_answer.question
        ):
            return [
                TextToSend(await self.msgs.get_no_binded_question_message())
            ]

        attachment = await last_answer.add_attachment(
            tg_file_id, attachment_type, date, self.repo
        )

        message_for_support_user = TextToSend(
            await self.msgs.get_answer_attachment_addition_message(
                self.support_user
            )
        )

        message_for_regular_user = get_file_to_send_from_attachment_entity(
            attachment,
            chat_id=last_answer.question.regular_user.tg_bot_user_id,
            reply_to=last_answer.question.tg_message_id,
        )

        return [message_for_support_user, message_for_regular_user]

    async def get_attachments_for_question(
        self, question_tg_message_id: int
    ) -> list[MessageToSend]:
        if self.is_answer_questions_permission_denied():
            return [
                TextToSend(
                    await self.msgs.get_permission_denied_message(self.tg_user)
                )
            ]

        question = await self.repo.get_question_by_tg_message_id(
            question_tg_message_id
        )

        if not question:
            return [
                TextToSend(
                    await self.msgs.get_unavailable_or_deleted_object_message()
                )
            ]

        attachments = await question.get_attachments(self.repo)

        if not attachments:
            return [
                TextToSend(
                    await self.msgs.get_no_question_attachments_message(
                        question
                    )
                )
            ]

        return list(
            map(
                lambda x: get_file_to_send_from_attachment_entity(x),
                attachments,
            )
        )

    def is_manage_permission_denied(self) -> bool:
        support_user = self.support_user

        return not (
            (support_user and support_user.is_active)
            and (
                support_user.is_owner
                or (
                    support_user.role
                    and support_user.role.permissions.can_manage_support_users
                )
            )
        )

    def is_answer_questions_permission_denied(
        self,
    ) -> bool:
        support_user = self.support_user

        return not (
            (support_user and support_user.is_active)
            and (
                support_user.is_owner
                or (
                    support_user.role
                    and support_user.role.permissions.can_answer_questions
                )
            )
        )
