from app.extensions import db
from app.models.student import Student
from app.models.user import User


class StudentService:

    @staticmethod
    def create_student(
        user_id,
        registration_number,
        gender=None,
        phone=None,
        course=None,
        year_of_study=None,
        guardian_name=None,
        guardian_phone=None
    ):
        # Check that the user exists
        user = db.session.get(User, user_id)

        if not user:
            raise ValueError("User not found")

        # Only student users can have student profiles
        if user.role != "student":
            raise ValueError(
                "Student profile can only be created for a student user"
            )

        # Check if user already has a student profile
        existing_student = Student.query.filter_by(
            user_id=user_id
        ).first()

        if existing_student:
            raise ValueError(
                "This user already has a student profile"
            )

        # Check registration number
        existing_registration = Student.query.filter_by(
            registration_number=registration_number
        ).first()

        if existing_registration:
            raise ValueError(
                "Registration number already exists"
            )

        student = Student(
            user_id=user_id,
            registration_number=registration_number,
            gender=gender,
            phone=phone,
            course=course,
            year_of_study=year_of_study,
            guardian_name=guardian_name,
            guardian_phone=guardian_phone
        )

        db.session.add(student)
        db.session.commit()

        return student

    @staticmethod
    def get_all_students():
        return Student.query.all()

    @staticmethod
    def get_student_by_id(student_id):
        return db.session.get(Student, student_id)

    @staticmethod
    def update_student(student_id, data):

        student = db.session.get(Student, student_id)

        if not student:
            raise ValueError("Student not found")

        # Don't allow changing the user relationship
        # through the update endpoint.
        allowed_fields = [
            "registration_number",
            "gender",
            "phone",
            "course",
            "year_of_study",
            "guardian_name",
            "guardian_phone"
        ]

        if "registration_number" in data:
            existing = Student.query.filter(
                Student.registration_number == data["registration_number"],
                Student.id != student_id
            ).first()

            if existing:
                raise ValueError(
                    "Registration number already exists"
                )

        for field in allowed_fields:

            if field in data:
                setattr(
                    student,
                    field,
                    data[field]
                )

        db.session.commit()

        return student

    @staticmethod
    def delete_student(student_id):

        student = db.session.get(Student, student_id)

        if not student:
            raise ValueError("Student not found")

        db.session.delete(student)
        db.session.commit()

        return True