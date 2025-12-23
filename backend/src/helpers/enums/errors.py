from enum import Enum


class DatabaseErrorCodes(Enum):
    UNIQUE_VIOLATION = "23505"