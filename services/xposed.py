import requests

XPOSED_API_URL = "https://api.xposedornot.com/v1/check-email/{email}"


class XposedCheckError(Exception):
    """Не удалось выполнить запрос к API проверки утечек"""


def check_email_xposed(email: str) -> list[str]:
    url = XPOSED_API_URL.format(email=email)

    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as exc:
        raise XposedCheckError(
            "Не удалось подключиться к сервису проверки почт."
        ) from exc

    data = response.json()

    if "Error" in data:
        return []

    return data["breaches"][0]
