import requests

PWNED_API_URL = "https://api.pwnedpasswords.com/range/{prefix}"


class PwnedCheckError(Exception):
    """Не удалось выполнить запрос к API проверки утечек."""


def check_password_pwned(sha1_hash_upper: str) -> int:
    prefix, suffix = sha1_hash_upper[:5], sha1_hash_upper[5:]
    url = PWNED_API_URL.format(prefix=prefix)

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except requests.exceptions.RequestException as exc:
        raise PwnedCheckError(
            "Не удалось подключиться к серверу проверки паролей."
        ) from exc

    for line in response.text.splitlines():
        line_suffix, _, count = line.partition(":")
        if line_suffix == suffix:
            return int(count)

    return 0
