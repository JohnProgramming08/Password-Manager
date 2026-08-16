from .create_db import db, User
from services.encryption import Encryption


class Select:
    # Check if the email hash is in the database
    @staticmethod
    def email_exists(email_hash: str) -> bool:
        found_user = User.query.filter(User.email_hash == email_hash).first()
        return found_user is not None

    # Check if the users details are correct
    @staticmethod
    def are_details_correct(email_hash: str, password: str) -> bool:
        found_user = User.query.filter(
            (User.email_hash == email_hash)
            & (Encryption.verify_password(password, User.password_hash))
        ).first()
        return found_user is not None
