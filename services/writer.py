import os
import json
from .encryption import Encryption
from .config import Config


class Writer:
    # Add a section to the data vault, returning if successful
    @staticmethod
    def add_section(section_name: str, vault_path="data/") -> bool:
        valid_vault = os.path.exists(vault_path)
        valid_section = not os.path.exists(vault_path + section_name + ".json")

        if not valid_section or not valid_vault:
            print("There was an error creating the section.")
            return False

        # Section is valid
        config_service = Config(config_path=vault_path + "config.json")
        password = config_service.confirm_master_password()
        if password is None:
            return False

        with open(f"{vault_path}{section_name}.json", "w+") as file:
            file.write("{}")

        return True

    # Set the value of a field in a section, returning if successful
    @staticmethod
    def set_field(
        section_name: str, field_name: str, value: str, vault_path="data/"
    ) -> bool:
        valid_vault = os.path.exists(vault_path)
        valid_section = os.path.exists(vault_path + section_name + ".json")

        if not valid_vault or not valid_section:
            print("There was an error setting the value of the field.")
            return False

        # Section exists
        config_service = Config()
        password = config_service.confirm_master_password()
        if password is None:
            return False

        encrypted_value = Encryption.encrypt_string(value, password).decode()

        # Save encrypted value
        with open(f"{vault_path}{section_name}.json", "r+") as file:
            section_data = json.load(file)
            section_data[field_name] = encrypted_value
            file.write("")
            json.dump(section_data, file, indent=4)

        return True
