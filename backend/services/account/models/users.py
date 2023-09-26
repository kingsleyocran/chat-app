from datetime import datetime

import sqlalchemy as sq
from werkzeug.security import check_password_hash, generate_password_hash

from core import setup


class Users(setup.Base):
    __tablename__ = "users"
    id = sq.Column(sq.Integer, primary_key=True)
    username = sq.Column(
        sq.String,
        unique=True,
        nullable=False,
    )
    email = sq.Column(sq.String, nullable=False)
    hash_password = sq.Column(sq.String, nullable=False)
    is_admin = sq.Column(sq.Boolean, default=False)
    is_a_star = sq.Column(sq.Boolean, default=False)
    is_email_verified = sq.Column(sq.Boolean, default=False)
    joined_at = sq.Column(sq.DateTime, nullable=False, default=datetime.now())

    def __str__(self) -> str:
        return f"{self.id}-{self.username}"

    @staticmethod
    def generate_hash_password(password: str) -> str:
        encrypted_password = generate_password_hash(password)
        return encrypted_password

    @staticmethod
    def verify_password(hash_password: str, password: str) -> bool:
        return check_password_hash(hash_password, password)
