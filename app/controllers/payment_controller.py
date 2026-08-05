
from flask import request, jsonify
from marshmallow import ValidationError

from app.models.student import Student

from app.schemas.payment_schema import (
    PaymentSchema,
    PaymentStatusSchema
)

from app.services.payment_service import PaymentService

from app.utils.authorization import (
    role_required,
    get_current_user_id
)


payment_schema = PaymentSchema()
payment_status_schema = PaymentStatusSchema()


# =====================================================
# CREATE PAYMENT
# Finance Officer / Admin
# =====================================================

@role_required("finance", "admin")
def create_payment():

    try:

        data = payment_schema.load(
            request.get_json()
        )

        payment = PaymentService.create_payment(
            student_id=data["student_id"],
            amount=data["amount"],
            semester=data["semester"],
            reference_number=data["reference_number"],
            status=data.get(
                "status",
                "Pending"
            )
        )

        return jsonify({
            "message": "Payment recorded successfully",
            "payment": payment.to_dict()
        }), 201

    except ValidationError as error:

        return jsonify({
            "error": error.messages
        }), 400

    except ValueError as error:

        return jsonify({
            "error": str(error)
        }), 409

    except Exception as error:

        return jsonify({
            "error": str(error)
        }), 500


# =====================================================
# GET ALL PAYMENTS
# Finance Officer / Admin
# =====================================================

@role_required("finance", "admin")
def get_all_payments():

    try:

        payments = PaymentService.get_all_payments()

        return jsonify({
            "payments": [
                payment.to_dict()
                for payment in payments
            ]
        }), 200

    except Exception as error:

        return jsonify({
            "error": str(error)
        }), 500


# =====================================================
# GET ONE PAYMENT
# Finance Officer / Admin
# =====================================================

@role_required("finance", "admin")
def get_payment(payment_id):

    try:

        payment = PaymentService.get_payment_by_id(
            payment_id
        )

        if not payment:

            return jsonify({
                "error": "Payment not found"
            }), 404

        return jsonify({
            "payment": payment.to_dict()
        }), 200

    except Exception as error:

        return jsonify({
            "error": str(error)
        }), 500


# =====================================================
# GET STUDENT PAYMENTS
# Finance Officer / Admin
# =====================================================

@role_required("finance", "admin")
def get_student_payments(student_id):

    try:

        payments = PaymentService.get_student_payments(
            student_id
        )

        return jsonify({
            "payments": [
                payment.to_dict()
                for payment in payments
            ]
        }), 200

    except ValueError as error:

        return jsonify({
            "error": str(error)
        }), 404

    except Exception as error:

        return jsonify({
            "error": str(error)
        }), 500


# =====================================================
# UPDATE PAYMENT STATUS
# Finance Officer / Admin
# =====================================================

@role_required("finance", "admin")
def update_payment_status(payment_id):

    try:

        data = payment_status_schema.load(
            request.get_json()
        )

        payment = PaymentService.update_status(
            payment_id=payment_id,
            status=data["status"]
        )

        return jsonify({
            "message": (
                "Payment status updated successfully"
            ),
            "payment": payment.to_dict()
        }), 200

    except ValidationError as error:

        return jsonify({
            "error": error.messages
        }), 400

    except ValueError as error:

        return jsonify({
            "error": str(error)
        }), 404

    except Exception as error:

        return jsonify({
            "error": str(error)
        }), 500


# =====================================================
# DELETE PAYMENT
# Admin only
# =====================================================

@role_required("admin")
def delete_payment(payment_id):

    try:

        PaymentService.delete_payment(
            payment_id
        )

        return jsonify({
            "message": "Payment deleted successfully"
        }), 200

    except ValueError as error:

        return jsonify({
            "error": str(error)
        }), 404

    except Exception as error:

        return jsonify({
            "error": str(error)
        }), 500


# =====================================================
# GET CURRENT STUDENT'S PAYMENTS
# Student only
# =====================================================

@role_required("student")
def get_my_payments():

    try:

        user_id = get_current_user_id()

        student = Student.query.filter_by(
            user_id=user_id
        ).first()

        if not student:

            return jsonify({
                "error": "Student profile not found"
            }), 404

        payments = PaymentService.get_student_payments(
            student.id
        )

        return jsonify({
            "payments": [
                payment.to_dict()
                for payment in payments
            ]
        }), 200

    except Exception as error:

        return jsonify({
            "error": str(error)
        }), 500


# =====================================================
# GET CURRENT STUDENT FINANCIAL STATUS
# Student only
#
# Example:
# GET /api/payments/my/financial-status
#     ?semester=Semester%201%202026
# =====================================================

@role_required("student")
def get_my_financial_status():

    try:

        semester = request.args.get(
            "semester"
        )

        if not semester:

            return jsonify({
                "error": "Semester is required"
            }), 400

        user_id = get_current_user_id()

        student = Student.query.filter_by(
            user_id=user_id
        ).first()

        if not student:

            return jsonify({
                "error": "Student profile not found"
            }), 404

        financial_status = (
            PaymentService
            .get_student_financial_status(
                student.id,
                semester
            )
        )

        return jsonify({
            "financial_status": financial_status
        }), 200

    except ValueError as error:

        return jsonify({
            "error": str(error)
        }), 404

    except Exception as error:

        return jsonify({
            "error": str(error)
        }), 500


# =====================================================
# GET ANY STUDENT FINANCIAL STATUS
# Finance Officer / Admin
#
# Example:
# GET /api/payments/student/5/financial-status
#     ?semester=Semester%201%202026
# =====================================================

@role_required("finance", "admin")
def get_student_financial_status(student_id):

    try:

        semester = request.args.get(
            "semester"
        )

        if not semester:

            return jsonify({
                "error": "Semester is required"
            }), 400

        financial_status = (
            PaymentService
            .get_student_financial_status(
                student_id,
                semester
            )
        )

        return jsonify({
            "financial_status": financial_status
        }), 200

    except ValueError as error:

        return jsonify({
            "error": str(error)
        }), 404

    except Exception as error:

        return jsonify({
            "error": str(error)
        }), 500
