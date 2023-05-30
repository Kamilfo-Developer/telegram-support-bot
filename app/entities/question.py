from __future__ import annotations
from datetime import datetime
from uuid import UUID, uuid4
from app.entities.attachments import Attachment
from app.entities.attachments import QuestionAttachment
from app.utils import (
    IdComparable,
    AttachmentType,
    TgCaption,
    TgFileIdType,
    TgMessageIdType,
    TgMessageText,
)

from typing import TYPE_CHECKING, Self

if TYPE_CHECKING:
    from app.entities.answer import Answer
    from app.entities.regular_user import RegularUser


class Question(IdComparable):
    _id: UUID

    regular_user_id: UUID

    message: TgMessageText

    tg_message_id: TgMessageIdType

    date: datetime

    def __init__(
        self,
        id: UUID,
        regular_user_id: UUID,
        message: TgMessageText,
        tg_message_id: TgMessageIdType,
        attachments: list[QuestionAttachment],
        date: datetime,
    ) -> None:
        self._id = id
        self.regular_user_id = regular_user_id
        self.message = message
        self.tg_message_id = tg_message_id
        self.attachments = attachments
        self.date = date

    async def add_attachment(
        self,
        tg_file_id: TgFileIdType,
        attachment_type: AttachmentType,
        caption: TgCaption,
    ) -> None:
        self.attachments.append(
            QuestionAttachment(
                tg_file_id,
                question_id=self.id,
                attachment_type=attachment_type,
                caption=caption,
                date=datetime.utcnow(),
            )
        )

    @classmethod
    def create(
        cls,
        regular_user_id: UUID,
        message: TgMessageText,
        tg_message_id: TgMessageIdType,
    ) -> Self:
        new_question = cls(
            id=uuid4(),
            regular_user_id=regular_user_id,
            message=message,
            tg_message_id=tg_message_id,
            attachments=[],
            date=datetime.now(),
        )

        return new_question
