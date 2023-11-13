import pytest
from app.regular_users.entities import RegularUser
from app.shared.value_objects import TgUserId


@pytest.fixture()
def regular_user_entity() -> RegularUser:
    tg_bot_user_id = 12345

    regular_user = RegularUser.create(TgUserId(tg_bot_user_id))

    return regular_user
