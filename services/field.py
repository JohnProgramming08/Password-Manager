from .encryption import Encryption
from .config import Config
import os
import json


class Field:
    # Get the value of a specific field
    @staticmethod
    def get_value(section: str, field: str, vault_path="data/") -> str | None:
        valid_section = os.path.exists(vault_path + section + ".json")
        valid_vault = os.path.exists(vault_path)

        if not valid_section or not valid_vault:
            print("There was an error accessing the section.")
            return None

        # Check user password
        config_service = Config(config_path=vault_path + "config.json")
        password = config_service.confirm_master_password()
        if password is None:
            return None

        # Section and user password are both valid
        with open(f"{vault_path}{section}.json", "r") as file:
            section_data = json.load(file)

        # Decrypt value
        encrypted_value = section_data.get(field)
        if encrypted_value is None:
            return "empty"

        encrypted_value = encrypted_value.encode("utf-8")
        decrypted_value = Encryption.decrypt_string(encrypted_value, password)

        return decrypted_value

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
        config_service = Config(config_path=vault_path + "config.json")
        password = config_service.confirm_master_password()
        if password is None:
            return False

        encrypted_value = Encryption.encrypt_string(value, password).decode()

        # Save encrypted value
        with open(f"{vault_path}{section_name}.json", "r") as file:
            section_data = json.load(file)
            section_data[field_name] = encrypted_value

        with open(f"{vault_path}{section_name}.json", "w") as file:
            file.write("")
            json.dump(section_data, file, indent=4)

        return True
