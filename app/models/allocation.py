"""
Room Allocation model.

Stores room allocation history for students.
"""

from datetime import datetime
from app.extensions import db


class Allocation(db.Model):
    __tablename__ = "room_allocations"

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("students.id"),
        nullable=False
    )

    room_id = db.Column(
        db.Integer,
        db.ForeignKey("rooms.id"),
        nullable=False
    )

    allocation_date = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    checkout_date = db.Column(db.DateTime)

    status = db.Column(
        db.Enum(
            "Active",
            "Completed",
            name="allocation_status"
        ),
        default="Active"
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
        back_populates="allocations"
    )

    room = db.relationship(
        "Room",
        back_populates="allocations"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "student_id": self.student_id,
            "room_id": self.room_id,
            "allocation_date": self.allocation_date,
            "checkout_date": self.checkout_date,
            "status": self.status
        }