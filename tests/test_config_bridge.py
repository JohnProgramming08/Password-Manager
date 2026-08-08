import pytest
from interface import ConfigBridge
from types import SimpleNamespace


# config it
def test_none(empty_config_file):
    args = SimpleNamespace(config="activated", command="it")
    config_bridge = ConfigBridge(args)
    assert config_bridge.command is None


# config init
def test_init(monkeypatch, empty_config_file):
    monkeypatch.setattr("builtins.input", lambda _: "sigma")

    args = SimpleNamespace(config="activated", command="init")
    config_bridge = ConfigBridge(args)
    assert config_bridge.command == "init"
