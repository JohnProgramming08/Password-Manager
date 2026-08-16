from .create_db import User, db
from services import Encryption


class Insert:
    # Insert a new user into the database, returning if successful
    @staticmethod
    def insert_user(email_hash: str, password: str) -> bool:
        try:
            password_hash = Encryption.hash_password(password)
            new_user = User(password_hash=password_hash, email_hash=email_hash)
            db.session.add(new_user)
            db.session.commit()

            return True

        except:
            return False
