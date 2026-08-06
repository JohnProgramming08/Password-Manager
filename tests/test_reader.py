from services import Reader
import pytest


@pytest.mark.parametrize(
    "field, expected",
    [
        ("username", "sigma"),
        ("password", "MORE SIGMA"),
        ("email", "test"),
        ("not a field", "empty"),
    ],
)
def test_get_value_valid(monkeypatch, filled_section, field, expected):
    monkeypatch.setattr("builtins.input", lambda _: "test")
    assert Reader.get_value("filled", field, vault_path="test/") == expected


def test_get_value_invalid(monkeypatch, filled_section):
    inputs = iter(["incorrect", "test", "test"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    assert Reader.get_value("filled", "username", vault_path="test/") is None
    assert Reader.get_value("filled", "username", vault_path="nopety/") is None
    assert Reader.get_value("wrong", "username", vault_path="test/") is None
