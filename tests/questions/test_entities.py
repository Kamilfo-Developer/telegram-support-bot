from uuid import uuid4

import pytest
from app.questions.entities import Question
from app.shared.value_objects import (
    RegularUserIdType,
    TgCaption,
    TgFileIdType,
    TgMessageIdType,
    TgMessageText,
)
from app.utils import TgFileType


@pytest.fixture()
def question_entity() -> Question:
    regular_user_id = RegularUserIdType(uuid4())

    message = TgMessageText("13kjrlskfg")

    tg_message_id = TgMessageIdType(123123123)

    question_entity = Question.create(regular_user_id, message, tg_message_id)

    return question_entity


def test_a_new_attachment_was_added_to_question(
    question_entity: Question,
):
    assert question_entity.attachments == []

    tg_file_id = TgFileIdType("aklsdjflks")

    attachment_type = TgFileType.IMAGE

    caption = TgCaption("klasjdfl;ksajdf")

    question_entity.add_attachment(tg_file_id, attachment_type, caption)

    assert len(question_entity.attachments) == 1

    assert question_entity.attachments[0].tg_file_id == tg_file_id

    assert question_entity.attachments[0].caption == caption

    assert question_entity.attachments[0].attachment_type == attachment_type
