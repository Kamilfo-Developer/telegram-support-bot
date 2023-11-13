import pytest
from app.errors import SameValueAssigningError

from app.roles.entities import Role
from app.roles.value_objects import RoleDescription, RoleName
from app.shared.value_objects import RolePermissions


@pytest.fixture()
def role_entity() -> Role:
    name = RoleName("ARoleName")

    description = RoleDescription("A description for ARoleName role")

    permissions = RolePermissions(True, False)

    role_entity = Role.create(
        name=name, description=description, permissions=permissions
    )

    return role_entity


def test_role_permissions_changed_to_new(role_entity: Role):
    new_permissions = RolePermissions(
        can_answer_questions=(
            not role_entity.permissions.can_answer_questions
        ),
        can_manage_support_users=(
            not role_entity.permissions.can_manage_support_users
        ),
    )

    role_entity.change_permissions(new_permissions)

    assert role_entity.permissions == new_permissions


def test_role_permissions_changed_to_the_same_one_raises_error(
    role_entity: Role,
):
    same_permissions = RolePermissions(
        can_answer_questions=(role_entity.permissions.can_answer_questions),
        can_manage_support_users=(
            role_entity.permissions.can_manage_support_users
        ),
    )

    with pytest.raises(SameValueAssigningError):
        role_entity.change_permissions(same_permissions)


def test_role_name_changed_to_new(role_entity: Role):
    new_name = RoleName("A new name for the role")

    role_entity.change_name(new_name)

    assert role_entity.name == new_name


def test_role_name_changed_to_the_same_one_raises_error(role_entity: Role):
    same_name = RoleName(role_entity.name)

    with pytest.raises(SameValueAssigningError):
        role_entity.change_name(same_name)


def test_role_description_changed_to_new(role_entity: Role):
    new_description = RoleDescription("A new description for the role")

    role_entity.change_description(new_description)

    assert role_entity.description == new_description


def test_role_description_changed_to_the_same_one_raise_error(
    role_entity: Role,
):
    same_description = RoleDescription(role_entity.description)

    with pytest.raises(SameValueAssigningError):
        role_entity.change_description(same_description)
