import base64
import hashlib
import hmac
import os


SALT_LENGTH = 16
KEY_LENGTH = 64

SCRYPT_N = 2**14
SCRYPT_R = 8
SCRYPT_P = 1


def hash_password(password: str) -> str:
    salt = os.urandom(SALT_LENGTH)

    password_hash = hashlib.scrypt(
        password.encode("utf-8"),
        salt=salt,
        n=SCRYPT_N,
        r=SCRYPT_R,
        p=SCRYPT_P,
        dklen=KEY_LENGTH,
    )

    encoded_salt = base64.b64encode(salt).decode("utf-8")
    encoded_hash = base64.b64encode(password_hash).decode("utf-8")

    return f"scrypt${encoded_salt}${encoded_hash}"


def verify_password(password: str, password_hash: str) -> bool:
    try:
        algorithm, encoded_salt, encoded_hash = password_hash.split("$")

        if algorithm != "scrypt":
            return False

        salt = base64.b64decode(encoded_salt)
        stored_hash = base64.b64decode(encoded_hash)

        calculated_hash = hashlib.scrypt(
            password.encode("utf-8"),
            salt=salt,
            n=SCRYPT_N,
            r=SCRYPT_R,
            p=SCRYPT_P,
            dklen=len(stored_hash),
        )

        return hmac.compare_digest(
            calculated_hash,
            stored_hash,
        )

    except (ValueError, TypeError):
        return False
