from datetime import datetime
from uuid import UUID
from app.utils import (
    TgCaption,
    IdComparable,
    AttachmentType,
    TgFileIdType,
)
import abc


class Attachment(abc.ABC):
    tg_file_id: TgFileIdType

    attachment_type: AttachmentType

    caption: TgCaption | None

    date: datetime


class QuestionAttachment(Attachment, IdComparable):
    tg_file_id: TgFileIdType

    question_id: UUID

    attachment_type: AttachmentType

    caption: TgCaption | None

    date: datetime

    def __init__(
        self,
        tg_file_id: TgFileIdType,
        question_id: UUID,
        attachment_type: AttachmentType,
        caption: TgCaption | None = None,
        date: datetime = datetime.now(),
    ) -> None:
        self.tg_file_id = tg_file_id
        self.question_id = question_id
        self.attachment_type = attachment_type
        self.caption = caption
        self.date = date


class AnswerAttachment(Attachment, IdComparable):
    tg_file_id: TgFileIdType

    answer_id: UUID

    attachment_type: AttachmentType

    caption: TgCaption | None

    date: datetime

    def __init__(
        self,
        tg_file_id: TgFileIdType,
        answer_id: UUID,
        attachment_type: AttachmentType,
        caption: TgCaption | None = None,
        date: datetime = datetime.now(),
    ) -> None:
        self.tg_file_id = tg_file_id
        self.answer_id = answer_id
        self.attachment_type = attachment_type
        self.caption = caption
        self.date = date
