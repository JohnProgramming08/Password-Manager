from services import Config
import os
import pytest


# Checking if a config file is filled in
def test_is_config_finished_false1():
    service = Config(config_path="test/config.json")
    assert service.is_config_finished() is False
    os.removedirs("test")


def test_is_config_finished_false2(empty_config_file):
    service = Config(config_path="test/config.json")
    assert service.is_config_finished() is False
    with open("test/config.json", "w") as file:
        file.write("{}")
    assert service.is_config_finished() is False


def test_is_config_finished_true(filled_config_file):
    service = Config(config_path="test/config.json")
    assert service.is_config_finished() is True


# Asking the user for their master password
@pytest.mark.parametrize(
    "iterable, password",
    [
        (("password", "password"), "password"),
        (("cool", "not the same", "cool", "cool"), "cool"),
        (("", "", "fine", "", "fine", "fine"), "fine"),
    ],
)
def test_set_master_password(monkeypatch, iterable, password):
    inputs = iter(iterable)
    monkeypatch.setattr("getpass.getpass", lambda _: next(inputs))
    service = Config(config_path="test/config.json")

    assert service.set_master_password() == password


# Ask the user to fill in the config file if not already filled
def test_init_config_file_filled(filled_config_file):
    service = Config(config_path="test/config.json")
    service.init_config_file()


@pytest.mark.parametrize(
    "iterable",
    [
        ("password", "password"),
        ("cool", "not the same", "cool", "cool"),
        ("", "", "fine", "", "fine", "fine"),
    ],
)
def test_init_config_file_empty(monkeypatch, empty_config_file, iterable):
    inputs = iter(iterable)
    monkeypatch.setattr("getpass.getpass", lambda _: next(inputs))

    service = Config(config_path="test/config.json")
    service.init_config_file()


@pytest.mark.parametrize(
    "iterable",
    [
        ("password", "password"),
        ("cool", "not the same", "cool", "cool"),
        ("", "", "fine", "", "fine", "fine"),
    ],
)
def test_init_config_file_nonexistent(monkeypatch, iterable):
    inputs = iter(iterable)
    monkeypatch.setattr("getpass.getpass", lambda _: next(inputs))

    service = Config(config_path="test/config.json")
    service.init_config_file()

    os.remove("test/config.json")
    os.removedirs("test")


# Confirm the users master password
def test_confirm_master_password_filled_valid(filled_config_file, monkeypatch):
    monkeypatch.setattr("getpass.getpass", lambda _: "test")
    service = Config(config_path="test/config.json")
    assert service.confirm_master_password() == "test"


@pytest.mark.parametrize(
    "input", ["not correct", "tes", "TEST", "boom", "sigma"]
)
def test_confirm_master_password_filled_invalid(
    filled_config_file, monkeypatch, input
):
    monkeypatch.setattr("getpass.getpass", lambda _: input)
    service = Config(config_path="test/config.json")
    assert service.confirm_master_password() is None


@pytest.mark.parametrize(
    "iterable, expected",
    [
        (["sigma", "sigma", "sigma"], "sigma"),
        (["not", "equal", "same", "same", "same"], "same"),
        (["valid", "valid", "not valid"], None),
        (["not it", "it", "it", "it", "not it"], None),
    ],
)
def test_confirm_master_password_empty(
    monkeypatch, empty_config_file, iterable, expected
):
    inputs = iter(iterable)
    monkeypatch.setattr("getpass.getpass", lambda _: next(inputs))
    service = Config(config_path="test/config.json")
    assert service.confirm_master_password() == expected


@pytest.mark.parametrize(
    "iterable, expected",
    [
        (["test", "test", "test"], "test"),
        (["test", "test", "nope"], None),
        (["weird", "not the same", "equal", "equal", "equal"], "equal"),
        (["weird", "not the same", "equal", "equal", "invalid"], None),
    ],
)
def test_confirm_master_password_nonexistent(monkeypatch, iterable, expected):
    inputs = iter(iterable)
    monkeypatch.setattr("getpass.getpass", lambda _: next(inputs))
    service = Config(config_path="test/config.json")
    assert service.confirm_master_password() == expected

    os.remove("test/config.json")
    os.removedirs("test")
