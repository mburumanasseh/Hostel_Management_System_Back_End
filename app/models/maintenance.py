"""
Maintenance Request model.
"""

from datetime import datetime
from app.extensions import db


class MaintenanceRequest(db.Model):
    __tablename__ = "maintenance_requests"

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

    title = db.Column(
        db.String(150),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=False
    )

    priority = db.Column(
        db.Enum(
            "Low",
            "Medium",
            "High",
            "Urgent",
            name="priority_levels"
        ),
        default="Medium"
    )

    status = db.Column(
        db.Enum(
            "Pending",
            "In Progress",
            "Resolved",
            name="maintenance_status"
        ),
        default="Pending"
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
        back_populates="maintenance_requests"
    )

    room = db.relationship(
        "Room",
        back_populates="maintenance_requests"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "status": self.status
        }