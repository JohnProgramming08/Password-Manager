import hashlib


class Encryption:
    # Hash the given password
    @staticmethod
    def hash_password(password: str) -> str:
        full_hashed_password = int(
            hashlib.sha256(password.encode("utf-8")).hexdigest(), 16
        )
        password_hash = full_hashed_password % (10**8)

        return str(password_hash)
