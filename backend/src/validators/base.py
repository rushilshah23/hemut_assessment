class Validator:
    message: str = "Validation failed"

    @classmethod
    def raise_error(cls, message: str | None = None):
        raise ValueError(message or cls.message)
