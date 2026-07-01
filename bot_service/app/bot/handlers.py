from aiogram import Router
from aiogram.types import Message

router = Router()

# временное хранилище токенов (потом заменим на Redis)
user_tokens = {}


@router.message()
async def handle_message(message: Message):
    text = message.text

    # команда /start
    if text == "/start":
        await message.answer(
            "Привет! Отправь /token <JWT>, чтобы авторизоваться"
        )
        return

    # команда /token
    if text.startswith("/token"):
        parts = text.split()

        if len(parts) < 2:
            await message.answer("Нужен токен: /token <JWT>")
            return

        token = parts[1]
        user_tokens[message.from_user.id] = token

        await message.answer("Токен сохранён")
        return

    # обычные сообщения
    if message.from_user.id not in user_tokens:
        await message.answer("Сначала отправь /token <JWT>")
        return

    await message.answer(f"Принято: {text}")