import os
import logging
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.client.default import DefaultBotProperties

API_URL = os.getenv("API_URL", "http://api:8000")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

def get_main_buttons() -> InlineKeyboardMarkup:
    """Создает инлайн кнопки для основного меню"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📝 Создать таблицу", callback_data="create_table")],
            [InlineKeyboardButton(text="❓ Помощь", callback_data="help")]
        ]
    )
    return keyboard

def get_help_buttons() -> InlineKeyboardMarkup:
    """Создает инлайн кнопки помощи"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="💬 Чат поддержки", url="https://t.me/rabbit_bot_chat")],
            [InlineKeyboardButton(text="👥 Группа обсуждений", url="https://t.me/rabbit_bot_group")],
            [InlineKeyboardButton(text="📖 Документация", url="https://t.me/rabbit_bot_docs")],
            [InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_main")]
        ]
    )
    return keyboard

def log_user_info(message: Message):
    """Логирование информации о пользователе"""
    user = message.from_user
    chat = message.chat
    logger.info(
        f"User Info:\n"
        f"User ID: {user.id}\n"
        f"Username: @{user.username}\n"
        f"First Name: {user.first_name}\n"
        f"Last Name: {user.last_name}\n"
        f"Language: {user.language_code}\n"
        f"Chat Type: {chat.type}\n"
        f"Chat ID: {chat.id}\n"
        f"Message Text: {message.text}"
    )

@dp.message(Command("start"))
async def start_cmd(message: Message):
    log_user_info(message)
    await message.answer(
        "👋 Привет! Я бот для создания таблиц.\n\n"
        "Выберите действие:",
        reply_markup=get_main_buttons()
    )

@dp.callback_query(lambda c: c.data == "create_table")
async def create_table_callback(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(
        "Введите название таблицы в формате:\n"
        "/create_table [название]"
    )
    await callback_query.answer()

@dp.callback_query(lambda c: c.data == "help")
async def help_callback(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(
        "📚 Справка по использованию бота:\n\n"
        "1. Нажмите '📝 Создать таблицу'\n"
        "2. Введите название таблицы\n"
        "3. Готово! Таблица создана\n\n"
        "Дополнительная информация:",
        reply_markup=get_help_buttons()
    )
    await callback_query.answer()

@dp.callback_query(lambda c: c.data == "back_to_main")
async def back_to_main_callback(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(
        "👋 Привет! Я бот для создания таблиц.\n\n"
        "Выберите действие:",
        reply_markup=get_main_buttons()
    )
    await callback_query.answer()

@dp.message(Command("create_table"))
async def create_table(message: Message):
    log_user_info(message)
    parts = message.text.split(maxsplit=1)
    if len(parts) != 2:
        await message.answer(
            "❗ Укажи название: /create_table BarName",
            reply_markup=get_main_buttons()
        )
        return
    bar_name = parts[1].strip()
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{API_URL}/create_table/{bar_name}") as resp:
            if resp.status == 200:
                await message.answer(
                    f"✅ Таблица '{bar_name}' создана.",
                    reply_markup=get_main_buttons()
                )
            else:
                await message.answer(
                    f"❌ Ошибка: {await resp.text()}",
                    reply_markup=get_main_buttons()
                )

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())