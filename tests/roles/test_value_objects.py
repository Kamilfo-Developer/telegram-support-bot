import pytest

from app.roles.value_objects import RoleDescription, RoleName


def test_role_description():
    with pytest.raises(ValueError):
        RoleDescription("This will raise an error" * 666)

    string_for_name = "A normal role description"

    name = RoleDescription(string_for_name)

    assert string_for_name == name


def test_role_name():
    with pytest.raises(ValueError):
        RoleName("This will raise an error" * 666)

    string_for_name = "A normal role description"

    name = RoleName(string_for_name)

    assert string_for_name == name
