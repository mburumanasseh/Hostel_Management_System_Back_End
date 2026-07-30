from datetime import datetime

from app.extensions import db
from app.models.allocation import Allocation
from app.models.student import Student
from app.models.room import Room


class AllocationService:

    @staticmethod
    def create_allocation(student_id, room_id):

        try:
            student = db.session.get(
                Student,
                student_id
            )

            if not student:
                raise ValueError("Student not found")

            room = db.session.get(
                Room,
                room_id
            )

            if not room:
                raise ValueError("Room not found")

            # Check if student already has an active allocation
            existing_allocation = Allocation.query.filter_by(
                student_id=student_id,
                status="Active"
            ).first()

            if existing_allocation:
                raise ValueError(
                    "Student already has an active room allocation"
                )

            # Room cannot accept students if under maintenance
            if room.status == "Maintenance":
                raise ValueError(
                    "Room is currently under maintenance"
                )

            # Make sure room has a valid capacity
            if not room.capacity or room.capacity < 1:
                raise ValueError(
                    "Room has an invalid capacity"
                )

            # Check room capacity
            if room.occupied >= room.capacity:
                raise ValueError(
                    "Room is already at full capacity"
                )

            allocation = Allocation(
                student_id=student_id,
                room_id=room_id,
                allocation_date=datetime.utcnow(),
                status="Active"
            )

            # Increase occupancy
            room.occupied += 1

            # Update room status
            if room.occupied >= room.capacity:
                room.status = "Occupied"
            else:
                room.status = "Available"

            db.session.add(allocation)
            db.session.commit()

            return allocation

        except ValueError:
            db.session.rollback()
            raise

        except Exception:
            db.session.rollback()
            raise

    @staticmethod
    def get_all_allocations():

        return Allocation.query.order_by(
            Allocation.id.asc()
        ).all()

    @staticmethod
    def get_allocation_by_id(allocation_id):

        return db.session.get(
            Allocation,
            allocation_id
        )

    @staticmethod
    def get_student_allocations(student_id):

        student = db.session.get(
            Student,
            student_id
        )

        if not student:
            raise ValueError("Student not found")

        return Allocation.query.filter_by(
            student_id=student_id
        ).order_by(
            Allocation.id.desc()
        ).all()

    @staticmethod
    def get_active_allocation(student_id):

        student = db.session.get(
            Student,
            student_id
        )

        if not student:
            raise ValueError("Student not found")

        return Allocation.query.filter_by(
            student_id=student_id,
            status="Active"
        ).first()

    @staticmethod
    def complete_allocation(allocation_id):

        try:
            allocation = db.session.get(
                Allocation,
                allocation_id
            )

            if not allocation:
                raise ValueError("Allocation not found")

            if allocation.status == "Completed":
                raise ValueError(
                    "Allocation is already completed"
                )

            room = allocation.room

            allocation.status = "Completed"
            allocation.checkout_date = datetime.utcnow()

            # Decrease occupancy
            if room.occupied > 0:
                room.occupied -= 1

            # Update room status
            if room.occupied == 0:
                room.status = "Available"

            elif room.occupied < room.capacity:
                room.status = "Available"

            else:
                room.status = "Occupied"

            db.session.commit()

            return allocation

        except ValueError:
            db.session.rollback()
            raise

        except Exception:
            db.session.rollback()
            raise

    @staticmethod
    def delete_allocation(allocation_id):

        try:
            allocation = db.session.get(
                Allocation,
                allocation_id
            )

            if not allocation:
                raise ValueError(
                    "Allocation not found"
                )

            # Restore room occupancy if
            # deleting an active allocation
            if allocation.status == "Active":

                room = allocation.room

                if room.occupied > 0:
                    room.occupied -= 1

                if room.occupied == 0:
                    room.status = "Available"

                elif room.occupied < room.capacity:
                    room.status = "Available"

                else:
                    room.status = "Occupied"

            db.session.delete(allocation)
            db.session.commit()

            return True

        except ValueError:
            db.session.rollback()
            raise

        except Exception:
            db.session.rollback()
            raise