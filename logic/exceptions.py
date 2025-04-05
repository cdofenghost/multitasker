class AppError(Exception):
    code: int = 500
    message: str = "Internal Server Error"

class UserNotFoundError(AppError):
    code = 404
    message = "Пользователь не найден"

class PermissionDeniedError(AppError):
    code = 403
    message = "Недостаточно прав"


class IncorrectPasswordError(AppError):
    code = 403
    message = "Вы ввели неверный пароль. Попробуйте снова."
    
