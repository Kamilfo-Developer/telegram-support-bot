from uuid import uuid4
import pytest
from app.errors import IncorrectActionError, SameValueAssigningError

from app.shared.value_objects import (
    QuestionIdType,
    RoleIdType,
    RolePermissions,
    TgUserId,
)
from app.support_users.entities import SupportUser, SupportUserRole
from app.support_users.value_objects import DescriptiveName


@pytest.fixture()
def support_user_with_role() -> SupportUser:
    descriptive_name = DescriptiveName(
        "A descriptive name for the support user"
    )

    tg_bot_user_id = TgUserId(12345)

    support_user_role = SupportUserRole(
        RoleIdType(54321),
        RolePermissions(
            can_answer_questions=True, can_manage_support_users=False
        ),
    )

    new_support_user = SupportUser.create(
        descriptive_name,
        tg_bot_user_id,
        role=support_user_role,
    )

    return new_support_user


@pytest.fixture()
def support_user_can_answer_questions_with_bound_question() -> SupportUser:
    descriptive_name = DescriptiveName(
        "A descriptive name for the support user"
    )

    tg_bot_user_id = TgUserId(12345)

    support_user_role = SupportUserRole(
        RoleIdType(54321),
        RolePermissions(
            can_answer_questions=True, can_manage_support_users=False
        ),
    )

    new_support_user = SupportUser.create(
        descriptive_name,
        tg_bot_user_id,
        role=support_user_role,
    )

    bound_question_id = QuestionIdType(uuid4())

    new_support_user.bind_question(bound_question_id)

    return new_support_user


@pytest.fixture()
def support_user_can_answer_questions_without_bound_question() -> SupportUser:
    descriptive_name = DescriptiveName(
        "A descriptive name for the support user"
    )

    tg_bot_user_id = TgUserId(12345)

    support_user_role = SupportUserRole(
        RoleIdType(54321),
        RolePermissions(
            can_answer_questions=True, can_manage_support_users=False
        ),
    )

    new_support_user = SupportUser.create(
        descriptive_name,
        tg_bot_user_id,
        role=support_user_role,
    )

    return new_support_user


@pytest.fixture()
def support_user_cannot_answer_questions() -> SupportUser:
    descriptive_name = DescriptiveName(
        "A descriptive name for the support user"
    )

    tg_bot_user_id = TgUserId(12345)

    support_user_role = SupportUserRole(
        RoleIdType(54321),
        RolePermissions(
            can_answer_questions=False, can_manage_support_users=True
        ),
    )

    new_support_user = SupportUser.create(
        descriptive_name,
        tg_bot_user_id,
        role=support_user_role,
    )

    return new_support_user


@pytest.fixture()
def support_user_without_role() -> SupportUser:
    descriptive_name = DescriptiveName(
        "A descriptive name for the support user"
    )

    tg_bot_user_id = TgUserId(12345)

    new_support_user = SupportUser.create(
        descriptive_name,
        tg_bot_user_id,
        role=None,
    )

    return new_support_user


@pytest.fixture()
def owner_entity() -> SupportUser:
    descriptive_name = DescriptiveName(
        "A descriptive name for the support user"
    )

    tg_bot_user_id = TgUserId(12345)

    new_support_user = SupportUser.create_owner(
        descriptive_name,
        tg_bot_user_id,
    )

    return new_support_user


@pytest.fixture()
def owner_entity_without_bound_question() -> SupportUser:
    descriptive_name = DescriptiveName(
        "A descriptive name for the support user"
    )

    tg_bot_user_id = TgUserId(12345)

    new_support_user = SupportUser.create_owner(
        descriptive_name,
        tg_bot_user_id,
    )

    return new_support_user


@pytest.fixture()
def owner_entity_with_bound_question() -> SupportUser:
    descriptive_name = DescriptiveName(
        "A descriptive name for the support user"
    )

    tg_bot_user_id = TgUserId(12345)

    new_support_user = SupportUser.create_owner(
        descriptive_name,
        tg_bot_user_id,
    )

    bound_question_id = QuestionIdType(uuid4())

    new_support_user.bind_question(bound_question_id)

    return new_support_user


# Testing owner rights
def test_support_user_was_promoted_to_owner(
    support_user_with_role: SupportUser,
):
    assert support_user_with_role.role

    support_user_with_role.promote_to_owner()

    assert support_user_with_role.is_owner is True


def test_support_user_was_stripped_of_owner_rights_raises_error(
    support_user_with_role: SupportUser,
):
    assert support_user_with_role.is_owner is False

    with pytest.raises(IncorrectActionError):
        support_user_with_role.remove_owner_rights()


def test_owner_was_stripped_of_owner_rights(owner_entity: SupportUser):
    owner_entity.remove_owner_rights()

    assert owner_entity.is_owner is False


def test_owner_was_promoted_to_owner_raises_error(owner_entity: SupportUser):
    with pytest.raises(IncorrectActionError):
        owner_entity.promote_to_owner()


# Testing role assigning and removing


def test_support_user_with_role_was_stripped_of_role(
    support_user_with_role: SupportUser,
):
    assert support_user_with_role.role

    support_user_with_role.remove_role()

    assert support_user_with_role.role is None


def test_support_user_without_role_was_stripped_of_role_raises_error(
    support_user_without_role: SupportUser,
):
    assert support_user_without_role.role is None

    with pytest.raises(SameValueAssigningError):
        support_user_without_role.remove_role()


def test_owner_was_stripped_of_role_raises_error(
    owner_entity: SupportUser,
):
    with pytest.raises(IncorrectActionError):
        owner_entity.remove_role()


def test_support_user_with_role_was_assigned_a_new_one(
    support_user_with_role: SupportUser,
):
    assert support_user_with_role.role

    new_role = SupportUserRole(RoleIdType(1234), RolePermissions(False, False))

    support_user_with_role.assign_role(new_role)

    assert support_user_with_role.role == new_role


def test_support_user_without_role_was_assigned_a_new_one(
    support_user_without_role: SupportUser,
):
    assert support_user_without_role.role is None

    new_role = SupportUserRole(RoleIdType(1234), RolePermissions(False, False))

    support_user_without_role.assign_role(new_role)

    assert support_user_without_role.role == new_role


def test_support_user_assigned_same_role_raises_error(
    support_user_with_role: SupportUser,
):
    assert support_user_with_role.role

    same_role = SupportUserRole(
        support_user_with_role.role._id,
        support_user_with_role.role.permissions,
    )

    with pytest.raises(SameValueAssigningError):
        support_user_with_role.assign_role(same_role)


def test_owner_role_was_changed_raises_error(owner_entity: SupportUser):
    new_role = SupportUserRole(RoleIdType(1234), RolePermissions(False, False))

    with pytest.raises(IncorrectActionError):
        owner_entity.assign_role(new_role)


# Test binding and unbinding questions


def test_owner_with_bound_question_bound_a_question(
    owner_entity_with_bound_question: SupportUser,
):
    question_id = QuestionIdType(uuid4())

    owner_entity_with_bound_question.bind_question(question_id)

    assert owner_entity_with_bound_question.current_question_id == question_id


def test_owner_without_bound_question_bound_a_question(
    owner_entity_without_bound_question: SupportUser,
):
    question_id = QuestionIdType(uuid4())

    owner_entity_without_bound_question.bind_question(question_id)

    assert (
        owner_entity_without_bound_question.current_question_id == question_id
    )


def test_owner_with_bound_question_unbound_a_question(
    owner_entity_with_bound_question: SupportUser,
):
    owner_entity_with_bound_question.unbind_question()

    assert owner_entity_with_bound_question.current_question_id is None


def test_owner_without_bound_question_unbound_a_question_raises_error(
    owner_entity_without_bound_question: SupportUser,
):
    with pytest.raises(SameValueAssigningError):
        owner_entity_without_bound_question.unbind_question()


def test_support_user_with_bound_question_bound_a_question(
    support_user_can_answer_questions_with_bound_question: SupportUser,
):
    question_id = QuestionIdType(uuid4())

    support_user_can_answer_questions_with_bound_question.bind_question(
        question_id
    )

    assert (
        support_user_can_answer_questions_with_bound_question.current_question_id  # noqa: E501
        == question_id
    )


def test_support_user_with_unbound_question_bound_a_question(
    support_user_can_answer_questions_without_bound_question: SupportUser,
):
    question_id = QuestionIdType(uuid4())

    support_user_can_answer_questions_without_bound_question.bind_question(
        question_id
    )

    assert (
        support_user_can_answer_questions_without_bound_question.current_question_id  # noqa: E501
        == question_id
    )


def test_support_user_cannot_answering_questions_bound_a_question_raises_error(  # noqa: E501
    support_user_cannot_answer_questions: SupportUser,
):
    question_id = QuestionIdType(uuid4())

    with pytest.raises(IncorrectActionError):
        support_user_cannot_answer_questions.bind_question(question_id)


def test_support_user_cannot_answering_questions_unbound_a_question_raises_error(  # noqa: E501
    support_user_cannot_answer_questions: SupportUser,
):
    assert support_user_cannot_answer_questions.current_question_id is None

    with pytest.raises(IncorrectActionError):
        support_user_cannot_answer_questions.unbind_question()


def test_support_user_with_bound_question_unbound_a_question(
    support_user_can_answer_questions_with_bound_question: SupportUser,
):
    support_user_can_answer_questions_with_bound_question.unbind_question()

    assert (
        support_user_can_answer_questions_with_bound_question.current_question_id  # noqa: E501
        is None
    )


def test_support_user_without_bound_question_unbound_a_question_raises_error(  # noqa: E501
    support_user_can_answer_questions_without_bound_question: SupportUser,
):
    assert (
        support_user_can_answer_questions_without_bound_question.current_question_id  # noqa: E501
        is None
    )

    with pytest.raises(SameValueAssigningError):
        support_user_can_answer_questions_without_bound_question.unbind_question()  # noqa: E501
