import asyncio

from aiogram import Bot, Dispatcher

from config import BOT_TOKEN
from handlers import routers
from middlewares.throttling import ThrottlingMiddleware

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

throttling = ThrottlingMiddleware(rate_limit=1.0)

dp.message.middleware(throttling)
dp.callback_query.middleware(throttling)

for router in routers:
    dp.include_router(router)


async def main():
    print("🤖 SecBot запущен и готов к работе!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
