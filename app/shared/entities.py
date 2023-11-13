from __future__ import annotations

import abc
from datetime import datetime

from app.shared.value_objects import TgCaption, TgFileIdType
from app.utils import TgFileType


class Attachment(abc.ABC):
    tg_file_id: TgFileIdType

    attachment_type: TgFileType

    caption: TgCaption | None

    date: datetime

    def __eq__(self, __value: object) -> bool:
        return (
            isinstance(__value, Attachment)
            and self.tg_file_id == __value.tg_file_id
        )
