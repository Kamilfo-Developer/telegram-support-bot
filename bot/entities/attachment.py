from datetime import datetime
from uuid import UUID
from bot.utils import AttachmentType
import abc


class Attachment(abc.ABC):
    id: UUID

    tg_file_id: str

    attachment_type: AttachmentType

    caption: str | None

    date: datetime
