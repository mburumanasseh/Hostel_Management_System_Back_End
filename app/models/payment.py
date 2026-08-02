"""
Payment model.
"""

from datetime import datetime
from app.extensions import db


class Payment(db.Model):
    __tablename__ = "payments"

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("students.id"),
        nullable=False
    )

    amount = db.Column(
        db.Numeric(10, 2),
        nullable=False
    )

    semester = db.Column(
        db.String(30),
        nullable=False
    )

    payment_date = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    status = db.Column(
        db.Enum(
            "Pending",
            "Paid",
            "Failed",
            name="payment_status"
        ),
        default="Pending"
    )

    reference_number = db.Column(
        db.String(100),
        unique=True,
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

    # Relationships

    student = db.relationship(
        "Student",
        back_populates="payments"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "student_id": self.student_id,
            "amount": float(self.amount),
            "semester": self.semester,
            "payment_date": self.payment_date,
            "status": self.status,
            "reference_number": self.reference_number
        }
