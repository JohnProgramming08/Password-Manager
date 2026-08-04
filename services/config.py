from encryption import Encryption
import json


class Config:
    def __init__(self):
        self.config_data = None

    # Check if the configuration file is finished
    def is_config_finished(self) -> bool:
        with open("data/config.json", "r") as config_file:
            self.config_data = json.load(config_file)

            return self.config_data.get("password", "unset") != "unset"

    # Ask the user for their new master password
    def get_master_password(self) -> str:
        print("YOUR MASTER PASSWORD CANNOT BE CHANGED")

        password = ""
        confirm_password = ""
        while not password or confirm_password != password:
            password = input("MASTER PASSWORD: ")
            confirm_password = input("CONFIRM MASTER PASSWORD: ")

        return password

    # Ask the user to fill in the config file if not done so already
    def init_config_file(self) -> None:
        if self.is_config_finished():
            return None

        # Config file not filled in
        print("------------------------------------")
        print("PASSWORD MANAGER CONFIG")

        password = self.get_master_password()
        password_hash = Encryption.hash_password(password)

        # Save password
        with open("data/config.json", "w") as config_file:
            self.config_data["password"] = password_hash
            json.dump(self.config_data, config_file, indent=4)

        print("------------------------------------")
