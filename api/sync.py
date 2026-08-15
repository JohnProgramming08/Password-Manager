import os


class Sync:
    def __init__(self, password_hash: str, file, users_path="users"):
        self.password_hash = password_hash
        self.file = file
        self.users_path = users_path

        self.create_users_path_dir()
        if self.user_exists():
            self.add_user()

        self.overwrite_section(file)

    # Return whether or not a user is in the system
    def user_exists(self) -> bool:
        user_dir_path = f"users/{self.password_hash}"
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
            user_dir_path = f"users/{self.password_hash}"
            os.makedirs(user_dir_path)
            return True

        except:
            return False

    # Overwrite a section in a users vault, returning if successful
    def overwrite_section(self) -> bool:
        try:
            file = self.file
            file.save(f"users/{self.password_hash}/vault/{file.filename}")
            return True

        except:
            return False
