"""
User model.

Stores authentication details and system roles.
"""

from datetime import datetime
from app.extensions import db


class User(db.Model):
    __tablename__ = "users"

    # Primary Key
    id = db.Column(db.Integer, primary_key=True)

    # Basic Information
    first_name = db.Column(db.String(100), nullable=False)

    last_name = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)

    password = db.Column(db.String(255), nullable=False)

    role = db.Column(
        db.Enum(
            "admin",
            "warden",
            "finance",
            "student",
            name="user_roles"
        ),
        nullable=False,
        default="student"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    # Relationships
    student = db.relationship(
        "Student",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "role": self.role,
        }