import asyncio
import os
from dotenv import load_dotenv
from pathlib import Path

from aiogram import Bot, Dispatcher
from app.bot.handlers import router


BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")


async def main():
    token = os.getenv("TELEGRAM_BOT_TOKEN")

    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN is missing")

    bot = Bot(token=token)
    dp = Dispatcher()

    dp.include_router(router)

    print("Bot started...")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())