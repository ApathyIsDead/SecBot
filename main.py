import asyncio
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers import routers

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

for router in routers:
    dp.include_router(router)

async def main():
    print("🤖 SecBot запущен и готов к работе!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())