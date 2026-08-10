from types import SimpleNamespace
from interface import FieldBridge


def test_none():
    args1 = SimpleNamespace(field="activated", set="activated")
    field_bridge1 = FieldBridge(args1)
    assert field_bridge1.command is None

    args2 = SimpleNamespace()
    field_bridge1 = FieldBridge(args2)
    assert field_bridge1.command is None


def test_set(monkeypatch, filled_config_file):
    monkeypatch.setattr("builtins.input", lambda _: "test")

    args = SimpleNamespace(
        field="activated",
        set="activated",
        section_name="filled",
        field_name="sigma",
        value="female",
    )
    field_bridge = FieldBridge(args)
    assert field_bridge.command == "set"


def test_get(monkeypatch, filled_config_file):
    monkeypatch.setattr("builtins.input", lambda _: "test")

    args = SimpleNamespace(
        field="activated",
        get="activated",
        section_name="filled",
        field_name="cant",
    )
    field_bridge = FieldBridge(args)
    assert field_bridge.command == "get"


def test_ls(filled_config_file):
    args = SimpleNamespace(field="activated", ls="activated")
    field_bridge = FieldBridge(args)
    assert field_bridge.command == "ls"


def test_ls_section(filled_config_file):
    args = SimpleNamespace(
        field="activated", ls="activated", section_name="config"
    )
    field_bridge = FieldBridge(args)
    assert field_bridge.command == "ls section"


def test_rm(monkeypatch, filled_section):
    monkeypatch.setattr("builtins.input", lambda _: "test")
    args = SimpleNamespace(
        field="activated",
        rm="activated",
        section_name="filled",
        field_name="username",
    )
    field_bridge = FieldBridge(args)
    assert field_bridge.command == "rm"
