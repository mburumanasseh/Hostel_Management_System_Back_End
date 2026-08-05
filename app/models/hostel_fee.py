"""
Hostel Fee model.

Stores the official hostel fee amount for each semester.
"""

from datetime import datetime

from app.extensions import db


class HostelFee(db.Model):
    __tablename__ = "hostel_fees"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    semester = db.Column(
        db.String(30),
        nullable=False,
        unique=True
    )

    amount = db.Column(
        db.Numeric(10, 2),
        nullable=False
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

    def to_dict(self):
        return {
            "id": self.id,
            "semester": self.semester,
            "amount": float(self.amount),
            "created_at": (
                self.created_at.isoformat()
                if self.created_at
                else None
            ),
            "updated_at": (
                self.updated_at.isoformat()
                if self.updated_at
                else None
            )
        }