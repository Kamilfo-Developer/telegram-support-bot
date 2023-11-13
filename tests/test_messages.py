# from app.localization.get_messages import get_messages
# from app.localization.en_messages_content import ENMessagesContent
# from app.localization.ru_messages_content import RUMessagesContent

from pytz import timezone
import pytest


@pytest.mark.skip(reason="Messages classes must be refactored first")
def test_get_messages() -> None:
    assert isinstance(get_messages("ru", timezone("UTC")), RUMessagesContent)

    assert isinstance(get_messages("en", timezone("UTC")), ENMessagesContent)

    assert isinstance(get_messages("cz", timezone("UTC")), ENMessagesContent)

    assert isinstance(
        get_messages("cz", timezone("UTC"), "ru"), RUMessagesContent
    )

    with pytest.raises(ValueError):
        get_messages("cz", timezone("UTC"), "pl")
