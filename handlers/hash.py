from html import escape

from aiogram import Router, types
from aiogram.filters import Command

from services.crypto import make_hashes
from utils.validators import parse_command_arg

router = Router()


@router.message(Command("hash"))
async def hash_command(message: types.Message):
    text = parse_command_arg(message.text)

    if text is None:
        await message.answer("Укажи текст для хеширования. Пример: /hash hello")
        return

    hashes = make_hashes(text)
    safe_text = escape(text)

    await message.answer(
        f"Хеши для строки <b>{safe_text}</b>:\n\n"
        f"🔹 MD5:\n<code>{hashes.get('MD5')}</code>\n\n"
        f"🔹 SHA-1:\n<code>{hashes.get('SHA-1')}</code>\n\n"
        f"🔹 SHA-256:\n<code>{hashes.get('SHA-256')}</code>",
        parse_mode="HTML",
    )
