from uuid6 import UUID

from src.core.exceptions.base import AppError, NotFoundError


class OrganizationError(AppError):
    """Базовое исключение для организаций"""

    def __init__(self, message: str = "Organization error occurred"):
        super().__init__(message)


class OrganizationNotFoundError(NotFoundError):
    """Организация не найдена"""

    def __init__(self, org_id: UUID):
        super().__init__(f"Organization with ID {org_id} not found")
