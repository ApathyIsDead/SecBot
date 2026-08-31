from aiogram import Router, types
from aiogram.filters import Command

router = Router()


@router.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "Привет! Я SecBot — твой помощник в мире кибербезопасности.\n\n"
        "Доступные команды:\n"
        "/password [длина] — сгенерировать пароль (4–128 символов)\n"
        "/hash [текст] — показать хеши (MD5, SHA‑1, SHA‑256)\n"
        "/check [пароль] — проверить пароль в утечках\n\n"
        "Сообщение с /check я удаляю сразу после проверки, "
        "чтобы пароль не оставался в истории чата.\n\n"
        "Примеры:\n"
        "/password 12\n"
        "/hash hello\n"
        "/check qwerty123"
    )
