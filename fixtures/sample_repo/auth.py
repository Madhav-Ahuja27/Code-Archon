"""Authentication module for the sample app."""

import hashlib
import os


class UserAuth:
    """Handles user authentication."""

    def __init__(self, secret_key: str):
        self.secret_key = secret_key

    def hash_password(self, password: str) -> str:
        """Hash a plain-text password."""
        salt = os.urandom(16).hex()
        hashed = hashlib.sha256((password + salt).encode()).hexdigest()
        return f"{salt}:{hashed}"

    def verify_password(self, password: str, stored: str) -> bool:
        """Verify a password against a stored hash."""
        salt, hashed = stored.split(":")
        candidate = hashlib.sha256((password + salt).encode()).hexdigest()
        return candidate == hashed


def create_auth(secret: str) -> UserAuth:
    """Factory function for UserAuth."""
    return UserAuth(secret)
