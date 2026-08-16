from .create_db import User, db


class Insert:
    # Insert a new user into the database, returning if successful
    @staticmethod
    def insert_user(email_hash: str, password_hash: str) -> bool:
        try:
            new_user = User(password_hash=password_hash, email_hash=email_hash)
            db.session.add(new_user)
            db.session.commit()

            return True

        except:
            return False
