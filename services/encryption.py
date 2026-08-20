import hashlib
from cryptography.fernet import Fernet
import base64
from argon2 import PasswordHasher
from argon2.low_level import hash_secret_raw, Type


class Encryption:
    # Hash the given password
    @staticmethod
    def hash_password(password: str) -> str:
        hasher = PasswordHasher(
            time_cost=3,
            memory_cost=65536,  # 64 MiB
            parallelism=4,
            hash_len=32,
            salt_len=16,
        )

        password_hash = hasher.hash(password)

        return str(password_hash)

    # Verify a given password
    @staticmethod
    def verify_password(password: str, expected_hash: str) -> bool:
        hasher = PasswordHasher(
            time_cost=3,
            memory_cost=65536,  # 64 MiB
            parallelism=4,
            hash_len=32,
            salt_len=16,
        )

        try:
            hasher.verify(expected_hash, password)
            return True
        except:
            return False

    # Generate the encryption/decryption key from the master password
    @staticmethod
    def generate_key(password: str) -> bin:
        FIXED_SALT = b"saltywalty123456"
        raw_key = hash_secret_raw(
            secret=password.encode(),
            salt=FIXED_SALT,
            time_cost=3,
            memory_cost=64 * 1024,  # 64 MiB
            parallelism=1,
            hash_len=32,
            type=Type.ID,
        )
        fernet_key = base64.urlsafe_b64encode(raw_key)

        return fernet_key

    # Encrypt the given string using the users encryption key
    @staticmethod
    def encrypt_string(strng: str, password: str) -> bin:
        key = Encryption.generate_key(password)
        f = Fernet(key)
        binary = strng.encode("utf-8")
        ciphertext = f.encrypt(binary)

        return ciphertext

    # Decrypt the given string using the users encryption key
    @staticmethod
    def decrypt_string(ciphertext: bin, password: str) -> str:
        key = Encryption.generate_key(password)
        f = Fernet(key)
        plaintext = f.decrypt(ciphertext)

        return plaintext.decode()

    # Hash the given email with SHA256
    @staticmethod
    def hash_email(email: str) -> str:
        full_hashed_email = int(
            hashlib.sha256(email.encode("utf-8")).hexdigest(), 16
        )

        hashed_email = full_hashed_email % 100000000

        return str(hashed_email)
