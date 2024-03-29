from __future__ import annotations
from datetime import datetime
from uuid import UUID, uuid4
from typing import TYPE_CHECKING
from bot.typing import Repo
from bot.utils import IdComparable, AttachmentType
from bot.entities.answer_attachment import AnswerAttachment
from bot.services.statistics import AnswerStatistics


if TYPE_CHECKING:
    from bot.entities.question import Question
    from bot.entities.support_user import SupportUser


class Answer(IdComparable):
    id: UUID
    support_user: SupportUser
    question: Question
    message: str
    tg_message_id: int
    is_useful: bool | None
    date: datetime

    def __init__(
        self,
        id: UUID,
        support_user: SupportUser,
        question: Question,
        message: str,
        tg_message_id: int,
        is_useful: bool | None = None,
        date: datetime = datetime.now(),
    ):
        self.id = id
        self.support_user = support_user
        self.question = question
        self.message = message
        self.tg_message_id = tg_message_id
        self.is_useful = is_useful
        self.date = date

    async def estimate_as_useful(self, repo: Repo) -> None:
        if not (self.is_useful is None):
            return None

        await repo.estimate_answer_as_useful(self.id)

    async def estimate_as_unuseful(self, repo: Repo) -> None:
        if not (self.is_useful is None):
            return None

        await repo.estimate_answer_as_unuseful(self.id)

    async def get_attachments(self, repo: Repo) -> list[AnswerAttachment]:
        return await repo.get_answer_attachments(self.id)

    async def get_statistics(self, repo: Repo) -> AnswerStatistics:
        return await AnswerStatistics.get_statistics(self.id, repo)

    async def add_attachment(
        self,
        tg_file_id: str,
        attachment_type: AttachmentType,
        date: datetime,
        repo: Repo,
    ) -> AnswerAttachment:
        return await repo.add_answer_attachment(
            AnswerAttachment(
                uuid4(), self.id, tg_file_id, attachment_type, date=date
            )
        )
