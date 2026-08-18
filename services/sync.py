import json
import requests
import os
from services import Config, Encryption


class Sync:
    def __init__(self, remote_url: str, vault_path="data"):
        self.remote_url = remote_url
        self.vault_path = vault_path

        config = Config(config_path=f"{vault_path}/config.json")
        self.password = config.confirm_master_password()
        self.email_hash = config.get_email_hash()

    # Upload the given file to the remote, returning if successful
    def upload_file(self, file_name: str) -> int:
        # Fetch file data
        file_path = f"{self.vault_path}/{file_name}"
        with open(file_path, "r") as file:
            file_data = json.load(file)

        payload = {"file_contents": file_data, "password": self.password}
        payload_json = json.dumps(payload)

        url = f"{self.remote_url}/upload/{self.email_hash}/{file_name}"
        response = requests.post(url, data=payload_json)

        return response.status_code

    # Upload all of the users data to the remote, returning if successful
    def push(self) -> bool:
        if self.password is None or self.email_hash is None:
            return False

        sections = os.listdir(self.vault_path)
        for file_name in sections:
            upload_success = self.upload_file(file_name) == 200
            if not upload_success:
                return False

        return True

    # Download and save the contents of a given file, returning if successful
    def download_file(self, file_name: str) -> int:
        payload_json = json.dumps({"password": self.password})
        url = f"{self.remote_url}/download_file/{self.email_hash}/{file_name}"
        response = requests.post(url, data=payload_json)

        try:
            data = response.json()
            file_path = f"{self.vault_path}/{file_name}"
            with open(file_path, "w") as file:
                file.write("")
                json.dump(data, file, indent=4)

        except:
            pass

        return response.status_code

    # Return a list of all backed up file names
    def get_file_names(self) -> list:
        payload_json = json.dumps({"password": self.password})
        url = f"{self.remote_url}/list_sections/{self.email_hash}"
        response = requests.post(url, data=payload_json)

        data_dict = response.json()
        return [key for key in data_dict]

    # Download all backed up data, returning if successful
    def pull(self) -> bool:
        if self.password is None or self.email_hash is None:
            return False

        file_names = self.get_file_names()

        for name in file_names:
            status_code = self.download_file(name)
            if status_code != 200:
                return False

        return True
