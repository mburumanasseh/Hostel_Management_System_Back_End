from flask_jwt_extended import create_access_token

from app.extensions import db, bcrypt
from app.models.user import User


class AuthService:

    @staticmethod
    def register_user(
        first_name,
        last_name,
        email,
        password,
        role="student"
    ):
        existing_user = User.query.filter_by(
            email=email
        ).first()

        if existing_user:
            raise ValueError("Email already registered")

        hashed_password = bcrypt.generate_password_hash(
            password
        ).decode("utf-8")

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

    @staticmethod
    def login_user(email, password):

        user = User.query.filter_by(
            email=email
        ).first()

        if not user or not bcrypt.check_password_hash(user.password, password):
            raise ValueError("Invalid email or password")

        access_token = create_access_token(
            identity=str(user.id),
            additional_claims={
                "role": user.role
            }
        )

        return user, access_token

    @staticmethod
    def get_user_by_id(user_id):

        # Using db.session.get is preferred in modern Flask-SQLAlchemy / SQLAlchemy 2.0+
        return db.session.get(User, int(user_id))