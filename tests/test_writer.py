import pytest
import os
from services import Writer


# Adding a section to the data vault
@pytest.mark.parametrize("name", ["valid_name", "literally_anything", "sigma"])
def test_add_section_filled_valid(monkeypatch, filled_config_file, name):
    monkeypatch.setattr("builtins.input", lambda _: "test")
    assert Writer.add_section(name, vault_path="test/") is True
    os.remove(f"test/{name}.json")


def test_add_section_filled_invalid(monkeypatch, filled_config_file):
    inputs = iter(["test", "incorrect"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    assert Writer.add_section("valid", vault_path="invalid/") is False
    Writer.add_section("copy", vault_path="test/")
    assert Writer.add_section("copy", vault_path="test/") is False
    assert Writer.add_section("fine", vault_path="test/") is False

    os.remove("test/copy.json")


@pytest.mark.parametrize(
    "iterable, section_name",
    [
        (["test", "test", "test"], "valid"),
        (["test", "nope", "fine", "fine", "fine"], "literally_anything"),
        (
            ["whenever", "wherever", "with space", "with space", "with space"],
            "whaaaaat",
        ),
    ],
)
def test_add_section_empty_valid(
    monkeypatch, empty_config_file, iterable, section_name
):
    inputs = iter(iterable)
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    assert Writer.add_section(section_name, vault_path="test/") is True

    os.remove(f"test/{section_name}.json")


@pytest.mark.parametrize(
    "iterable, section_name",
    [
        (["test", "test", "fine"], "codewars"),
        (["not it", "fine", "fine", "fine", "not it"], "anything"),
        (["nope", "nope", "test"], "any_is_fine"),
    ],
)
def test_add_section_empty_invalid1(
    monkeypatch, empty_config_file, iterable, section_name
):
    inputs = iter(iterable)
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    assert Writer.add_section(section_name, vault_path="test/") is False


def test_add_section_empty_invalid2(monkeypatch, empty_config_file):
    monkeypatch.setattr("builtins.input", lambda _: "test")
    Writer.add_section("duplicate", vault_path="test/")
    assert Writer.add_section("duplicate", vault_path="test/") is False

    os.remove("test/duplicate.json")


def test_add_section_nonexistent_invalid():
    assert Writer.add_section("anything", vault_path="test/") is False


# Setting the value of a field in a section
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
        Writer.set_field("empty", field_name, value, vault_path="test/") is True
    )

    os.remove("test/empty.json")


def test_set_field_invalid(monkeypatch, empty_section):
    inputs = iter(["not correct", "test", "test"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    assert (
        Writer.set_field("empty", "fine", "fine", vault_path="test/") is False
    )
    assert (
        Writer.set_field("invalid", "fine", "fine", vault_path="test/") is False
    )
    assert (
        Writer.set_field("empty", "fine", "fine", vault_path="wrong/") is False
    )

    os.remove("test/empty.json")
