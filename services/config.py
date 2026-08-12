from .encryption import Encryption
import json
import os
import getpass
import logging


class Config:
    def __init__(self, config_path="data/config.json"):
        self.config_data = None
        self.config_path = config_path

    # Check if the configuration file is finished
    def is_config_finished(self) -> bool:
        vault_path = self.config_path.split("/")[0] + "/"
        # Config file does not exist
        if not os.path.exists(self.config_path):
            self.config_data = {}
            if not os.path.exists(vault_path):
                os.makedirs(vault_path[:-1])

            return False

        # Config file exists
        try:
            with open(self.config_path, "r") as config_file:
                self.config_data = json.load(config_file)
                return self.config_data.get("password") is not None

        # Config file is empty
        except json.JSONDecodeError:
            self.config_data = {}
            return False

    # Set the users master password
    def set_master_password(self) -> str:
        logging.info(" YOUR MASTER PASSWORD CANNOT BE CHANGED")

        password = ""
        confirm_password = ""
        while not password or confirm_password != password:
            password = getpass.getpass("MASTER PASSWORD: ")
            confirm_password = getpass.getpass("CONFIRM MASTER PASSWORD: ")

            if password != confirm_password:
                logging.error(" PASSWORDS DON'T MATCH")

        # Save the users password
        password_hash = Encryption.hash_password(password)
        with open(self.config_path, "w+") as config_file:
            self.config_data["password"] = password_hash
            config_file.write("")
            json.dump(self.config_data, config_file, indent=4)

        logging.info(" PASSWORD SUCCESSFULLY SET")

        return password

    # Set the maximum number of failed password attempts
    def set_failed_attempts_limit(self) -> bool:
        self.init_config_file()

        print(
            "Third parties may attempt to access your data. You can choose a failed password attempt limit that takes action after x failed attempts"
        )
        keep_going = input("Would you like to set an attempt limit (Y/N)? ")
        if keep_going != "Y":
            return False

        # User would like to set an attempt limit
        attempt_limit = input("ATTEMPT LIMIT: ")
        if not attempt_limit.isdigit():
            logging.error(" YOUR INPUT MUST BE AN INTEGER")
            return False

        password = self.confirm_master_password()
        if password is None:
            return False

        # Save the users attempt limit
        with open(self.config_path, "w+") as config_file:
            self.config_data["attempt_limit"] = attempt_limit
            self.config_data["attempts"] = 0
            config_file.write("")
            json.dump(self.config_data, config_file, indent=4)

        return True

    # Ask the user to fill in the config file if not done so already
    def init_config_file(self) -> None:
        if self.is_config_finished():
            return None

        # Config file not filled in
        print("------------------------------------")
        print("PASSWORD MANAGER CONFIG")

        # Set the users password
        password = self.set_master_password()

        print("------------------------------------")

    # Confirm the users master password
    def confirm_master_password(self) -> None | str:
        self.init_config_file()
        password = getpass.getpass("MASTER PASSWORD: ")
        expected_hash = self.config_data.get("password")

        if Encryption.verify_password(password, expected_hash):
            return password
        else:
            logging.error(" COMMAND DENIED")
