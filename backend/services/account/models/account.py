from datetime import datetime

import sqlalchemy as sq
from sqlalchemy.orm import relationship

from core import setup


class UserAccount(setup.Base):
    __tablename__ = "account"
    id = sq.Column(sq.Integer, primary_key=True)
    profile_pic = sq.Column(sq.String, nullable=True)
    is_active = sq.Column(sq.Boolean, default=True)
    user_id = sq.Column(sq.Integer, sq.ForeignKey("users.id"))
    user = relationship("Users", backref="users")
    created_at = sq.Column(sq.DateTime, default=datetime.now())
    updated_at = sq.Column(sq.DateTime, default=datetime.now())

    def __str__(self) -> str:
        return f"{self.id}-{self.user.username}"
