from __future__ import annotations
from datetime import datetime
from uuid import UUID, uuid4
from typing import TYPE_CHECKING, Self
from app.utils import (
    IdComparable,
    AttachmentType,
    TgCaption,
    TgFileIdType,
    TgMessageIdType,
    TgMessageText,
)
from app.entities.attachments import AnswerAttachment


if TYPE_CHECKING:
    from app.entities.question import Question
    from app.entities.support_user import SupportUser


class Answer(IdComparable):
    id: UUID
    support_user: SupportUser
    question: Question
    message: TgMessageText
    tg_message_id: TgMessageIdType
    is_useful: bool | None
    attachments: list[AnswerAttachment]
    date: datetime

    def __init__(
        self,
        id: UUID,
        support_user_id: UUID,
        question_id: UUID,
        message: TgMessageText,
        tg_message_id: TgMessageIdType,
        attachments: list[AnswerAttachment],
        is_useful: bool | None,
        date: datetime,
    ) -> None:
        self._id = id
        self.support_user_id = support_user_id
        self.question_id = question_id
        self.message = message
        self.tg_message_id = tg_message_id
        self.is_useful = is_useful
        self.attachments = attachments
        self.date = date

    @classmethod
    def create(
        cls,
        support_user_id: UUID,
        question_id: UUID,
        message: TgMessageText,
        tg_message_id: TgMessageIdType,
    ) -> Self:
        new_answer = cls(
            id=uuid4(),
            support_user_id=support_user_id,
            question_id=question_id,
            message=message,
            tg_message_id=tg_message_id,
            attachments=[],
            is_useful=None,
            date=datetime.now(),
        )

        return new_answer

    def estimate_as_useful(self) -> None:
        self.is_useful = True

    def estimate_as_unuseful(self) -> None:
        self.is_useful = False

    def add_attachment(
        self,
        tg_file_id: TgFileIdType,
        attachment_type: AttachmentType,
        caption: TgCaption,
    ) -> None:
        self.attachments.append(
            AnswerAttachment(
                tg_file_id=tg_file_id,
                answer_id=self.id,
                attachment_type=attachment_type,
                caption=caption,
                date=datetime.utcnow(),
            )
        )
