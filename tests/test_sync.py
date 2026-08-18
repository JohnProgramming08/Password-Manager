from services import Sync, Encryption
from unittest.mock import patch, MagicMock
import os


# Uploading a file to the remote
@patch("requests.post")
def test_upload_file_valid(mock_post, monkeypatch, filled_config_file):
    monkeypatch.setattr("getpass.getpass", lambda _: "test")
    fake_response = MagicMock()
    fake_response.status_code = 200
    fake_response.return_value = {"ok": True}
    mock_post.return_value = fake_response

    sync = Sync("http:/", "sigma@guy.ru", vault_path="test")
    assert sync.upload_file("config.json") == 200
    mock_post.assert_called_once()


@patch("requests.post")
def test_upload_file_invalid(mock_post, monkeypatch, filled_config_file):
    monkeypatch.setattr("getpass.getpass", lambda _: "test")
    fake_response = MagicMock()
    fake_response.status_code = 404
    fake_response.return_value = {"ok": True}
    mock_post.return_value = fake_response

    sync = Sync("http:/", "sigma@guy.ru", vault_path="test")
    assert sync.upload_file("config.json") == 404
    mock_post.assert_called_once()


# Uploading all files to the remote
@patch("requests.post")
def test_push_valid(mock_post, monkeypatch, filled_section):
    monkeypatch.setattr("getpass.getpass", lambda _: "test")
    fake_response = MagicMock()
    fake_response.status_code = 200
    fake_response.return_value = {"ok": True}
    mock_post.return_value = fake_response

    sync = Sync("http:/", "sigma@guy.ru", vault_path="test")
    assert sync.push() is True
    assert mock_post.call_count == 2


@patch("requests.post")
def test_push_invalid1(mock_post, monkeypatch, filled_section):
    monkeypatch.setattr("getpass.getpass", lambda _: "wrong")
    sync = Sync("http:/", "sigma@guy.ru", vault_path="test")
    assert sync.push() is False


@patch("requests.post")
def test_push_invalid2(mock_post, monkeypatch, filled_section):
    monkeypatch.setattr("getpass.getpass", lambda _: "test")
    fake_response = MagicMock()
    fake_response.status_code = 404
    fake_response.return_value = {}
    mock_post.return_value = fake_response

    sync = Sync("http:/", "sigma@guy.ru", vault_path="test")
    assert sync.push() is False


# Downloading a file
@patch("requests.post")
def test_download_file_valid(mock_post, monkeypatch, filled_section):
    monkeypatch.setattr("getpass.getpass", lambda _: "test")
    test_data = {"sigma": "male", "great": "britain"}
    fake_response = MagicMock()
    fake_response.status_code = 200
    fake_response.return_value = test_data
    mock_post.return_value = fake_response

    sync = Sync("http:/", "sigma@guy.ru", vault_path="test")
    assert sync.download_file("dope.json") == 200

    os.remove("test/dope.json")


@patch("requests.post")
def test_download_file_invalid(mock_post, monkeypatch, filled_section):
    monkeypatch.setattr("getpass.getpass", lambda _: "test")
    fake_response = MagicMock()
    fake_response.status_code = 404
    fake_response.json.return_value = {}
    mock_post.return_value = fake_response

    sync = Sync("http:/", "sigma@guy.ru", vault_path="test")
    assert sync.download_file("dope.json") == 404

    os.remove("test/dope.json")


# Fetching a list of all backed up file names
@patch("requests.post")
def test_get_file_names_valid(mock_post, monkeypatch, filled_section):
    monkeypatch.setattr("getpass.getpass", lambda _: "test")
    test_data = {"one.json": "yup", "two.json": "yup", "three.json": "yup"}
    fake_response = MagicMock()
    fake_response.status_code = 200
    fake_response.json.return_value = test_data
    mock_post.return_value = fake_response

    sync = Sync("http:/", "sigma@guy.ru", vault_path="test")
    name_list = sync.get_file_names()
    assert name_list == [key for key in test_data]


@patch("requests.post")
def test_get_file_names_invalid(mock_post, monkeypatch, filled_section):
    monkeypatch.setattr("getpass.getpass", lambda _: "test")
    fake_response = MagicMock()
    fake_response.status_code = 404
    fake_response.json.return_value = {}
    mock_post.return_value = fake_response

    sync = Sync("http:/", "sigma@guy.ru", vault_path="test")
    name_list = sync.get_file_names()
    assert name_list == []


# Downloading all backed up data
@patch("requests.post")
def test_pull_valid(mock_post, monkeypatch, filled_section):
    monkeypatch.setattr("getpass.getpass", lambda _: "test")
    test_data = {"sigumah.json": "yup"}
    fake_response = MagicMock()
    fake_response.status_code = 200
    fake_response.json.return_value = test_data
    fake_response.return_value = test_data
    mock_post.return_value = fake_response

    sync = Sync("http:/", "sigma@guy.ru", vault_path="test")
    assert sync.pull() is True
    assert mock_post.call_count == 2

    os.remove("test/sigumah.json")


def test_pull_invalid1(monkeypatch, filled_section):
    monkeypatch.setattr("getpass.getpass", lambda _: "wrong")
    sync = Sync("http:/", "sigma@guy.ru", vault_path="test")
    assert sync.pull() is False


@patch("requests.post")
def test_pull_invalid2(mock_post, monkeypatch, filled_section):
    monkeypatch.setattr("getpass.getpass", lambda _: "test")
    fake_response1 = MagicMock()
    fake_response1.status_code = 200
    fake_response1.json.return_value = {"sigumah.json": "yup"}

    fake_response2 = MagicMock()
    fake_response2.status_code = 404
    fake_response2.json.return_value = {}

    mock_post.side_effect = [fake_response1, fake_response2]

    sync = Sync("http:/", "sigma@guy.ru", vault_path="test")
    assert sync.pull() is False

    os.remove("test/sigumah.json")
