from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.backends import default_backend
from base64 import b64encode, b64decode
import os

# Constants
KEY_SIZE = 32  # AES-256
IV_SIZE = 16
SALT_SIZE = 16
ITERATIONS = 100_000

def _derive_key(password: str, salt: bytes) -> bytes:
    """
    Derive a cryptographic key from a password and salt.
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEY_SIZE,
        salt=salt,
        iterations=ITERATIONS,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

def encrypt(plain_text: str, password: str) -> str:
    """
    Encrypt a string using AES CBC mode with the provided password.

    Returns:
        A base64-encoded string containing salt + iv + ciphertext.
    """
    salt = os.urandom(SALT_SIZE)
    iv = os.urandom(IV_SIZE)
    key = _derive_key(password, salt)

    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(plain_text.encode()) + padder.finalize()

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    cipher_text = encryptor.update(padded_data) + encryptor.finalize()

    encrypted_data = salt + iv + cipher_text
    return b64encode(encrypted_data).decode()

def decrypt(encrypted_data_b64: str, password: str) -> str:
    """
    Decrypt a string encrypted by the `encrypt` function.

    Args:
        encrypted_data_b64: The base64 string from `encrypt`.

    Returns:
        The decrypted plaintext string.
    """
    encrypted_data = b64decode(encrypted_data_b64)
    salt = encrypted_data[:SALT_SIZE]
    iv = encrypted_data[SALT_SIZE:SALT_SIZE+IV_SIZE]
    cipher_text = encrypted_data[SALT_SIZE+IV_SIZE:]

    key = _derive_key(password, salt)

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded_plain_text = decryptor.update(cipher_text) + decryptor.finalize()

    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    plain_text = unpadder.update(padded_plain_text) + unpadder.finalize()

    return plain_text.decode()
