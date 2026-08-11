from services import Section
import pytest
import os


# Adding a section to the data vault
@pytest.mark.parametrize("name", ["valid_name", "literally_anything", "sigma"])
def test_add_section_filled_valid(monkeypatch, filled_config_file, name):
    monkeypatch.setattr("getpass.getpass", lambda _: "test")
    assert Section.add_section(name, vault_path="test/") is True
    os.remove(f"test/{name}.json")


def test_add_section_filled_invalid(monkeypatch, filled_config_file):
    inputs = iter(["test", "incorrect"])
    monkeypatch.setattr("getpass.getpass", lambda _: next(inputs))
    assert Section.add_section("valid", vault_path="invalid/") is False
    Section.add_section("copy", vault_path="test/")
    assert Section.add_section("copy", vault_path="test/") is False
    assert Section.add_section("fine", vault_path="test/") is False

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
    monkeypatch.setattr("getpass.getpass", lambda _: next(inputs))
    assert Section.add_section(section_name, vault_path="test/") is True

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
    monkeypatch.setattr("getpass.getpass", lambda _: next(inputs))
    assert Section.add_section(section_name, vault_path="test/") is False


def test_add_section_empty_invalid2(monkeypatch, empty_config_file):
    monkeypatch.setattr("getpass.getpass", lambda _: "test")
    Section.add_section("duplicate", vault_path="test/")
    assert Section.add_section("duplicate", vault_path="test/") is False

    os.remove("test/duplicate.json")


def test_add_section_nonexistent_invalid():
    assert Section.add_section("anything", vault_path="test/") is False


# Listing all sections made by the user
def test_list_sections_none(empty_config_file):
    assert Section.list_sections(vault_path="test/") == ""


def test_list_sections_one(empty_section):
    assert Section.list_sections(vault_path="test/") == "empty"
    os.remove("test/empty.json")


def test_list_sections_many(many_empty_sections):
    res = "one\nthree\ntwo"
    assert Section.list_sections(vault_path="test/") == res


# Removing a section
@pytest.mark.parametrize("section_name", ["one", "two", "three"])
def test_remove_section_valid(monkeypatch, many_empty_sections, section_name):
    monkeypatch.setattr("getpass.getpass", lambda _: "test")
    assert Section.remove_section(section_name, vault_path="test/") is True


def test_remove_section_invalid1(many_empty_sections):
    assert Section.remove_section("four", vault_path="test/") is False


def test_remove_section_invalid2(monkeypatch, many_empty_sections):
    monkeypatch.setattr("getpass.getpass", lambda _: "wrong")
    assert Section.remove_section("one", vault_path="test/") is False
