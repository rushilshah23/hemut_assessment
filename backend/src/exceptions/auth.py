from src.exceptions.base import AppException


class InvalidCredentialsError(AppException):
    status = 401
    message = "Invalid email or password"



class InvalidTokenError(AppException):
    status_code = 401

    def __init__(self, message="Invalid or expired token"):
        super().__init__(message)
