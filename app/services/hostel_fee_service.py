from app.extensions import db
from app.models.hostel_fee import HostelFee


class HostelFeeService:

    # =====================================================
    # CREATE HOSTEL FEE
    # =====================================================

    @staticmethod
    def create_fee(
        semester,
        amount
    ):

        existing_fee = HostelFee.query.filter_by(
            semester=semester
        ).first()

        if existing_fee:
            raise ValueError(
                "A hostel fee already exists for this semester"
            )

        fee = HostelFee(
            semester=semester,
            amount=amount
        )

        db.session.add(fee)
        db.session.commit()

        return fee

    # =====================================================
    # GET ALL HOSTEL FEES
    # =====================================================

    @staticmethod
    def get_all_fees():

        return HostelFee.query.order_by(
            HostelFee.created_at.desc()
        ).all()

    # =====================================================
    # GET ONE HOSTEL FEE
    # =====================================================

    @staticmethod
    def get_fee_by_id(fee_id):

        return db.session.get(
            HostelFee,
            fee_id
        )

    # =====================================================
    # UPDATE HOSTEL FEE
    # =====================================================

    @staticmethod
    def update_fee(
        fee_id,
        semester=None,
        amount=None
    ):

        fee = db.session.get(
            HostelFee,
            fee_id
        )

        if not fee:
            raise ValueError(
                "Hostel fee not found"
            )

        # ---------------------------------------------
        # Update semester
        # ---------------------------------------------

        if semester is not None:

            existing_fee = HostelFee.query.filter(
                HostelFee.semester == semester,
                HostelFee.id != fee_id
            ).first()

            if existing_fee:
                raise ValueError(
                    "A hostel fee already exists for this semester"
                )

            fee.semester = semester

        # ---------------------------------------------
        # Update amount
        # ---------------------------------------------

        if amount is not None:
            fee.amount = amount

        db.session.commit()

        return fee

    # =====================================================
    # DELETE HOSTEL FEE
    # =====================================================

    @staticmethod
    def delete_fee(fee_id):

        fee = db.session.get(
            HostelFee,
            fee_id
        )

        if not fee:
            raise ValueError(
                "Hostel fee not found"
            )

        db.session.delete(fee)

        db.session.commit()

        return True