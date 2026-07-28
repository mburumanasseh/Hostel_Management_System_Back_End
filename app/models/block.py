"""
Hostel Block model.
"""

from datetime import datetime
from app.extensions import db


class Block(db.Model):
    __tablename__ = "blocks"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(
        db.String(20),
        unique=True,
        nullable=False
    )

    gender = db.Column(
        db.Enum(
            "Male",
            "Female",
            "Mixed",
            name="block_gender"
        )
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

    rooms = db.relationship(
        "Room",
        back_populates="block",
        cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender
        }