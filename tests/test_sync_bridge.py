from interface import SyncBridge
from types import SimpleNamespace


# sync
def test_none(filled_config_file):
    args = SimpleNamespace(sync="activated")
    sync_bridge = SyncBridge(args, config_path="test/config.json")
    assert sync_bridge.command is None


# sync pull
def test_pull(monkeypatch, filled_config_file):
    monkeypatch.setattr("getpass.getpass", lambda _: "test")
    args = SimpleNamespace(sync="activated", pull="activated")
    sync_bridge = SyncBridge(args, config_path="test/config.json")
    assert sync_bridge.command == "pull"


# sync push
def test_push(monkeypatch, filled_config_file):
    monkeypatch.setattr("getpass.getpass", lambda _: "test")
    args = SimpleNamespace(sync="activated", push="activated")
    sync_bridge = SyncBridge(args, config_path="test/config.json")
    assert sync_bridge.command == "push"
