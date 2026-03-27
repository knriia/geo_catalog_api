from fastapi import status


class AppError(Exception):
    """Базовый класс для всех ошибок приложения"""

    status_code: int = status.HTTP_400_BAD_REQUEST

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class NotFoundError(AppError):
    """Ошибка: ресурс не найден"""

    status_code = status.HTTP_404_NOT_FOUND


class ValidationError(AppError):
    """Ошибка валидации"""

    status_code = status.HTTP_422_UNPROCESSABLE_CONTENT
