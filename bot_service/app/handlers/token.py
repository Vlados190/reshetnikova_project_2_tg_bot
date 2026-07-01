from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

TOKENS = {}


@router.message(Command("token"))
async def token_handler(message: Message):
    parts = message.text.split()

    if len(parts) != 2:
        await message.answer("Используй: /token <jwt>")
        return

    TOKENS[message.from_user.id] = parts[1]

    await message.answer("Токен сохранён!")