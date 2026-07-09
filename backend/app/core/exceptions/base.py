from typing import Any


class AppException(Exception):
    def __init__(
        self,
        message: str,
        status_code: int = 400,
        details: dict[str, Any] | None = None,
    ) -> None:
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(message)


class NotFoundError(AppException):
    def __init__(self, resource: str, identifier: str | int) -> None:
        super().__init__(
            message=f"{resource} with id '{identifier}' not found",
            status_code=404,
        )


class ConflictError(AppException):
    def __init__(self, message: str) -> None:
        super().__init__(message=message, status_code=409)


class UnauthorizedError(AppException):
    def __init__(self, message: str = "Unauthorized") -> None:
        super().__init__(message=message, status_code=401)


class ForbiddenError(AppException):
    def __init__(self, message: str = "Forbidden") -> None:
        super().__init__(message=message, status_code=403)


class ValidationError(AppException):
    def __init__(self, message: str, details: dict[str, Any] | None = None) -> None:
        super().__init__(message=message, status_code=422, details=details)
