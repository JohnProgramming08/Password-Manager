import hashlib
from cryptography.fernet import Fernet
import base64


class Encryption:
    # Hash the given password
    @staticmethod
    def hash_password(password: str) -> str:
        full_hashed_password = int(
            hashlib.sha256(password.encode("utf-8")).hexdigest(), 16
        )
        password_hash = full_hashed_password % (10**8)

        return str(password_hash)

    # Generate the encryption/decryption key from the master password
    @staticmethod
    def generate_key(password: str) -> bin:
        full_hashed_password = int(
            hashlib.sha256(password.encode("utf-8")).hexdigest(), 16
        )
        password_hash = full_hashed_password % (10**32)
        password_hash_binary = str(password_hash).encode("utf-8")

        encoded_hash = base64.urlsafe_b64encode(password_hash_binary)
        return encoded_hash

    # Encrypt the given string using the users encryption key
    @staticmethod
    def encrypt_string(strng: str, password: str) -> bin:
        key = Encryption.generate_key(password)
        f = Fernet(key)
        binary = strng.encode("utf-8")
        ciphertext = f.encrypt(binary)

        return ciphertext


Encryption.encrypt_string("sigma male", "test")
