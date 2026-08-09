import pytest
import os
from services import Field


# Setting the value of a field in a Field
@pytest.mark.parametrize(
    "field_name, value",
    [
        ("sigma", "male"),
        ("valid", "test"),
        ("21", "54"),
        ("this is getting a bit long now", "but dont worry ong"),
    ],
)
def test_set_field_valid(monkeypatch, empty_section, field_name, value):
    monkeypatch.setattr("builtins.input", lambda _: "test")
    assert (
        Field.set_field("empty", field_name, value, vault_path="test/") is True
    )

    os.remove("test/empty.json")


def test_set_field_invalid(monkeypatch, empty_section):
    inputs = iter(["not correct", "test", "test"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    assert Field.set_field("empty", "fine", "fine", vault_path="test/") is False
    assert (
        Field.set_field("invalid", "fine", "fine", vault_path="test/") is False
    )
    assert (
        Field.set_field("empty", "fine", "fine", vault_path="wrong/") is False
    )

    os.remove("test/empty.json")


# Getting the value of a given field in a Field
@pytest.mark.parametrize(
    "field, expected",
    [
        ("username", "sigma"),
        ("password", "MORE SIGMA"),
        ("email", "test"),
        ("not a field", "empty"),
    ],
)
def test_get_value_valid(monkeypatch, filled_section, field, expected):
    monkeypatch.setattr("builtins.input", lambda _: "test")
    assert Field.get_value("filled", field, vault_path="test/") == expected


def test_get_value_invalid(monkeypatch, filled_section):
    inputs = iter(["incorrect", "test", "test"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    assert Field.get_value("filled", "username", vault_path="test/") is None
    assert Field.get_value("filled", "username", vault_path="nopety/") is None
    assert Field.get_value("wrong", "username", vault_path="test/") is None


# Listing all fields in a section
def test_list_fields_in_section_filled(filled_section):
    assert Field.list_fields_in_section("filled", vault_path="test/") != ""


def test_list_fields_in_section_empty(empty_section):
    assert Field.list_fields_in_section("empty", vault_path="test/") == ""
    os.remove("test/empty.json")


# List all fields
def test_list_fields_filled(filled_section):
    assert Field.list_fields(vault_path="test/") != ""


def test_list_fields_empty(empty_section):
    assert Field.list_fields(vault_path="test/") == ""
    os.remove("test/empty.json")
