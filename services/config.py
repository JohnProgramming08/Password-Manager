from .encryption import Encryption
import json
import os


class Config:
    def __init__(self, config_path="data/config.json"):
        self.config_data = None
        self.config_path = config_path

    # Check if the configuration file is finished
    def is_config_finished(self) -> bool:
        try:
            with open(self.config_path, "r") as config_file:
                self.config_data = json.load(config_file)
                return self.config_data.get("password") is not None

        except FileNotFoundError:
            config_dir = self.config_path.split("/")[0]
            os.makedirs(config_dir)

        except json.JSONDecodeError:
            pass

        finally:
            self.config_data = {}

        return False

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
        with open(self.config_path, "w+") as config_file:
            self.config_data["password"] = password_hash
            json.dump(self.config_data, config_file, indent=4)

        print("------------------------------------")
