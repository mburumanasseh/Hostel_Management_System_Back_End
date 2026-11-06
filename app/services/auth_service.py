
from flask_jwt_extended import create_access_token

from app.extensions import db, bcrypt
from app.models.user import User
from app.models.student import Student


class AuthService:

    # ==========================================
    # STUDENT REGISTRATION
    # ==========================================

    @staticmethod
    def register_user(
        first_name,
        last_name,
        email,
        password,
        registration_number
    ):

        # ==========================================
        # CHECK EMAIL
        # ==========================================

        existing_user = User.query.filter_by(
            email=email
        ).first()

        if existing_user:
            raise ValueError(
                "Email already registered"
            )

        # ==========================================
        # CHECK REGISTRATION NUMBER
        # ==========================================

        existing_student = Student.query.filter_by(
            registration_number=registration_number
        ).first()

        if existing_student:
            raise ValueError(
                "Registration number already exists"
            )

        # ==========================================
        # HASH PASSWORD
        # ==========================================

        hashed_password = (
            bcrypt
            .generate_password_hash(password)
            .decode("utf-8")
        )

        # ==========================================
        # CREATE STUDENT USER
        # ==========================================

        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=hashed_password,
            role="student"
        )

        db.session.add(user)

        # Make user.id available
        db.session.flush()

        # ==========================================
        # CREATE STUDENT PROFILE
        # ==========================================

        student = Student(
            user_id=user.id,
            registration_number=registration_number
        )

        db.session.add(student)

        # ==========================================
        # SAVE BOTH
        # ==========================================

        db.session.commit()

        return user

    # ==========================================
    # STAFF REGISTRATION
    # ==========================================

    @staticmethod
    def register_staff(
        first_name,
        last_name,
        email,
        password,
        role
    ):

        # ==========================================
        # CHECK EMAIL
        # ==========================================

        existing_user = User.query.filter_by(
            email=email
        ).first()

        if existing_user:
            raise ValueError(
                "Email already registered"
            )

        # ==========================================
        # HASH PASSWORD
        # ==========================================

        hashed_password = (
            bcrypt
            .generate_password_hash(password)
            .decode("utf-8")
        )

        # ==========================================
        # CREATE STAFF USER
        # ==========================================

        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=hashed_password,
            role=role
        )

        db.session.add(user)
        db.session.commit()

        return user


    # ==========================================
    # BOOTSTRAP FIRST ADMIN (no admin exists yet)
    # ==========================================

    @staticmethod
    def bootstrap_admin(
        first_name,
        last_name,
        email,
        password
    ):
        existing_admin = User.query.filter_by(
            role="admin"
        ).first()

        if existing_admin:
            raise ValueError(
                "An admin account already exists"
            )

        existing_user = User.query.filter_by(
            email=email
        ).first()

        if existing_user:
            raise ValueError(
                "Email already registered"
            )

        hashed_password = (
            bcrypt
            .generate_password_hash(password)
            .decode("utf-8")
        )

        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=hashed_password,
            role="admin"
        )

        db.session.add(user)
        db.session.commit()

        return user

    # ==========================================
    # LOGIN
    # ==========================================

    @staticmethod
    def login_user(email, password):

        user = User.query.filter_by(
            email=email
        ).first()

        if (
            not user
            or not bcrypt.check_password_hash(
                user.password,
                password
            )
        ):
            raise ValueError(
                "Invalid email or password"
            )

        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={
                "role": user.role
            }
        )

        return user, access_token

    # ==========================================
    # GET USER BY ID
    # ==========================================


    @staticmethod
    def change_password(user_id, current_password, new_password, confirm_password):
        if new_password != confirm_password:
            raise ValueError("New password and confirmation do not match")

        if len(new_password) < 6:
            raise ValueError("New password must be at least 6 characters")

        if current_password == new_password:
            raise ValueError("New password must be different from current password")

        user = db.session.get(User, int(user_id))

        if not user:
            raise ValueError("User not found")

        if not bcrypt.check_password_hash(user.password, current_password):
            raise ValueError("Current password is incorrect")

        user.password = (
            bcrypt
            .generate_password_hash(new_password)
            .decode("utf-8")
        )

        db.session.commit()
        return user

    @staticmethod
    def get_user_by_id(user_id):

        return db.session.get(
            User,
            int(user_id)
        )