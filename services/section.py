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

    # Return a list of all sections the user has made
    @staticmethod
    def list_sections(vault_path="data/") -> str:
        file_list = os.listdir(vault_path[:-1])
        sections = ""
        for file in file_list:
            section_name = file.split(".")[0]
            if section_name != "config":
                sections += section_name + "\n"

        return sections
