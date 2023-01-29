from __future__ import annotations
from datetime import datetime
from uuid import UUID
from bot.typing import RepoType
from bot.utils import IdComparable, AttachmentType
from bot.entities.attachment import Attachment

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bot.entities.question import Question


class QuestionAttachment(Attachment, IdComparable):
    id: UUID

    question_id: UUID

    tg_file_id: str

    attachment_type: AttachmentType

    date: datetime

    def __init__(
        self,
        id: UUID,
        question_id: UUID,
        tg_file_id: str,
        attachment_type: AttachmentType,
        date: datetime = datetime.now(),
    ):
        self.id = id
        self.question_id = question_id
        self.tg_file_id = tg_file_id
        self.attachment_type = attachment_type
        self.date = date

    async def get_question(self, repo: RepoType) -> Question | None:
        return await repo.get_question_by_id(self.question_id)
