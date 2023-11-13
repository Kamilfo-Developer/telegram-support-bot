from re import A
from uuid import UUID, uuid4
import pytest
from app.utils import (
    ArgumentsValidator,
    IdComparable,
    StrWithMaxLength,
    ValueObject,
)


def test_value_object():
    class AValueObject(ValueObject):
        property_a: int
        property_b: str

        def __init__(self, property_a: int, property_b: str):
            self.property_a = property_a
            self.property_b = property_b

    a_value_object = AValueObject(12345, "12345")

    another_value_object = AValueObject(12345, "12345")

    assert a_value_object == another_value_object

    third_value_object = AValueObject(54321, "12345")

    assert third_value_object != a_value_object


def test_str_with_max_length():
    class AStrWithMaxLength(StrWithMaxLength):
        MAX_LENGTH = 5

    with pytest.raises(ValueError):
        AStrWithMaxLength("123456")

    a_str_with_max_length = "12345"

    assert a_str_with_max_length == AStrWithMaxLength(a_str_with_max_length)


def test_id_comparable():
    class AnIdComparable(IdComparable):
        _id: UUID
        a: str

        def __init__(self, id: UUID, a: str):
            self._id = id
            self.a = a

    class AnotherIdComparable(IdComparable):
        _id: UUID
        b: str

        def __init__(self, id: UUID, b: str):
            self._id = id
            self.b = b

    id = uuid4()

    an_id_comparable = AnIdComparable(id, "12345")

    second_id_comparable = AnIdComparable(id, "54321")

    assert an_id_comparable == second_id_comparable

    another_id_comparable = AnotherIdComparable(id, "15243")

    assert an_id_comparable == another_id_comparable


def test_arguments_validator():
    validator = ArgumentsValidator(["Not convertable to int"])

    assert validator.is_valid() is True
    assert validator.convertable(int).is_valid() is False

    validator = ArgumentsValidator(["101", "123"])

    assert (
        validator.convertable(int).next().convertable(int).is_valid() is True
    )

    validator = ArgumentsValidator(["101", "Some random string"])

    assert validator.convertable(int).is_valid() is False
