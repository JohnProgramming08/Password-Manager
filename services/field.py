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

    # Return a list of all fields in a particular section
    @staticmethod
    def list_fields_in_section(section: str, vault_path="data/") -> str:
        file_name = vault_path + section + ".json"
        if not os.path.exists(file_name):
            return ""

        with open(file_name, "r") as file:
            data = json.load(file)

        fields = ""
        for key in data:
            fields += f"{section} {key}\n"

        return fields

    # Return a list of all fields and their associated sections
    def list_fields(vault_path="data/") -> str:
        fields = ""
        sections = os.listdir(vault_path)

        for section in sections:
            # Don't output config fields
            if section == "config.json":
                continue

            section_name = section.split(".")[0]

            file_path = f"{vault_path}{section}"
            with open(file_path, "r") as file:
                data = json.load(file)

            for key in data:
                fields += f"[{section_name}] {key}\n"

        return fields

    # Remove a field from a section, returning if successful
    def remove_field(
        section_name: str, field_name: str, vault_path="data/"
    ) -> bool:
        if not os.path.exists(f"{vault_path}{section_name}.json"):
            return False

        config_service = Config(config_path=vault_path + "config.json")
        password = config_service.confirm_master_password()
        if password is None:
            return

        # Fetch the section data
        file_name = f"{vault_path}{section_name}.json"
        with open(file_name, "r") as file:
            file_data = json.load(file)
            if not file_data.get(field_name):
                return False

        # Remove the given field
        with open(file_name, "w") as file:
            del file_data[field_name]
            file.write("")
            json.dump(file_data, file, indent=4)
