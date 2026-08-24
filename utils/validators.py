MIN_PASSWORD_LENGTH = 4
MAX_PASSWORD_LENGTH = 128

def parse_command_arg(text: str | None) -> str | None:
    # Достаёт аргумент команды из текста сообщения (всё после первого слова).
    if text is None:
        return None
    parts = text.split(maxsplit=1)
    if len(parts) < 2:
        return None
    return parts[1]


def validate_password_length(raw_length: str) -> tuple[int | None, str | None]:
    # Проверяет длину пароля введённую пользователем
    try:
        length = int(raw_length)
    except ValueError:
        return None, "Длина должна быть числом. Пример: /password 12"

    if not(MIN_PASSWORD_LENGTH <= length <= MAX_PASSWORD_LENGTH):
        return None, f"Длина должна быть от {MIN_PASSWORD_LENGTH} до {MAX_PASSWORD_LENGTH} символов."

    return length, None

def validate_password(raw_password: str) -> tuple[bool, str | None]:
    if not raw_password:
        return False, "Пароль не может быть пустым"
    if any(ord(ch) < 32 for ch in raw_password):
        return False, "Пароль содержит недопустимые управляющие символы"
    return True, None

def validate_email(raw_email: str) -> tuple[bool, str | None]:
    if not raw_email:
        return False, "Почта не может быть пустой"
    if any(ord(ch) < 32 for ch in raw_email):
        return False, "Почта содержит недопустимые управляющие символы"

    parts = raw_email.split("@")
    if len(parts) != 2:
        return False, "Почта невалидна"
    if not parts[0] or not parts[1]:
        return False, "Почта невалидна"
    if any(ch.isspace() for ch in raw_email):
        return False, "Почта содержит пробелы"

    return True, None