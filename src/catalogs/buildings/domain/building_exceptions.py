from uuid6 import UUID

from src.core.exceptions.base import AppError, NotFoundError


class BuildingError(AppError):
    """Базовое исключение для зданий"""

    def __init__(self, message: str = "Building error occurred"):
        super().__init__(message)


class BuildingNotFoundError(NotFoundError):
    """Здание не найдено"""

    def __init__(self, building_id: UUID):
        super().__init__(f"Building with id {building_id} not found")
