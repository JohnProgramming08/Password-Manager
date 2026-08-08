from types import SimpleNamespace
from interface import SectionBridge
import os


def test_create(monkeypatch, filled_config_file):
    monkeypatch.setattr("builtins.input", lambda _: "test")
    args = SimpleNamespace(
        section="activated", create="activated", section_name="sigma"
    )
    section_bridge = SectionBridge(args)
    assert section_bridge.command == "create"
