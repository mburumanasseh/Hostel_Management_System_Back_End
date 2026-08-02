from app.extensions import db
from app.models.payment import Payment
from app.models.student import Student


class PaymentService:

    @staticmethod
    def create_payment(
        student_id,
        amount,
        semester,
        reference_number,
        status="Pending"
    ):
        # Check student exists
        student = Student.query.get(student_id)

        if not student:
            raise ValueError("Student not found")

        # Check reference number is unique
        existing_payment = Payment.query.filter_by(
            reference_number=reference_number
        ).first()

        if existing_payment:
            raise ValueError(
                "Reference number already exists"
            )

        payment = Payment(
            student_id=student_id,
            amount=amount,
            semester=semester,
            reference_number=reference_number,
            status=status
        )

        db.session.add(payment)
        db.session.commit()

        return payment

    @staticmethod
    def get_all_payments():

        return Payment.query.order_by(
            Payment.payment_date.desc()
        ).all()

    @staticmethod
    def get_payment_by_id(payment_id):

        return Payment.query.get(payment_id)

    @staticmethod
    def get_student_payments(student_id):

        student = Student.query.get(student_id)

        if not student:
            raise ValueError("Student not found")

        return Payment.query.filter_by(
            student_id=student_id
        ).order_by(
            Payment.payment_date.desc()
        ).all()

    @staticmethod
    def update_status(payment_id, status):

        payment = Payment.query.get(payment_id)

        if not payment:
            raise ValueError("Payment not found")

        payment.status = status

        db.session.commit()

        return payment

    @staticmethod
    def delete_payment(payment_id):

        payment = Payment.query.get(payment_id)

        if not payment:
            raise ValueError("Payment not found")

        db.session.delete(payment)

        db.session.commit()
