from flask import request, jsonify
from marshmallow import ValidationError

from app.schemas.hostel_fee_schema import (
    HostelFeeSchema
)

from app.services.hostel_fee_service import (
    HostelFeeService
)


hostel_fee_schema = HostelFeeSchema()


# =====================================================
# CREATE HOSTEL FEE
# =====================================================

def create_hostel_fee():

    try:

        data = hostel_fee_schema.load(
            request.get_json()
        )

        fee = HostelFeeService.create_fee(
            semester=data["semester"],
            amount=data["amount"]
        )

        return jsonify({
            "message": "Hostel fee created successfully",
            "hostel_fee": fee.to_dict()
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
# GET ALL HOSTEL FEES
# =====================================================

def get_all_hostel_fees():

    try:

        fees = HostelFeeService.get_all_fees()

        return jsonify({
            "hostel_fees": [
                fee.to_dict()
                for fee in fees
            ]
        }), 200

    except Exception as error:

        return jsonify({
            "error": str(error)
        }), 500


# =====================================================
# GET ONE HOSTEL FEE
# =====================================================

def get_hostel_fee(fee_id):

    try:

        fee = HostelFeeService.get_fee_by_id(
            fee_id
        )

        if not fee:

            return jsonify({
                "error": "Hostel fee not found"
            }), 404

        return jsonify({
            "hostel_fee": fee.to_dict()
        }), 200

    except Exception as error:

        return jsonify({
            "error": str(error)
        }), 500


# =====================================================
# UPDATE HOSTEL FEE
# =====================================================

def update_hostel_fee(fee_id):

    try:

        data = hostel_fee_schema.load(
            request.get_json(),
            partial=True
        )

        fee = HostelFeeService.update_fee(
            fee_id=fee_id,
            semester=data.get("semester"),
            amount=data.get("amount")
        )

        return jsonify({
            "message": "Hostel fee updated successfully",
            "hostel_fee": fee.to_dict()
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
# DELETE HOSTEL FEE
# =====================================================

def delete_hostel_fee(fee_id):

    try:

        HostelFeeService.delete_fee(
            fee_id
        )

        return jsonify({
            "message": "Hostel fee deleted successfully"
        }), 200

    except ValueError as error:

        return jsonify({
            "error": str(error)
        }), 404

    except Exception as error:

        return jsonify({
            "error": str(error)
        }), 500