import hashlib
import secrets
import math

LOWER = 'qwertyuiopasdfghjklzxcvbnm'
UPPER = LOWER.upper()
DIGITS = '1234567890'
SYMBOLS = '!@#$%^&*()+_-='
SIMILAR = set('Il1O0')

def build_alphabet(use_letters, use_digits, use_symbols, exclude_similar) -> str:
    alphabet = ""
    if use_letters:
        alphabet += LOWER + UPPER
    if use_digits:
        alphabet += DIGITS
    if use_symbols:
        alphabet += SYMBOLS
    if exclude_similar:
        alphabet = "".join(c for c in alphabet if c not in SIMILAR)
    return alphabet

def generate_password(length: int, alphabet: str) -> str:
    # Генирирует пароль из заданного количества символов
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def make_hashes(text: str) -> dict[str, str]:
    # Возвращает список с 3-мя хэшами текста
    text_bytes = text.encode('UTF-8')
    return {
        "MD5": hashlib.md5(text_bytes, usedforsecurity=False).hexdigest(),
        "SHA-1": hashlib.sha1(text_bytes, usedforsecurity=False).hexdigest(),
        "SHA-256": hashlib.sha256(text_bytes, usedforsecurity=False).hexdigest()
    }

def sha1_upper(text: str) -> str:
    # Возвращает SHA-1 хэш в верхнем регистре
    return hashlib.sha1(text.encode('UTF-8'), usedforsecurity=False).hexdigest().upper()

def get_alphabet_size(password: str) -> int:
    # Определяет количество различных символов в пароле
    size = 0
    if any(c.islower() for c in password):
        size += 26
    if any(c.isupper() for c in password):
        size += 26
    if any(c.isdigit() for c in password):
        size += 10
    if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?/~" for c in password):
        size += 32
    return max(size, 1)

def entropy(password: str) -> float | int:
    # Энтропия пароля в битах
    return len(password) * math.log2(get_alphabet_size(password))

def analyze_password(password: str) -> dict:
    # Полный анализ пароля
    length = len(password)
    alphabet_size = get_alphabet_size(password)
    ent = entropy(password)

    if ent < 28:
        level = 'Слабый'
    elif ent < 60:
        level = 'Средний'
    else:
        level = 'Сильный'

    return {
        "password": password,
        "length": length,
        "alphabet_size": alphabet_size,
        "entropy": round(ent, 2),
        "level": level
    }