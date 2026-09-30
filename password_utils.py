"""Simple password hashing helpers using Python's standard library."""

import hashlib
import hmac
import secrets


_ALGORITHM = "pbkdf2_sha256"
_ITERATIONS = 310_000


def hash_password(password):
    """Create a salted PBKDF2 hash suitable for storing in SQLite."""
    salt = secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), bytes.fromhex(salt), _ITERATIONS
    ).hex()
    return f"{_ALGORITHM}${_ITERATIONS}${salt}${digest}"


def verify_password(password, stored_password):
    """Verify a hashed password and identify legacy plain-text passwords."""
    if not stored_password.startswith(f"{_ALGORITHM}$"):
        return hmac.compare_digest(password, stored_password), False

    try:
        algorithm, iterations_text, salt, expected_digest = stored_password.split("$", 3)
        if algorithm != _ALGORITHM:
            return False, False
        digest = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            bytes.fromhex(salt),
            int(iterations_text),
        ).hex()
    except (ValueError, TypeError):
        return False, False

    return hmac.compare_digest(digest, expected_digest), True
