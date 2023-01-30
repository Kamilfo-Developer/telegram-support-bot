from __future__ import annotations
from datetime import datetime
from uuid import UUID
from bot.typing import Repo
from bot.utils import IdComparable, AttachmentType
from bot.entities.attachment import Attachment

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bot.entities.answer import Answer


class AnswerAttachment(Attachment, IdComparable):
    id: UUID

    answer_id: UUID

    tg_file_id: str

    attachment_type: AttachmentType

    date: datetime

    def __init__(
        self,
        id: UUID,
        answer_id: UUID,
        tg_file_id: str,
        attachment_type: AttachmentType,
        date: datetime = datetime.now(),
    ):
        self.id = id
        self.answer_id = answer_id
        self.tg_file_id = tg_file_id
        self.attachment_type = attachment_type
        self.date = date

    async def get_answer(self, repo: Repo) -> Answer | None:
        return await repo.get_answer_by_id(self.answer_id)
