import pytest
import os
import json
from services import Config, Encryption


# Empty config file at test/config.json
@pytest.fixture
def empty_config_file():
    # Setup empty test file
    os.makedirs("test")
    file = open("test/config.json", "w+")
    file.close()

    yield None

    # Remove file and directory after test
    os.remove("test/config.json")
    os.removedirs("test")


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
