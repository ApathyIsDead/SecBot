import time
from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message, TelegramObject, User


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, rate_limit=1.0):
        self.rate_limit = rate_limit
        self.last_time: dict[int, float] = {}

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        user: User | None = data.get("event_from_user")
        if user is None:
            return await handler(event, data)

        user_id = user.id
        now = time.monotonic()
        last = self.last_time.get(user_id)

        if last is not None and (now - last) < self.rate_limit:
            if isinstance(event, (Message, CallbackQuery)):
                await event.answer("Слишком часто, подожди немного")
            return None

        self.last_time[user_id] = now
        return await handler(event, data)
