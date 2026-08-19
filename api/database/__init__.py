from .select_db import Select
from .insert_db import Insert
from .create_db import db


class VerifyUser:
    # Verify the users account details
    @staticmethod
    def verify(email_hash: str, password: str) -> bool:
        valid = False
        if Select.email_exists(email_hash) and Select.are_details_correct(
            email_hash, password
        ):
            valid = True
        elif not Select.email_exists(email_hash) and Insert.insert_user(
            email_hash, password
        ):
            valid = True

        return valid
