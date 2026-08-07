import os
from .config import Config


class Section:
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
