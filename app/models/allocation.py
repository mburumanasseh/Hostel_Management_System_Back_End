"""
Room Allocation model.

Stores room allocation history for students.
"""

from datetime import datetime

from app.extensions import db


class Allocation(db.Model):
    __tablename__ = "room_allocations"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

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

    checkout_date = db.Column(
        db.DateTime
    )

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

    # ==========================================
    # RELATIONSHIPS
    # ==========================================

    student = db.relationship(
        "Student",
        back_populates="allocations"
    )

    room = db.relationship(
        "Room",
        back_populates="allocations"
    )

    # ==========================================
    # CONVERT TO DICTIONARY
    # ==========================================

    def to_dict(self):
        return {
            "id": self.id,
            "student_id": self.student_id,

            "allocation_date": (
                self.allocation_date.isoformat()
                if self.allocation_date
                else None
            ),

            "checkout_date": (
                self.checkout_date.isoformat()
                if self.checkout_date
                else None
            ),

            "status": self.status,

            # ==================================
            # ROOM INFORMATION
            # ==================================

            "room": {
                "id": self.room.id,
                "room_number": self.room.room_number,
                "floor": self.room.floor,
                "capacity": self.room.capacity,
                "status": self.room.status,

                # ==============================
                # BLOCK INFORMATION
                # ==============================

                "block": {
                    "id": self.room.block.id,
                    "name": self.room.block.name
                }
                if self.room.block
                else None
            }
            if self.room
            else None
        }