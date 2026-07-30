"""
Student model.

Stores student information.
"""

from datetime import datetime
from app.extensions import db


class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        unique=True
    )

    registration_number = db.Column(
        db.String(30),
        unique=True,
        nullable=False
    )

    gender = db.Column(db.Enum(
        "Male",
        "Female",
        name="gender_types"
    ))

    phone = db.Column(db.String(20))

    course = db.Column(db.String(100))

    year_of_study = db.Column(db.Integer)

    guardian_name = db.Column(db.String(100))

    guardian_phone = db.Column(db.String(20))

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

    user = db.relationship(
        "User",
        back_populates="student"
    )

    allocations = db.relationship(
        "Allocation",
        back_populates="student",
        cascade="all, delete-orphan"
    )

    payments = db.relationship(
        "Payment",
        back_populates="student",
        cascade="all, delete-orphan"
    )

    maintenance_requests = db.relationship(
        "MaintenanceRequest",
        back_populates="student",
        cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "registration_number": self.registration_number,
            "gender": self.gender,
            "phone": self.phone,
            "course": self.course,
            "year_of_study": self.year_of_study,
            "guardian_name": self.guardian_name,
            "guardian_phone": self.guardian_phone,
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