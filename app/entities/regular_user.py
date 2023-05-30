from __future__ import annotations
from datetime import datetime
from typing import Self
from uuid import UUID, uuid4
from app.utils import IdComparable


class RegularUser(IdComparable):
    id: UUID
    tg_bot_user_id: int
    join_date: datetime

    def __init__(
        self,
        id: UUID,
        tg_bot_user_id: int,
        join_date: datetime = datetime.now(),
    ) -> None:
        self.id = id
        self.tg_bot_user_id = tg_bot_user_id
        self.join_date = join_date

    @classmethod
    def create(cls, tg_bot_user_id: int) -> Self:
        regular_user = cls(
            id=uuid4(),
            tg_bot_user_id=tg_bot_user_id,
            join_date=datetime.utcnow(),
        )

        return regular_user
