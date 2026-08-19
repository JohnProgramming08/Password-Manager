import pytest
from interface import ConfigBridge
from types import SimpleNamespace


# config it
def test_none(empty_config_file):
    args = SimpleNamespace(config="activated", command="it")
    config_bridge = ConfigBridge(args, config_path="test/config.json")
    assert config_bridge.command is None


# config init
def test_init(monkeypatch, empty_config_file):
    monkeypatch.setattr("getpass.getpass", lambda _: "test")

    args = SimpleNamespace(config="activated", init="activated")
    config_bridge = ConfigBridge(args, config_path="test/config.json")
    assert config_bridge.command == "init"


# config password attempt_limit [limit_value]
def test_password_attempt_limit(monkeypatch, empty_config_file):
    monkeypatch.setattr("getpass.getpass", lambda _: "test")

    args = SimpleNamespace(
        config="activated",
        attempt_limit="activated",
        limit_value=3,
    )
    config_bridge = ConfigBridge(args, config_path="test/config.json")
    assert config_bridge.command == "attempt_limit"


# config email [email_value]
def test_email(monkeypatch, empty_config_file):
    monkeypatch.setattr("getpass.getpass", lambda _: "test")

    args = SimpleNamespace(
        config="activated", email="activated", email_value="sigma@female.ru"
    )
    config_bridge = ConfigBridge(args, config_path="test/config.json")
    assert config_bridge.command == "email"
