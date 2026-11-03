import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.client.default import DefaultBotProperties

from config import BOT_TOKEN

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=None))
dp = Dispatcher()

@dp.message(CommandStart())
async def cmd_start(message: Message):
    # Проверяем, находится ли сообщение в топике
    if message.message_thread_id:
        return # Если в топике, игнорируем /start, чтобы не засорять

    await message.answer(
        "📂 <b>Твоё структурированное Избранное</b>\n\n"
        "Чтобы создать папку:\n"
        "1. Нажми на кнопку «Все» внизу или на карточку «Новая тема».\n"
        "2. Напиши название папки (например, «Работа»).\n"
        "3. Кидай в неё файлы и текст.\n\n"
        "Всё.",
        parse_mode="HTML"
    )

@dp.message(F.forum_topic_created)
async def on_topic_created(message: Message):
    # Когда юзер создает новую тему, Telegram присылает сервисное сообщение.
    # Переименовываем тему в то название, которое ввел юзер.
    try:
        topic_name = message.forum_topic_created.name
        thread_id = message.message_thread_id
        
        # Вызываем API для изменения названия топика
        await message.bot.edit_forum_topic(
            chat_id=message.chat.id,
            message_thread_id=thread_id,
            name=topic_name
        )
    except Exception as e:
        logging.error(f"Ошибка при переименовании топика: {e}")

# Хендлер для любого текста/файла, чтобы бот не молчал в топиках (опционально)
@dp.message()
async def handle_all(message: Message):
    if message.message_thread_id:
        # Если это файл или текст в топике, можно просто поставить реакцию
        # или ничего не делать, так как Telegram сам сохраняет файлы в топике.
        pass

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())