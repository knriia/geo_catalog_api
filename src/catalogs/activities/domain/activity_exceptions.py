from uuid6 import UUID

from src.core.exceptions.base import AppError, NotFoundError, ValidationError


class ActivityError(AppError):
    """Базовое исключение для деятельностей"""

    def __init__(self, message: str = "Activity directory error"):
        super().__init__(message)


class ActivityLimitError(ValidationError):
    """Превышение лимита вложенности"""

    def __init__(self, message: str = "Maximum nesting level exceeded (max 3 levels)"):
        super().__init__(message)


class ActivityNotFoundError(NotFoundError):
    """Деятельность не найдена"""

    def __init__(self, activity_id: UUID):
        super().__init__(f"Activity with ID {activity_id} not found")
