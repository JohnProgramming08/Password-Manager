from .encryption import Encryption
import json
import os
import getpass
import logging
import shutil


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

    # Ask the user for the proposed master password
    def choose_master_password(self) -> str:
        logging.info(" YOUR MASTER PASSWORD CANNOT BE CHANGED")

        password = ""
        confirm_password = ""
        while not password or confirm_password != password:
            password = getpass.getpass("MASTER PASSWORD: ")
            confirm_password = getpass.getpass("CONFIRM MASTER PASSWORD: ")

            if password != confirm_password:
                logging.error(" PASSWORDS DON'T MATCH")

        return password

    # Set the maximum number of failed password attempts
    def set_attempt_limit(self, attempt_limit: int) -> bool:
        self.init_config_file()

        if type(attempt_limit) != int or attempt_limit < 1:
            logging.error(" ATTEMPT LIMIT MUST BE ABOVE 0")
            return False

        password = self.confirm_master_password()
        if password is None:
            return False

        # Save the users attempt limit
        with open(self.config_path, "w+") as config_file:
            self.config_data["attempt_limit"] = str(attempt_limit)
            self.config_data["attempts"] = "0"
            config_file.write("")
            json.dump(self.config_data, config_file, indent=4)

        logging.info(" ATTEMPT LIMIT SUCCESSFULLY SET")

        return True

    # Ask the user to fill in the config file if not done so already
    def init_config_file(self) -> None:
        if self.is_config_finished():
            return None

        # Config file not filled in
        print("------------------------------------")
        print("PASSWORD MANAGER CONFIG")

        # Set and save the users password
        password = self.choose_master_password()
        password_hash = Encryption.hash_password(password)

        with open(self.config_path, "w+") as config_file:
            self.config_data["password"] = password_hash
            config_file.write("")
            json.dump(self.config_data, config_file, indent=4)

        logging.info(" PASSWORD SUCCESSFULLY SET")

        print("------------------------------------")

    # Confirm the users master password
    def confirm_master_password(self) -> None | str:
        self.init_config_file()
        password = getpass.getpass("MASTER PASSWORD: ")
        expected_hash = self.config_data.get("password")

        if Encryption.verify_password(password, expected_hash):
            self.update_password_attempts(True)
            return password
        else:
            self.update_password_attempts(False)
            logging.error(" COMMAND DENIED")

    # Update a users password attempts, returning if they have reached the limit
    def update_password_attempts(self, correct_password: bool) -> bool:
        if self.config_data.get("attempt_limit") is None:
            return False

        # User has set an attempt limit
        attempts = int(self.config_data["attempts"]) + 1
        attempt_limit = int(self.config_data["attempt_limit"])

        if correct_password:
            self.config_data["attempts"] = "0"
            attempts = 0
        else:
            self.config_data["attempts"] = str(attempts)

        # Save attempts and exit
        if attempts < attempt_limit:
            with open(self.config_path, "w+") as config_file:
                config_file.write("")
                json.dump(self.config_data, config_file, indent=4)
                return False

        # User has reached max failed attempts
        vault_path = self.config_path.split("/")[0]
        shutil.rmtree(vault_path)
        logging.error(" ALL DATA HAS BEEN WIPED")

        return True

    # Allow the user to set an email
    def set_email(self, email: str) -> bool:
        self.init_config_file()
        hashed_email = Encryption.hash_email(email)

        password = self.confirm_master_password()
        if password is None:
            return False

        # Password is vaild
        self.config_data["email"] = hashed_email

        with open(self.config_path, "w") as file:
            file.write("")
            json.dump(self.config_data, file, indent=4)

        return True
