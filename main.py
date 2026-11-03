import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from config import BOT_TOKEN

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=None))
dp = Dispatcher()

# Состояния для создания папки
class FolderStates(StatesGroup):
    waiting_for_name = State()

# Клавиатура с кнопками
def get_main_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📁 Создать папку")],
        ],
        resize_keyboard=True
    )

@dp.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "📂 <b>Твоё структурированное Избранное</b>\n\n"
        "Нажми «📁 Создать папку», чтобы завести новую тему.\n"
        "Кидай в неё файлы, ссылки и текст — они останутся там навсегда.",
        parse_mode="HTML",
        reply_markup=get_main_kb()
    )

@dp.message(F.text == "📁 Создать папку")
async def ask_folder_name(message: Message, state: FSMContext):
    await message.answer("Напиши название для новой папки:")
    await state.set_state(FolderStates.waiting_for_name)

@dp.message(FolderStates.waiting_for_name)
async def create_folder(message: Message, state: FSMContext):
    folder_name = message.text
    
    # Убираем клавиатуру, чтобы не мешала в топике (опционально)
    await message.answer(f"Создаю папку «{folder_name}»...", reply_markup=get_main_kb())
    
    try:
        # Бот сам создает тему с нужным именем
        topic = await message.bot.create_forum_topic(
            chat_id=message.chat.id,
            name=folder_name
        )
        
        # Отправляем приветствие прямо в созданную тему
        await message.bot.send_message(
            chat_id=message.chat.id,
            message_thread_id=topic.message_thread_id,
            text=f"📁 <b>Папка «{folder_name}» создана!</b>\n\nКидай сюда всё, что хочешь сохранить.",
            parse_mode="HTML"
        )
    except Exception as e:
        await message.answer(f"❌ Ошибка при создании: {e}")
    
    await state.clear()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())