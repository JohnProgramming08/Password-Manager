import os
import json


class Sync:
    def __init__(
        self,
        password_hash: str,
        file_name="",
        file_contents={},
        users_path="users",
    ):
        self.password_hash = password_hash
        self.file_name = file_name
        self.file_contents = file_contents
        self.users_path = users_path

    # Return whether or not a user is in the system
    def user_exists(self) -> bool:
        user_dir_path = f"{self.users_path}/{self.password_hash}"
        return os.path.exists(user_dir_path)

    # Create users_path dir if it doesn't exist returning if it was created
    def create_users_path_dir(self) -> bool:
        if os.path.exists(self.users_path):
            return False

        os.makedirs(self.users_path)
        return True

    # Add a user to the system, returning if successful
    def add_user(self) -> bool:
        try:
            user_dir_path = f"{self.users_path}/{self.password_hash}"
            os.makedirs(user_dir_path)
            return True

        except:
            return False

    # Overwrite a section in a users vault, returning if successful
    def overwrite_section(self) -> bool:
        try:
            file_path = (
                f"{self.users_path}/{self.password_hash}/{self.file_name}"
            )
            with open(file_path, "w+") as file:
                json.dump(self.file_contents, file, indent=4)

            return True

        except:
            return False

    # Upload the users data to the server
    def upload_data(self):
        self.create_users_path_dir()
        if not self.user_exists():
            self.add_user()

        self.overwrite_section()

    # Fetch all sections belonging to the user
    def get_all_sections(self) -> list:
        try:
            dir_path = f"{self.users_path}/{self.password_hash}"
            return os.listdir(dir_path)

        except:
            return []

    # Return the contents of the given section
    def get_section_data(self) -> dict:
        try:
            section_path = (
                f"{self.users_path}/{self.password_hash}/{self.file_name}"
            )
            if not os.path.exists(section_path):
                return {}

            with open(section_path, "r") as file:
                data = json.load(file)

            return data

        except:
            return {}
