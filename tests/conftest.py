import pytest
import os
import json
from services import Config, Encryption
from api import create_app
from api.database import Insert


# Empty config file at test/config.json
@pytest.fixture
def empty_config_file():
    # Setup empty test file
    os.makedirs("test")
    file = open("test/config.json", "w+")
    file.close()

    yield None

    # Remove file and directory after test
    try:
        os.remove("test/config.json")
        os.removedirs("test")
    except:
        pass


# Filled in config file at test/config.json
@pytest.fixture
def filled_config_file(empty_config_file):
    password_hash = Encryption.hash_password("test")
    test_config_data = {"password": password_hash}
    with open("test/config.json", "w") as file:
        json.dump(test_config_data, file, indent=4)


# Filled in config file with an empty section
@pytest.fixture
def empty_section(filled_config_file):
    file = open("test/empty.json", "w+")
    file.write("{}")
    file.close()


# Section with 3 filled fields
@pytest.fixture
def filled_section(filled_config_file):
    test_data = {
        "username": Encryption.encrypt_string("sigma", "test").decode(),
        "password": Encryption.encrypt_string("MORE SIGMA", "test").decode(),
        "email": Encryption.encrypt_string("test", "test").decode(),
    }
    with open("test/filled.json", "w+") as file:
        json.dump(test_data, file, indent=4)

    yield None

    try:
        os.remove("test/filled.json")
    except:
        pass


# Filled in config file with 3 empty sections
@pytest.fixture
def many_empty_sections(filled_config_file):
    file_names = ["one", "two", "three"]
    for file_name in file_names:
        with open(f"test/{file_name}.json", "w+") as file:
            pass

    yield None

    for file_name in file_names:
        try:
            os.remove(f"test/{file_name}.json")
        except:
            pass


# Filled in config with attempts limit and attempts set
@pytest.fixture
def attempt_limit_config(empty_config_file):
    data = {"username": "test", "attempts_limit": "3", "attempts": "0"}
    with open("test/config.json", "w") as config_file:
        config_file.write("")
        json.dump(data, config_file, indent=4)

    yield None


# API testing
@pytest.fixture
def app():
    app = create_app(
        {
            "TESTING": True,
            "WTF_CSRF_ENABLED": False,  # <--- Disable CSRF for easier testing
            "SECRET_KEY": "test-secret",
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        }
    )
    yield app


@pytest.fixture
def client(app):
    res_client = app.test_client()

    return res_client


# Client with 3 filled sections under hash 67
@pytest.fixture
def many_filled_sections_client(client):
    test_data = {"super": "sigma", "iron": "man", "tony": "stark"}
    section_names = ["one", "two", "three"]

    os.makedirs("users/67")
    for name in section_names:
        path = f"users/67/{name}.json"
        file = open(path, "w")
        json.dump(test_data, file, indent=4)
        file.close()

    yield client

    for name in section_names:
        path = f"users/67/{name}.json"
        os.remove(path)
    os.removedirs("users/67")


# App with 3 users
@pytest.fixture
def many_users_app(app):
    with app.app_context():
        Insert.insert_user("sigma", "male")
        Insert.insert_user("Dylan", "Scully")
        Insert.insert_user("top", "grades")

    return app
