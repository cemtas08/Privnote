import hashlib
import random
import string

def generate_md5_hash(input_string: str) -> str:
    """
    Generate an MD5 hash for the given input string.

    Args:
        input_string (str): The input string to hash.

    Returns:
        str: The resulting MD5 hash in hexadecimal format.
    """
    return hashlib.md5(input_string.encode()).hexdigest()


def generate_random_str(length: int) -> str:
    """
    Generate a random alphanumeric string of the specified length.

    Args:
        length (int): The desired length of the random string.

    Returns:
        str: A randomly generated alphanumeric string.
    """
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))
