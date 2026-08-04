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
def test_get_master_password(monkeypatch, iterable, password):
    inputs = iter(iterable)
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    service = Config(config_path="test/config.json")

    assert service.get_master_password() == password


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
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

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
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    service = Config(config_path="test/config.json")
    service.init_config_file()

    os.remove("test/config.json")
    os.removedirs("test")
