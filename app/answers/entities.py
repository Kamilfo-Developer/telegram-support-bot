from __future__ import annotations
from datetime import datetime
from uuid import uuid4
from typing import Self
from app.errors import AnswerAlreadyEstimatedError
from app.shared.entities import Attachment
from app.shared.value_objects import (
    AnswerIdType,
    QuestionIdType,
    SupportUserIdType,
    TgCaption,
    TgFileIdType,
    TgMessageIdType,
    TgMessageText,
)
from app.utils import TgFileType, IdComparable


class Answer(IdComparable):
    _id: AnswerIdType
    support_user_id: SupportUserIdType
    message: TgMessageText
    tg_message_id: TgMessageIdType
    is_useful: bool | None
    attachments: list[AnswerAttachment]
    date: datetime

    def __init__(
        self,
        id: AnswerIdType,
        support_user_id: SupportUserIdType,
        question_id: QuestionIdType,
        message: TgMessageText,
        tg_message_id: TgMessageIdType,
        attachments: list[AnswerAttachment],
        is_useful: bool | None,
        date: datetime,
    ) -> None:
        """This method should not be called directly.
        Use ```Answer.create(...)``` instead."""

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
        support_user_id: SupportUserIdType,
        question_id: QuestionIdType,
        message: TgMessageText,
        tg_message_id: TgMessageIdType,
    ) -> Self:
        """
        A factory method which creates a new ```Answer``` entity.

        Args:
            support_user_id (SupportUserIdType): id of answering support user
            question_id (QuestionIdType): id of the answered question
            message (TgMessageText): text content of the answer
            tg_message_id (TgMessageIdType): Telegram message id of the answer

        Returns:
            Self: new ```Answer``` entity
        """

        new_answer = cls(
            id=AnswerIdType(uuid4()),
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
        """Estimates the answer as useful.

        Raises:
            AnswerAlreadyEstimatedError: raised
            if the answer was already estimated as useful
        """

        if self.is_useful:
            raise AnswerAlreadyEstimatedError()

        self.is_useful = True

    def estimate_as_unuseful(self) -> None:
        """Estimates the answer as unuseful.

        Raises:
            AnswerAlreadyEstimatedError: raised
            if the answer was already estimated as unuseful
        """
        if self.is_useful is not None and not self.is_useful:
            raise AnswerAlreadyEstimatedError()

        self.is_useful = False

    def add_attachment(
        self,
        tg_file_id: TgFileIdType,
        attachment_type: TgFileType,
        caption: TgCaption | None,
    ) -> None:
        """Adds an attachment to the answer

        Args:
            tg_file_id (TgFileIdType): Telegram file id
            attachment_type (TgFileType): type of the attachment
            caption (TgCaption | None): Telegram caption
        """

        self.attachments.append(
            AnswerAttachment(
                tg_file_id=tg_file_id,
                attachment_type=attachment_type,
                caption=caption,
                date=datetime.utcnow(),
            )
        )


class AnswerAttachment(Attachment):
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
