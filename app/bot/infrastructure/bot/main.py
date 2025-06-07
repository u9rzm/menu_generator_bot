"""
Основной файл бота, отвечающий за инициализацию и запуск всех компонентов.
Структура:
1. Импорты и настройки
2. Загрузка тематического маппинга
3. Инициализация бота и диспетчера
4. Инициализация обработчиков
5. Регистрация обработчиков
6. Запуск бота
"""

import os
import logging
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, ContentType
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Update
import traceback
from datetime import datetime
import json
import qrcode
from PIL import Image

# Импорты из нашей инфраструктуры
from app.bot.infrastructure.config.config import settings
from app.bot.infrastructure.logging.logger import logger
from app.bot.infrastructure.handlers.organization_handler import OrganizationHandler
from app.bot.infrastructure.handlers.menu_handler import MenuHandler
from app.bot.infrastructure.handlers.theme_handler import ThemeHandler
from app.bot.infrastructure.handlers.image_handler import ImageHandler
from app.bot.infrastructure.handlers.qr_code_handler import QRCodeHandler
from app.bot.infrastructure.handlers.help_handler import HelpHandler

# Определение состояний для FSM (Finite State Machine)
class OrganizationStates(StatesGroup):
    """Состояния для процесса создания организации"""
    waiting_for_name = State()  # Ожидание ввода названия
    waiting_for_description = State()  # Ожидание ввода описания
    waiting_for_type = State()  # Ожидание выбора типа меню
    waiting_for_menu = State()  # Ожидание загрузки меню
    waiting_for_description_images = State()  # Ожидание описания изображений
    waiting_for_images = State()  # Ожидание загрузки изображений
    waiting_for_background = State()  # Ожидание загрузки фона

# Глобальная переменная для хранения тематического маппинга
THEME_MAPPING = {}

async def load_theme_mapping():
    """
    Загружает маппинг тем при запуске бота.
    В случае ошибки устанавливает базовые темы.
    """
    global THEME_MAPPING
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{settings.NGINX_URL}/static/themes/theme_mapping.json") as resp:
                if resp.status == 200:
                    THEME_MAPPING = await resp.json()
                    logger.info(f"Successfully loaded theme mapping: {THEME_MAPPING}")
                else:
                    raise Exception(f"Failed to load themes: {await resp.text()}")
    except Exception as e:
        logger.error(f"Error loading theme mapping: {str(e)}")
        # Устанавливаем базовые темы в случае ошибки
        THEME_MAPPING = {
            'light': 'Светлая',
            'dark': 'Темная'
        }

# Инициализация бота с настройками из конфигурации
bot = Bot(
    token=settings.BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

# Инициализация диспетчера с хранилищем состояний в памяти
dp = Dispatcher(storage=MemoryStorage())

# Инициализация обработчиков с передачей экземпляра бота
organization_handler = OrganizationHandler(bot)
menu_handler = MenuHandler(bot)
theme_handler = ThemeHandler(bot)
image_handler = ImageHandler(bot)
qr_code_handler = QRCodeHandler(bot)
help_handler = HelpHandler(bot)

# Регистрация обработчиков команд
# Используем новый синтаксис register вместо декораторов
dp.message.register(organization_handler.handle_start, Command("start"))
dp.message.register(help_handler.handle_help, Command("help"))

# Регистрация обработчиков callback-запросов
# Организация
dp.callback_query.register(organization_handler.handle_create_org, lambda c: c.data == "create_org")
dp.callback_query.register(organization_handler.handle_my_organizations, lambda c: c.data == "my_organizations")
dp.callback_query.register(organization_handler.handle_back_to_main, lambda c: c.data == "back_to_main")
dp.callback_query.register(organization_handler.handle_org_actions, lambda c: c.data.startswith("org_actions_"))
dp.callback_query.register(organization_handler.handle_upload_images, lambda c: c.data.startswith("upload_images_"))
dp.callback_query.register(organization_handler.handle_upload_backgrounds, lambda c: c.data.startswith("upload_backgrounds_"))

# Меню
dp.callback_query.register(menu_handler.handle_show_menu, lambda c: c.data.startswith("show_menu_"))
dp.callback_query.register(menu_handler.handle_upload_menu_file, lambda c: c.data == "upload_menu_file")
dp.callback_query.register(menu_handler.handle_upload_menu_sheets, lambda c: c.data == "upload_menu_sheets")

# Темы
dp.callback_query.register(theme_handler.handle_theme_selection, lambda c: c.data.startswith("theme_"))
dp.callback_query.register(theme_handler.handle_ai_generate_theme, lambda c: c.data.startswith("ai_generate_theme_"))

# Изображения
dp.callback_query.register(image_handler.handle_image_upload, lambda c: c.data.startswith("upload_image_"))
dp.callback_query.register(image_handler.handle_background_upload, lambda c: c.data.startswith("upload_background_"))

# QR-коды
dp.callback_query.register(qr_code_handler.handle_qr_code_generation, lambda c: c.data.startswith("qrcode_"))

# Помощь
dp.callback_query.register(help_handler.handle_help_callback, lambda c: c.data == "help_")

# Регистрация обработчиков состояний
# Используем состояния из OrganizationStates
dp.message.register(organization_handler.handle_org_name, OrganizationStates.waiting_for_name)
dp.message.register(organization_handler.handle_org_description, OrganizationStates.waiting_for_description)
dp.message.register(organization_handler.handle_menu_upload, OrganizationStates.waiting_for_menu)
dp.message.register(organization_handler.handle_image_upload, OrganizationStates.waiting_for_images)
dp.message.register(organization_handler.handle_background_upload, OrganizationStates.waiting_for_background)

if __name__ == "__main__":
    import asyncio
    try:
        # Загружаем темы перед запуском бота
        asyncio.run(load_theme_mapping())
        # Запускаем бота
        asyncio.run(dp.start_polling(bot))
    except Exception as e:
        logger.error(f"Critical error in main: {str(e)}")
        logger.error(traceback.format_exc()) 