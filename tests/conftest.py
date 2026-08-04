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
