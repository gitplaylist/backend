"""Define exceptions."""

class ValidationError(ValueError):
    """Define a validation error."""

    def __init__(self, message):
        super(ValidationError, self).__init__(message)
