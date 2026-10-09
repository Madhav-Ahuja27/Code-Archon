"""API routes."""

from auth import create_auth, UserAuth
from models import User


def login(username: str, password: str) -> bool:
    """Handle login request."""
    auth = create_auth("secret")
    stored = auth.hash_password(password)
    return auth.verify_password(password, stored)


def get_user(user_id: int) -> User:
    """Fetch a user by ID."""
    return User(name="test", email="test@example.com")
