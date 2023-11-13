from __future__ import annotations
from datetime import datetime
from typing import Self
from uuid import uuid4

from app.shared.value_objects import (
    RegularUserIdType,
    TgUserId,
)
from app.utils import IdComparable


class RegularUser(IdComparable):
    _id: RegularUserIdType
    tg_bot_user_id: TgUserId
    join_date: datetime

    def __init__(
        self,
        id: RegularUserIdType,
        tg_bot_user_id: TgUserId,
        join_date: datetime = datetime.now(),
    ) -> None:
        """This method should not be called directly.
        Use ```RegularUser.create(...)``` instead."""

        self._id = id
        self.tg_bot_user_id = tg_bot_user_id
        self.join_date = join_date

    @classmethod
    def create(cls, tg_bot_user_id: TgUserId) -> Self:
        """A factory method which creates a new ```RegularUser``` entity.

        Args:
            tg_bot_user_id (TgUserId): Telegram user id of the user

        Returns:
            Self: new ```RegularUser``` entity
        """

        regular_user = cls(
            id=RegularUserIdType(uuid4()),
            tg_bot_user_id=tg_bot_user_id,
            join_date=datetime.utcnow(),
        )

        return regular_user
