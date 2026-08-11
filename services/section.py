import os
import logging
from .config import Config


class Section:
    # Add a section to the data vault, returning if successful
    @staticmethod
    def add_section(section_name: str, vault_path="data/") -> bool:
        valid_vault = os.path.exists(vault_path)
        valid_section = not os.path.exists(vault_path + section_name + ".json")

        if not valid_section or not valid_vault:
            logging.error(" SECTION COULD NOT BE CREATED")
            return False

        # Section is valid
        config_service = Config(config_path=vault_path + "config.json")
        password = config_service.confirm_master_password()
        if password is None:
            return False

        with open(f"{vault_path}{section_name}.json", "w+") as file:
            file.write("{}")

        logging.info(f" SECTION CREATED - {section_name}")

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

        return sections[:-1]

    # Attempt to remove a section, returning if successful
    @staticmethod
    def remove_section(section_name: str, vault_path="data/") -> bool:
        if not os.path.exists(f"{vault_path}{section_name}.json"):
            logging.error(" SECTION DOES NOT EXIST")
            return False

        config_service = Config(config_path=vault_path + "config.json")
        password = config_service.confirm_master_password()
        if password is None:
            return False

        os.remove(f"{vault_path}{section_name}.json")
        logging.info(f" SECTION REMOVED - {section_name}")

        return True
