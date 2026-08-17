import json
import requests
import os
from services import Config, Encryption


class Sync:
    def __init__(self, remote_url: str, email: str, vault_path="data"):
        self.remote_url = remote_url
        self.vault_path = vault_path
        self.email_hash = Encryption.hash_email(email)

        config = Config(config_path=f"{vault_path}/config.json")
        self.password = config.confirm_master_password()

    # Upload the given file to the remote, returning if successful
    def upload_file(self, file_name: str) -> bool:
        # Fetch file data
        with open(file_name, "r") as file:
            file_data = json.load(file)
        payload = json.dumps(file_data)

        url = f"{self.remote_url}/upload/{self.email_hash}/{self.password}/{file_name}"
        response = requests.post(url, data=payload)

        return response.status_code == 200

    # Upload all of the users data to the remote, returning if successful
    def push(self) -> bool:
        if self.password is None:
            return False

        sections = os.listdir(self.vault_path)
        for file_name in sections:
            upload_success = self.upload_file(file_name)
            if not upload_success:
                return False

        return True

    # Download and save the contents of a given file, returning if successful
    def download_file(self, file_name: str) -> bool:
        url = f"{self.remote_url}/download_file/{self.email_hash}/{self.password}/{file_name}"
        response = requests.post(url)

        if response.status_code != 200:
            return False

        data = response.json()
        file_path = f"{self.vault_path}/{file_name}"
        with open(file_path, "w") as file:
            file.write("")
            json.dump(data, file, indent=4)

        return True

    # Return a list of all backed up file names
    def get_file_names(self) -> list:
        url = (
            f"{self.remote_url}/list_sections/{self.email_hash}/{self.password}"
        )
        response = requests.post(url)

        data_dict = response.json()
        return [key for key in data_dict]

    # Download all backed up data, returning if successful
    def pull(self) -> bool:
        file_names = self.get_file_names()

        for name in file_names:
            file_downloaded = self.download_file(name)
            if not file_downloaded:
                return False

        return True
