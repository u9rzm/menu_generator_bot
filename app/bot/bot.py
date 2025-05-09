import os
import logging
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Update
from aiogram.ext.contexts import ContextTypes

API_URL = os.getenv("API_URL")
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
dp = Dispatcher(storage=MemoryStorage())

# Состояния для создания организации
class OrganizationStates(StatesGroup):
    waiting_for_name = State()
    waiting_for_description = State()
    waiting_for_menu = State()

async def register_user(user_id: int) -> bool:
    """Регистрирует пользователя в базе данных"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{API_URL}/register_user?tid={user_id}") as resp:
                if resp.status == 200:
                    user_data = await resp.json()
                    logger.info(f"User {user_id} registered successfully: {user_data}")
                    return True
                else:
                    error_text = await resp.text()
                    logger.error(f"Failed to register user {user_id}: {error_text}")
                    return False
    except Exception as e:
        logger.error(f"Error registering user {user_id}: {str(e)}")
        return False

def get_main_buttons() -> InlineKeyboardMarkup:
    """Создает инлайн кнопки для основного меню"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📝 Создать таблицу", callback_data="create_table")],
            [InlineKeyboardButton(text="🏢 Мои организации", callback_data="my_organizations")],
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

def get_organization_buttons() -> InlineKeyboardMarkup:
    """Создает инлайн кнопки для создания организации"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📝 Создать организацию", callback_data="create_org")],
            [InlineKeyboardButton(text="❓ Помощь", callback_data="help")]
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
async def cmd_start(message: Message):
    """Обработчик команды /start"""
    log_user_info(message)
    
    # Регистрируем пользователя только если это первое сообщение
    if message.message_id == 1:
        success = await register_user(message.from_user.id)
        if success:
            await message.answer(
                "👋 Добро пожаловать!\n\n"
                "Я бот для управления меню. Используйте следующие команды:\n"
                "/menu - Просмотр меню\n"
                "/create_org - Создать организацию\n"
                "/help - Получить помощь",
                reply_markup=get_main_buttons()
            )
        else:
            await message.answer(
                "❌ Произошла ошибка при регистрации. Пожалуйста, попробуйте позже."
            )
    else:
        await message.answer(
            "👋 С возвращением!\n\n"
            "Я бот для управления меню. Используйте следующие команды:\n"
            "/menu - Просмотр меню\n"
            "/create_org - Создать организацию\n"
            "/help - Получить помощь",
            reply_markup=get_main_buttons()
        )

@dp.callback_query(lambda c: c.data == "create_org")
async def create_org_callback(callback_query: types.CallbackQuery, state: FSMContext):
    """Начало процесса создания организации"""
    await callback_query.message.edit_text(
        "Введите название вашей организации:"
    )
    await state.set_state(OrganizationStates.waiting_for_name)
    await callback_query.answer()

@dp.message(OrganizationStates.waiting_for_name)
async def process_org_name(message: Message, state: FSMContext):
    """Обработка названия организации"""
    await state.update_data(org_name=message.text)
    await message.answer(
        "Отлично! Теперь введите описание вашей организации:"
    )
    await state.set_state(OrganizationStates.waiting_for_description)

@dp.message(OrganizationStates.waiting_for_description)
async def process_org_description(message: Message, state: FSMContext):
    """Обработка описания организации"""
    await state.update_data(org_description=message.text)
    await message.answer(
        "Теперь отправьте файл с меню в формате CSV или Excel.\n"
        "Формат файла должен быть следующим:\n"
        "name,price,category,description,subcategory\n"
        "Например:\n"
        "Пицца Маргарита,450,Пицца,Классическая пицца с томатами и моцареллой,Итальянская"
    )
    await state.set_state(OrganizationStates.waiting_for_menu)

@dp.message(OrganizationStates.waiting_for_menu)
async def process_org_menu(message: Message, state: FSMContext):
    """Обработка файла меню"""
    if not message.document:
        await message.answer(
            "Пожалуйста, отправьте файл с меню в формате CSV или Excel."
        )
        return

    # Получаем сохраненные данные
    data = await state.get_data()
    org_name = data.get('org_name')
    org_description = data.get('org_description')

    try:
        # Скачиваем файл
        file_path = f"temp_{message.document.file_id}.{message.document.file_name.split('.')[-1]}"
        await bot.download(message.document, destination=file_path)

        # Отправляем данные на API
        async with aiohttp.ClientSession() as session:
            # Сначала регистрируем пользователя
            async with session.post(f"{API_URL}/register_user?tid={message.from_user.id}") as resp:
                if resp.status != 200:
                    raise Exception(f"Failed to register user: {await resp.text()}")
                user = await resp.json()

            # Создаем организацию
            form_data = aiohttp.FormData()
            form_data.add_field('name', org_name)
            form_data.add_field('description', org_description)
            form_data.add_field('owner_id', str(user['id']))  # Используем ID из таблицы users

            async with session.post(f"{API_URL}/organizations", data=form_data) as resp:
                if resp.status != 200:
                    raise Exception(f"Failed to create organization: {await resp.text()}")
                org = await resp.json()

            # Загружаем меню
            with open(file_path, 'rb') as f:
                files = {'file': f}
                async with session.post(f"{API_URL}/organizations/{org['id']}/menu", data=files) as resp:
                    if resp.status != 200:
                        raise Exception(f"Failed to upload menu: {await resp.text()}")

        # Удаляем временный файл
        os.remove(file_path)

        await message.answer(
            f"✅ Организация '{org_name}' успешно создана!\n\n"
            "Теперь вы можете:\n"
            "/menu - Просмотреть меню\n"
            "/help - Получить помощь"
        )
    except Exception as e:
        logger.error(f"Error creating organization: {str(e)}")
        await message.answer(
            "❌ Произошла ошибка при создании организации. Пожалуйста, попробуйте позже."
        )
    finally:
        await state.clear()

@dp.callback_query(lambda c: c.data == "create_menu")
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
        "1. Нажмите '📝 Создать Меню Органицации'\n"
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

@dp.message(Command("create_org"))
async def cmd_create_org(message: Message, state: FSMContext):
    """Обработчик команды /create_org"""
    log_user_info(message)
    
    await message.answer(
        "Введите название вашей организации:"
    )
    await state.set_state(OrganizationStates.waiting_for_name)

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

@dp.message(Command("help"))
async def cmd_help(message: Message):
    """Обработчик команды /help"""
    log_user_info(message)
    
    help_text = (
        "📋 Доступные команды:\n\n"
        "/start - Начать работу с ботом\n"
        "/menu - Просмотр меню\n"
        "/help - Показать это сообщение\n\n"
        "Если у вас возникли вопросы, обратитесь к администратору."
    )
    
    await message.answer(help_text)

@dp.message(Command("menu"))
async def cmd_menu(message: Message):
    """Обработчик команды /menu"""
    log_user_info(message)
    
    try:
        async with aiohttp.ClientSession() as session:
            # Получаем список организаций пользователя
            async with session.get(f"{API_URL}/organizations?owner_id={message.from_user.id}") as resp:
                if resp.status != 200:
                    raise Exception(f"Failed to get organizations: {await resp.text()}")
                organizations = await resp.json()

            if not organizations:
                await message.answer(
                    "У вас пока нет организаций. Создайте организацию командой /create_org"
                )
                return

            # Если у пользователя только одна организация, показываем её меню
            if len(organizations) == 1:
                org = organizations[0]
                await show_organization_menu(message, org['id'])
                return

            # Если несколько организаций, предлагаем выбрать
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text=org['name'], callback_data=f"show_menu_{org['id']}")]
                    for org in organizations
                ]
            )
            await message.answer(
                "Выберите организацию, меню которой хотите посмотреть:",
                reply_markup=keyboard
            )
    except Exception as e:
        logger.error(f"Error fetching menu: {str(e)}")
        await message.answer("❌ Произошла ошибка при загрузке меню. Пожалуйста, попробуйте позже.")

async def show_organization_menu(message: Message, org_id: int):
    """Показывает меню организации"""
    try:
        async with aiohttp.ClientSession() as session:
            # Получаем меню организации
            async with session.get(f"{API_URL}/organizations/{org_id}/menu") as resp:
                if resp.status != 200:
                    raise Exception(f"Failed to get menu: {await resp.text()}")
                menu_items = await resp.json()
                
                if not menu_items:
                    await message.answer("📋 Меню пусто")
                    return
                
                # Группируем блюда по категориям
                categories = {}
                for item in menu_items:
                    if item['is_available']:
                        category = item['category']
                        if category not in categories:
                            categories[category] = []
                        categories[category].append(item)
                
                # Формируем сообщение
                menu_text = "📋 Наше меню:\n\n"
                
                for category, items in categories.items():
                    menu_text += f"🍽 {category}:\n"
                    for item in items:
                        price = float(item['price'])
                        menu_text += f"• {item['name']} - {price:.2f} ₽\n"
                        if item.get('description'):
                            menu_text += f"  {item['description']}\n"
                    menu_text += "\n"
                
                await message.answer(menu_text)
    except Exception as e:
        logger.error(f"Error showing menu: {str(e)}")
        await message.answer("❌ Произошла ошибка при загрузке меню. Пожалуйста, попробуйте позже.")

@dp.callback_query(lambda c: c.data.startswith("show_menu_"))
async def show_menu_callback(callback_query: types.CallbackQuery):
    """Обработчик выбора организации для просмотра меню"""
    org_id = int(callback_query.data.split("_")[2])
    await show_organization_menu(callback_query.message, org_id)
    await callback_query.answer()

@dp.callback_query(lambda c: c.data == "my_organizations")
async def my_organizations_callback(callback_query: types.CallbackQuery):
    """Обработчик кнопки 'Мои организации'"""
    try:
        async with aiohttp.ClientSession() as session:
            # Сначала получаем ID пользователя из базы данных
            async with session.get(f"{API_URL}/users/telegram/{callback_query.from_user.id}") as resp:
                if resp.status != 200:
                    raise Exception(f"Failed to get user: {await resp.text()}")
                user = await resp.json()

            # Теперь получаем список организаций пользователя по его ID в базе данных
            async with session.get(f"{API_URL}/organizations?owner_id={user['id']}") as resp:
                if resp.status != 200:
                    raise Exception(f"Failed to get organizations: {await resp.text()}")
                organizations = await resp.json()

            if not organizations:
                await callback_query.message.edit_text(
                    "У вас пока нет организаций. Создайте организацию командой /create_org",
                    reply_markup=get_main_buttons()
                )
                return

            # Создаем клавиатуру с организациями
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text=org['name'], callback_data=f"org_actions_{org['id']}")]
                    for org in organizations
                ] + [[InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_main")]]
            )

            await callback_query.message.edit_text(
                "Выберите организацию:",
                reply_markup=keyboard
            )
    except Exception as e:
        logger.error(f"Error fetching organizations: {str(e)}")
        await callback_query.message.edit_text(
            "❌ Произошла ошибка при загрузке организаций. Пожалуйста, попробуйте позже.",
            reply_markup=get_main_buttons()
        )
    await callback_query.answer()

@dp.callback_query(lambda c: c.data.startswith("org_actions_"))
async def organization_actions_callback(callback_query: types.CallbackQuery):
    """Обработчик действий с организацией"""
    org_id = int(callback_query.data.split("_")[2])
    
    try:
        async with aiohttp.ClientSession() as session:
            # Получаем информацию об организации
            async with session.get(f"{API_URL}/organizations/{org_id}") as resp:
                if resp.status != 200:
                    raise Exception(f"Failed to get organization: {await resp.text()}")
                org = await resp.json()

            # Создаем клавиатуру с действиями
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="📋 Показать меню", callback_data=f"show_menu_{org_id}")],
                    [InlineKeyboardButton(text="🌐 Сгенерировать веб-страницу", callback_data=f"generate_web_{org_id}")],
                    [InlineKeyboardButton(text="◀️ Назад к списку", callback_data="my_organizations")]
                ]
            )

            await callback_query.message.edit_text(
                f"Организация: {org['name']}\n"
                f"Описание: {org['description'] or 'Нет описания'}\n\n"
                "Выберите действие:",
                reply_markup=keyboard
            )
    except Exception as e:
        logger.error(f"Error in organization actions: {str(e)}")
        await callback_query.message.edit_text(
            "❌ Произошла ошибка. Пожалуйста, попробуйте позже.",
            reply_markup=get_main_buttons()
        )
    await callback_query.answer()

@dp.callback_query(lambda c: c.data.startswith("generate_web_"))
async def generate_web_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик кнопки генерации веб-страницы"""
    query = update.callback_query
    await query.answer()
    
    # Получаем ID организации из callback_data
    org_id = int(query.data.split(':')[1])
    
    try:
        # Получаем список доступных тем
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{API_URL}/api/themes") as response:
                if response.status == 200:
                    data = await response.json()
                    themes = data['themes']
                else:
                    await query.message.reply_text("Ошибка при получении списка тем")
                    return
    except Exception as e:
        await query.message.reply_text(f"Ошибка при получении списка тем: {str(e)}")
        return

    # Создаем клавиатуру с темами
    keyboard = []
    for theme_id, theme_name in themes.items():
        keyboard.append([InlineKeyboardButton(
            theme_name,
            callback_data=f"theme:{org_id}:{theme_id}"
        )])

    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text(
        "Выберите стиль оформления меню:",
        reply_markup=reply_markup
    )

async def theme_selected_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик выбора темы"""
    query = update.callback_query
    await query.answer()
    
    # Получаем ID организации и тему из callback_data
    _, org_id, theme = query.data.split(':')
    
    try:
        # Генерируем страницу меню
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{API_URL}/api/organizations/{org_id}/menu/generate",
                json={"theme": theme}
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    url = data['url']
                    await query.message.reply_text(
                        f"Страница меню успешно сгенерирована!\n"
                        f"Вы можете просмотреть её по ссылке:\n{url}"
                    )
                else:
                    error_data = await response.json()
                    await query.message.reply_text(
                        f"Ошибка при генерации страницы: {error_data.get('detail', 'Неизвестная ошибка')}"
                    )
    except Exception as e:
        await query.message.reply_text(f"Ошибка при генерации страницы: {str(e)}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(dp.start_polling(bot))