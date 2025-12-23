import re
from .base import Validator


class UserValidators:

    class Email(Validator):
        message = "Invalid email address"

        @classmethod
        def validate(cls, email: str):
            if not email or not isinstance(email, str):
                cls.raise_error("Email is required")

            email = email.strip().lower()

            email_regex = r"^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$"

            if not re.match(email_regex, email):
                cls.raise_error()

            return email

    class Password(Validator):
        message = "Password does not meet security requirements"

        @classmethod
        def validate(cls, password: str):
            if not password or not isinstance(password, str):
                cls.raise_error("Password is required")

            if len(password) < 6:
                cls.raise_error("Password must be at least 6 characters long")

            # if not any(c.isupper() for c in password):
            #     cls.raise_error("Password must contain at least one uppercase letter")

            # if not any(c.islower() for c in password):
            #     cls.raise_error("Password must contain at least one lowercase letter")

            # if not any(c.isdigit() for c in password):
            #     cls.raise_error("Password must contain at least one digit")

            # if not any(c in "!@#$%^&*()_+-=[]{}|;':\",./<>?" for c in password):
            #     cls.raise_error("Password must contain at least one special character")

            return password

    class PasswordEqualsConfirmPassword(Validator):
        message = "Passwords do not match"

        @classmethod
        def validate(cls, password: str, confirm_password: str):
            if password != confirm_password:
                cls.raise_error()

            return True
