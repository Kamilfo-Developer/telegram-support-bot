from __future__ import annotations

from datetime import datetime
from typing import Self
from uuid import uuid4
from app.shared.entities import Attachment
from app.utils import TgFileType, IdComparable


from app.shared.value_objects import (
    QuestionIdType,
    RegularUserIdType,
    TgCaption,
    TgFileIdType,
    TgMessageIdType,
    TgMessageText,
)


class QuestionAttachment(Attachment):
    tg_file_id: TgFileIdType

    attachment_type: TgFileType

    caption: TgCaption | None

    date: datetime

    def __init__(
        self,
        tg_file_id: TgFileIdType,
        attachment_type: TgFileType,
        caption: TgCaption | None = None,
        date: datetime = datetime.now(),
    ) -> None:
        self.tg_file_id = tg_file_id
        self.attachment_type = attachment_type
        self.caption = caption
        self.date = date


class Question(IdComparable):
    _id: QuestionIdType

    regular_user_id: RegularUserIdType

    message: TgMessageText

    tg_message_id: TgMessageIdType

    date: datetime

    def __init__(
        self,
        id: QuestionIdType,
        regular_user_id: RegularUserIdType,
        message: TgMessageText,
        tg_message_id: TgMessageIdType,
        attachments: list[QuestionAttachment],
        date: datetime,
    ) -> None:
        """This method should not be called directly.
        Use ```Question.create(...)``` instead."""

        self._id = id
        self.regular_user_id = regular_user_id
        self.message = message
        self.tg_message_id = tg_message_id
        self.attachments = attachments
        self.date = date

    def add_attachment(
        self,
        tg_file_id: TgFileIdType,
        attachment_type: TgFileType,
        caption: TgCaption | None,
    ) -> None:
        """Adds an attachment to the question

        Args:
            tg_file_id (TgFileIdType): Telegram file id
            attachment_type (TgFileType): type of the attachment
            caption (TgCaption | None): Telegram caption
        """

        self.attachments.append(
            QuestionAttachment(
                tg_file_id=tg_file_id,
                attachment_type=attachment_type,
                caption=caption,
                date=datetime.utcnow(),
            )
        )

    @classmethod
    def create(
        cls,
        regular_user_id: RegularUserIdType,
        message: TgMessageText,
        tg_message_id: TgMessageIdType,
    ) -> Self:
        """A factory method which creates a new ```Question``` entity.

        Args:
            regular_user_id (RegularUserIdType): id of the asking regular user
            message (TgMessageText): text content of the question
            tg_message_id (TgMessageIdType): Telegram message
            id of the question

        Returns:
            Self: new ```Question``` entity
        """

        new_question = cls(
            id=QuestionIdType(uuid4()),
            regular_user_id=regular_user_id,
            message=message,
            tg_message_id=tg_message_id,
            attachments=[],
            date=datetime.now(),
        )

        return new_question
