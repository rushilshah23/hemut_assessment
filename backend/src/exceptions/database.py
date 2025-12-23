from .base import AppException

class DuplicateResourceError(AppException):
    def __init__(self, field: str):
        self.field = field
        super().__init__(f"{field} already exists")



class NotFoundError(AppException):
    status_code = 404
    message = "Resource not found"