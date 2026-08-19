import os
import json
from api.sync import Sync


# Checking if a user is in the system
def test_user_exists_invalid(empty_config_file):
    sync = Sync("67", "temp", "temp", users_path="test")
    assert sync.user_exists() is False


def test_user_exists_valid(empty_config_file):
    os.makedirs("test/67")
    sync = Sync("67", "temp", "temp", users_path="test")
    assert sync.user_exists() is True

    os.removedirs("test/67")


# Creating the users path directory
def test_create_users_path_dir_invalid(empty_config_file):
    sync = Sync("67", "temp", "temp", users_path="test")
    assert sync.create_users_path_dir() is False


def test_create_users_path_dir_valid():
    sync = Sync("67", "temp", "temp", users_path="test")
    assert sync.create_users_path_dir() is True

    os.removedirs("test")


# Adding a user to the system
def test_add_user_valid1(empty_config_file):
    sync = Sync("sigma", "temp", "temp", users_path="test")
    assert sync.add_user() is True

    os.removedirs("test/sigma")


def test_add_user_valid2():
    sync = Sync("sigma", "temp", "temp", users_path="test")
    assert sync.add_user() is True

    os.removedirs("test/sigma")


def test_add_user_invalid(empty_config_file):
    os.makedirs("test/sigma")
    sync = Sync("sigma", "temp", "temp", users_path="test")
    assert sync.add_user() is False

    os.removedirs("test/sigma")


# Overwriting a section
def test_overwrite_section_valid1(empty_config_file):
    os.makedirs("test/67")
    file_data = {"sigma": "female"}
    sync = Sync("67", "test.json", file_data, users_path="test")
    assert sync.overwrite_section() is True
    assert sync.overwrite_section() is True

    os.remove("test/67/test.json")
    os.removedirs("test/67")


def test_overwrite_section_invalid():
    file_data = {"sigma": "female"}
    sync = Sync("67", "test.json", file_data, users_path="test")
    assert sync.overwrite_section() is False


# Uploading the users data to the server
def test_upload_data(empty_config_file):
    file_data = {"Physics": "A*", "Maths": "A*", "Computer Science": "A*"}
    sync = Sync("42069", "grades.json", file_data, users_path="test")
    sync.upload_data()

    os.remove("test/42069/grades.json")
    os.removedirs("test/42069")


# Fetching all sections belonging to the user
def test_get_all_sections_valid(empty_config_file):
    os.makedirs("test/67")
    with open("test/67/sigma.json", "w+") as file:
        pass

    sync = Sync("67", users_path="test")
    assert sync.get_all_sections() == ["sigma.json"]

    os.remove("test/67/sigma.json")
    os.removedirs("test/67")


def test_get_all_sections_invalid(empty_config_file):
    sync = Sync("67", users_path="test")
    assert sync.get_all_sections() == []


# Fetching the contents of a section
def test_get_section_data_valid(empty_config_file):
    test_data = {"sigma": "female"}
    os.makedirs("test/67")
    with open("test/67/sigma.json", "w+") as file:
        json.dump(test_data, file, indent=4)

    sync = Sync("67", file_name="sigma.json", users_path="test")
    assert sync.get_section_data() == test_data

    os.remove("test/67/sigma.json")
    os.removedirs("test/67")


# Fetching the contents of a section
def test_get_section_data_invalid(empty_config_file):
    test_data = {"sigma": "female"}
    os.makedirs("test/67")
    with open("test/67/sigma.json", "w+") as file:
        json.dump(test_data, file, indent=4)

    sync = Sync("67", file_name="sigma2.json", users_path="test")
    assert sync.get_section_data() == {}

    os.remove("test/67/sigma.json")
    os.removedirs("test/67")
