from src.exceptions.base import AppException


class InvalidCredentialsError(AppException):
    status = 401
    message = "Invalid email or password"
