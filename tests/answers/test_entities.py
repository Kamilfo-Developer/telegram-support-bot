from uuid import uuid4

import pytest
from app.answers.entities import Answer
from app.errors import AnswerAlreadyEstimatedError
from app.shared.value_objects import (
    QuestionIdType,
    SupportUserIdType,
    TgCaption,
    TgFileIdType,
    TgMessageIdType,
    TgMessageText,
)
from app.utils import TgFileType


@pytest.fixture()
def answer_entity() -> Answer:
    support_user_id = SupportUserIdType(uuid4())

    question_id = QuestionIdType(uuid4())

    message = TgMessageText("Answer message")

    tg_message_id = TgMessageIdType(12351356)

    answer_entity = Answer.create(
        support_user_id, question_id, message, tg_message_id
    )

    assert answer_entity.is_useful is None

    return answer_entity


def test_answer_entity_is_estemated_as_useful_when_not_estimated(
    answer_entity: Answer,
):
    assert answer_entity.is_useful is None

    answer_entity.estimate_as_useful()

    assert answer_entity.is_useful is True


def test_answer_entity_estemated_as_unuseful_when_not_estimated(
    answer_entity: Answer,
):
    assert answer_entity.is_useful is None

    answer_entity.estimate_as_unuseful()

    assert answer_entity.is_useful is False


def test_answer_entity_estemated_as_unuseful_when_estimated_as_useful(
    answer_entity: Answer,
):
    answer_entity.estimate_as_useful()

    assert answer_entity.is_useful is True

    answer_entity.estimate_as_unuseful()

    assert answer_entity.is_useful is False


def test_answer_entity_estemated_as_useful_when_estimated_as_unuseful(
    answer_entity: Answer,
):
    answer_entity.estimate_as_unuseful()

    assert answer_entity.is_useful is False

    answer_entity.estimate_as_useful()

    assert answer_entity.is_useful is True


def test_answer_entity_estemated_as_useful_when_estimated_as_useful(
    answer_entity: Answer,
):
    answer_entity.estimate_as_useful()

    assert answer_entity.is_useful is True

    with pytest.raises(AnswerAlreadyEstimatedError):
        answer_entity.estimate_as_useful()


def test_answer_entity_estemated_as_unuseful_when_estimated_as_unuseful(
    answer_entity: Answer,
):
    answer_entity.estimate_as_unuseful()

    assert answer_entity.is_useful is False

    with pytest.raises(AnswerAlreadyEstimatedError):
        answer_entity.estimate_as_unuseful()


def test_an_attachment_was_added_to_answer_entity(answer_entity: Answer):
    assert answer_entity.attachments == []

    tg_file_id = TgFileIdType("sdfklasdf")

    attachment_type = TgFileType.DOCUMENT

    tg_caption = TgCaption("SDfjklas;df;lksjf")

    answer_entity.add_attachment(
        tg_file_id,
        attachment_type,
        tg_caption,
    )

    assert len(answer_entity.attachments) == 1

    assert answer_entity.attachments[0].attachment_type == attachment_type
    assert answer_entity.attachments[0].tg_file_id == tg_file_id
    assert answer_entity.attachments[0].caption == tg_caption
