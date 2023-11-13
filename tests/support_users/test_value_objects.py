import pytest

from app.support_users.value_objects import DescriptiveName


def test_descriptive_name():
    with pytest.raises(ValueError):
        DescriptiveName("This will raise an error" * 666)

    string_for_name = "A normal descriptive name"

    name = DescriptiveName(string_for_name)

    assert string_for_name == name
