"""
Room model.
"""

from datetime import datetime
from app.extensions import db


class Room(db.Model):
    __tablename__ = "rooms"

    id = db.Column(db.Integer, primary_key=True)

    block_id = db.Column(
        db.Integer,
        db.ForeignKey("blocks.id"),
        nullable=False
    )

    room_number = db.Column(
        db.String(20),
        nullable=False
    )

    floor = db.Column(db.Integer)

    capacity = db.Column(db.Integer)

    occupied = db.Column(
        db.Integer,
        default=0
    )

    status = db.Column(
        db.Enum(
            "Available",
            "Occupied",
            "Maintenance",
            name="room_status"
        ),
        default="Available"
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

    block = db.relationship(
        "Block",
        back_populates="rooms"
    )

    allocations = db.relationship(
        "Allocation",
        back_populates="room",
        cascade="all, delete-orphan"
    )

    maintenance_requests = db.relationship(
        "MaintenanceRequest",
        back_populates="room",
        cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "room_number": self.room_number,
            "floor": self.floor,
            "capacity": self.capacity,
            "occupied": self.occupied,
            "status": self.status,
            "block": self.block.to_dict() if self.block else None
        }