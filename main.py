import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties

from config import BOT_TOKEN

logging.basicConfig(level=logging.INFO)

# Отключаем глобальный parse_mode
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=None))
dp = Dispatcher()

@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        "📂 <b>Добро пожаловать в твое структурированное Избранное!</b>\n\n"
        "Здесь больше не будет хаоса. Ты сам создаешь папки (ветки) под свои нужды: "
        "«Работа», «Учеба», «Мемы» или что угодно еще.\n\n"
        "👉 <b>Как начать:</b> Нажми на иконку меню чата (вверху экрана) и выбери «Создать топик». "
        "Дай ему название и кидай туда всё, что хочешь сохранить. Всё, как в обычном Telegram, только с порядком!",
        parse_mode="HTML"
    )

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())