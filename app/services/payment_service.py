
from decimal import Decimal

from app.extensions import db
from app.models.payment import Payment
from app.models.student import Student
from app.models.hostel_fee import HostelFee


class PaymentService:

    # =====================================================
    # CREATE PAYMENT
    # =====================================================

    @staticmethod
    def create_payment(
        student_id,
        amount,
        semester,
        reference_number,
        status="Pending"
    ):
        # Check student exists
        student = db.session.get(Student, student_id)

        if not student:
            raise ValueError("Student not found")

        # Check reference number
        existing_payment = Payment.query.filter_by(
            reference_number=reference_number
        ).first()

        if existing_payment:
            raise ValueError(
                "Reference number already exists"
            )

        # Validate status
        allowed_statuses = [
            "Pending",
            "Paid",
            "Failed"
        ]

        if status not in allowed_statuses:
            raise ValueError(
                "Invalid payment status"
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

    # =====================================================
    # GET ALL PAYMENTS
    # =====================================================

    @staticmethod
    def get_all_payments():

        return Payment.query.order_by(
            Payment.payment_date.desc()
        ).all()

    # =====================================================
    # GET PAYMENT
    # =====================================================

    @staticmethod
    def get_payment_by_id(payment_id):

        return db.session.get(
            Payment,
            payment_id
        )

    # =====================================================
    # GET STUDENT PAYMENTS
    # =====================================================

    @staticmethod
    def get_student_payments(student_id):

        student = db.session.get(
            Student,
            student_id
        )

        if not student:
            raise ValueError(
                "Student not found"
            )

        return Payment.query.filter_by(
            student_id=student_id
        ).order_by(
            Payment.payment_date.desc()
        ).all()

    # =====================================================
    # UPDATE PAYMENT STATUS
    # =====================================================

    @staticmethod
    def update_status(
        payment_id,
        status
    ):

        payment = db.session.get(
            Payment,
            payment_id
        )

        if not payment:
            raise ValueError(
                "Payment not found"
            )

        allowed_statuses = [
            "Pending",
            "Paid",
            "Failed"
        ]

        if status not in allowed_statuses:
            raise ValueError(
                "Invalid payment status"
            )

        payment.status = status

        db.session.commit()

        return payment

        # =====================================================
    # GET STUDENT FINANCIAL STATUS
    # =====================================================

    @staticmethod
    def get_student_financial_status(
        student_id,
        semester
    ):

        # ================================================
        # CHECK STUDENT
        # ================================================

        student = db.session.get(
            Student,
            student_id
        )

        if not student:
            raise ValueError(
                "Student not found"
            )

        # ================================================
        # FIND HOSTEL FEE FOR SEMESTER
        # ================================================

        hostel_fee = HostelFee.query.filter_by(
            semester=semester
        ).first()

        if not hostel_fee:
            raise ValueError(
                "Hostel fee not found for this semester"
            )

        # ================================================
        # GET PAYMENTS FOR THIS STUDENT + SEMESTER
        # ================================================

        payments = Payment.query.filter_by(
            student_id=student_id,
            semester=semester
        ).all()

        # ================================================
        # CALCULATE PAID AMOUNT
        # ================================================

        total_paid = sum(
            (
                payment.amount
                for payment in payments
                if payment.status == "Paid"
            ),
            Decimal("0.00")
        )

        # ================================================
        # CALCULATE PENDING AMOUNT
        # ================================================

        total_pending = sum(
            (
                payment.amount
                for payment in payments
                if payment.status == "Pending"
            ),
            Decimal("0.00")
        )

        # ================================================
        # CALCULATE FAILED AMOUNT
        # ================================================

        total_failed = sum(
            (
                payment.amount
                for payment in payments
                if payment.status == "Failed"
            ),
            Decimal("0.00")
        )

        # ================================================
        # REQUIRED HOSTEL FEE
        # ================================================

        required_fee = Decimal(
            str(hostel_fee.amount)
        )

        # ================================================
        # CALCULATE BALANCE
        # ================================================

        balance = required_fee - total_paid

        # Prevent negative balance
        if balance < Decimal("0.00"):
            balance = Decimal("0.00")

        # ================================================
        # DETERMINE FINANCIAL STATUS
        # ================================================

        if total_paid >= required_fee:
            financial_status = "Paid"

        elif total_paid > Decimal("0.00"):
            financial_status = "Partially Paid"

        elif total_pending > Decimal("0.00"):
            financial_status = "Pending"

        else:
            financial_status = "No Payment"

        # ================================================
        # RETURN FINANCIAL SUMMARY
        # ================================================

        return {
            "student_id": student.id,

            "registration_number": (
                student.registration_number
            ),

            "first_name": (
                student.user.first_name
                if student.user
                else None
            ),

            "last_name": (
                student.user.last_name
                if student.user
                else None
            ),

            "email": (
                student.user.email
                if student.user
                else None
            ),

            "semester": semester,

            "required_fee": float(
                required_fee
            ),

            "total_paid": float(
                total_paid
            ),

            "total_pending": float(
                total_pending
            ),

            "total_failed": float(
                total_failed
            ),

            "balance": float(
                balance
            ),

            "payment_count": len(
                payments
            ),

            "financial_status": financial_status
        }

    # =====================================================
    # DELETE PAYMENT
    # =====================================================

    @staticmethod
    def delete_payment(payment_id):

        payment = db.session.get(
            Payment,
            payment_id
        )

        if not payment:
            raise ValueError(
                "Payment not found"
            )

        db.session.delete(payment)

        db.session.commit()

        return True