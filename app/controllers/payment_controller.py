from flask import request, jsonify
from marshmallow import ValidationError
from flask_jwt_extended import get_jwt_identity
from app.models.student import Student

from app.schemas.payment_schema import (
    PaymentSchema,
    PaymentStatusSchema
)

from app.services.payment_service import PaymentService


payment_schema = PaymentSchema()
payment_status_schema = PaymentStatusSchema()


# =====================================================
# CREATE PAYMENT
# =====================================================

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
# =====================================================

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
# =====================================================

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
# =====================================================

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
# =====================================================

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
            "message": "Payment status updated successfully",
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
# =====================================================

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
        

def get_my_payments():

    try:

        user_id = int(get_jwt_identity())

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