"""Data models."""


class Base:
    """Base model."""
    pass


class User(Base):
    """User model."""

    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email

    def to_dict(self) -> dict:
        """Serialize to dict."""
        return {"name": self.name, "email": self.email}


class AdminUser(User):
    """Admin variant."""

    def __init__(self, name: str, email: str, level: int = 1):
        super().__init__(name, email)
        self.level = level
