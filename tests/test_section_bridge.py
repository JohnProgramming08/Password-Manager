from types import SimpleNamespace
from interface import SectionBridge
import os


def test_create(monkeypatch, filled_config_file):
    monkeypatch.setattr("getpass.getpass", lambda _: "test")
    args = SimpleNamespace(
        section="activated", create="activated", section_name="sigma"
    )
    section_bridge = SectionBridge(args)
    assert section_bridge.command == "create"


def test_list(filled_config_file):
    args = SimpleNamespace(section="activated", ls="activated")
    section_bridge = SectionBridge(args)
    assert section_bridge.command == "ls"


def test_remove(monkeypatch, many_empty_sections):
    monkeypatch.setattr("getpass.getpass", lambda _: "test")
    args = SimpleNamespace(
        section="activated", rm="activated", section_name="two"
    )
    section_bridge = SectionBridge(args)
    assert section_bridge.command == "rm"
