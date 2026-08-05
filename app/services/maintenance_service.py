from app.extensions import db
from app.models.maintenance import MaintenanceRequest
from app.models.student import Student
from app.models.room import Room


class MaintenanceService:

    @staticmethod
    def create_request(
        student_id,
        room_id,
        title,
        description,
        priority="Medium"
    ):

        student = db.session.get(
            Student,
            student_id
        )

        if not student:
            raise ValueError(
                "Student not found"
            )

        room = db.session.get(
            Room,
            room_id
        )

        if not room:
            raise ValueError(
                "Room not found"
            )

        active_allocation = None

        for allocation in student.allocations:

            if (
                allocation.room_id == room_id
                and allocation.status == "Active"
            ):
                active_allocation = allocation
                break

        if not active_allocation:
            raise ValueError(
                "Student is not currently allocated to this room"
            )

        maintenance_request = MaintenanceRequest(
            student_id=student_id,
            room_id=room_id,
            title=title,
            description=description,
            priority=priority,
            status="Pending"
        )

        try:

            db.session.add(
                maintenance_request
            )

            db.session.commit()

            return maintenance_request

        except Exception:

            db.session.rollback()

            raise


    # ==========================================================
    # CREATE REQUEST FOR CURRENTLY LOGGED-IN STUDENT
    # ==========================================================

    @staticmethod
    def create_request_for_student(
        user_id,
        title,
        description,
        priority="Medium"
    ):

        # Find the student profile belonging
        # to the logged-in user.
        student = Student.query.filter_by(
            user_id=user_id
        ).first()

        if not student:
            raise ValueError(
                "Student profile not found"
            )

        # Find the student's active allocation.
        active_allocation = None

        for allocation in student.allocations:

            if allocation.status == "Active":
                active_allocation = allocation
                break

        if not active_allocation:
            raise ValueError(
                "You are not currently allocated to a room"
            )

        maintenance_request = MaintenanceRequest(
            student_id=student.id,
            room_id=active_allocation.room_id,
            title=title,
            description=description,
            priority=priority,
            status="Pending"
        )

        try:

            db.session.add(
                maintenance_request
            )

            db.session.commit()

            return maintenance_request

        except Exception:

            db.session.rollback()

            raise


    @staticmethod
    def get_all_requests():

        return MaintenanceRequest.query.order_by(
            MaintenanceRequest.id.desc()
        ).all()


    @staticmethod
    def get_request_by_id(request_id):

        return db.session.get(
            MaintenanceRequest,
            request_id
        )


    @staticmethod
    def get_student_requests(student_id):

        student = db.session.get(
            Student,
            student_id
        )

        if not student:
            raise ValueError(
                "Student not found"
            )

        return MaintenanceRequest.query.filter_by(
            student_id=student_id
        ).order_by(
            MaintenanceRequest.id.desc()
        ).all()


    @staticmethod
    def update_status(
        request_id,
        status
    ):

        maintenance_request = db.session.get(
            MaintenanceRequest,
            request_id
        )

        if not maintenance_request:
            raise ValueError(
                "Maintenance request not found"
            )

        maintenance_request.status = status

        try:

            db.session.commit()

            return maintenance_request

        except Exception:

            db.session.rollback()

            raise


    @staticmethod
    def delete_request(request_id):

        maintenance_request = db.session.get(
            MaintenanceRequest,
            request_id
        )

        if not maintenance_request:
            raise ValueError(
                "Maintenance request not found"
            )

        try:

            db.session.delete(
                maintenance_request
            )

            db.session.commit()

            return True

        except Exception:

            db.session.rollback()

            raise