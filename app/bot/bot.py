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
import traceback

from pydantic import BaseModel


# from front import get_main_buttons, get_help_buttons, get_organization_buttons, get_theme_buttons, get_back_to_org_buttons, log_user_info

API_URL = os.getenv("API_URL")
BOT_TOKEN = os.getenv("BOT_TOKEN")
GEN_URL ='http://genhtm:2424'
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
        logger.info(f"Attempting to register user {user_id} with API at {API_URL}")
        async with aiohttp.ClientSession() as session:
            url = f"{API_URL}/register_user?tid={user_id}"
            logger.info(f"Making POST request to {url}")
            async with session.post(url) as resp:
                response_text = await resp.text()
                logger.info(f"API response status: {resp.status}, body: {response_text}")
                if resp.status == 200:
                    user_data = await resp.json()
                    logger.info(f"User {user_id} registered successfully: {user_data}")
                    return True
                else:
                    logger.error(f"Failed to register user {user_id}: {response_text}")
                    return False
    except Exception as e:
        logger.error(f"Error registering user {user_id}: {str(e)}")
        logger.error(traceback.format_exc())
        return False
#def for menu
#Main menu
def get_main_buttons() -> InlineKeyboardMarkup:
    """Создает инлайн кнопки для основного меню"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📝 Создать организацию", callback_data="create_org")],
            [InlineKeyboardButton(text="🏢 Мои организации", callback_data="my_organizations")],
            [InlineKeyboardButton(text="❓ Помощь", callback_data="help")]
        ]
    )
    return keyboard
#Help menu
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
            [InlineKeyboardButton(text="🏢 Мои организации", callback_data="my_organizations")],
            [InlineKeyboardButton(text="❓ Помощь", callback_data="help")]
        ]
    )
    return keyboard

def get_theme_buttons(org_id: int) -> InlineKeyboardMarkup:
    """Создает инлайн кнопки для выбора темы"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Современный темный", callback_data=f"theme_{org_id}_modern-dark")],
            [InlineKeyboardButton(text="Светлый элегантный", callback_data=f"theme_{org_id}_light-elegant")],
            [InlineKeyboardButton(text="Минималистичный", callback_data=f"theme_{org_id}_minimal")],
            [InlineKeyboardButton(text="Винтажный", callback_data=f"theme_{org_id}_vintage")],
            [InlineKeyboardButton(text="Футуристический", callback_data=f"theme_{org_id}_futuristic")],
            [InlineKeyboardButton(text="Природный", callback_data=f"theme_{org_id}_nature")],
            [InlineKeyboardButton(text="◀️ Назад", callback_data=f"org_actions_{org_id}")]
        ]
    )
    return keyboard

def get_back_to_org_buttons(org_id: int) -> InlineKeyboardMarkup:
    """Создает инлайн кнопки для возврата к организации"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="◀️ Назад к организации", callback_data=f"org_actions_{org_id}")]
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
#_________________________________________________________________________________________________________
#Comands
# Start
@dp.message(Command("start"))
async def cmd_start(message: Message):
    """Обработчик команды /start"""
    log_user_info(message)
    
    # Регистрируем пользователя только если это первое сообщение
    if message.message_id == 1:
        success = await register_user(message.from_user.id)
        if success:
            await message.answer(
                reply_markup=get_main_buttons()
            )
        else:
            await message.answer(
                "❌ Произошла ошибка при регистрации. Пожалуйста, попробуйте позже."
            )
    else:
        await message.answer(
            "👋 Привет!\n\n"
            "Я бот для управления меню. Используйте следующие команды:\n"
            "/menu - Просмотр меню\n"
            "/help - Получить помощь",
            reply_markup=get_main_buttons()
        )
# Создать организацию
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
                print(f'\nSending user data\n {user}\n')

            # Создаем организацию
            form_data = aiohttp.FormData()
            form_data.add_field('name', org_name)
            form_data.add_field('description', org_description)
            form_data.add_field('owner_id', str(user['id'])) 
            print(form_data) # Используем ID из таблицы users
            async with session.post(f"{API_URL}/organizations", data=form_data) as resp:
                if resp.status != 200:
                    raise Exception(f"Failed to create organization: {await resp.text()}")
                org = await resp.json()
                print('Организация записана в базу')

            # Загружаем меню
            with open(file_path, 'rb') as f:
                files = {'file': f}
                async with session.post(f"{API_URL}/organizations/{org['id']}/menu", data=files) as resp:
                    if resp.status != 200:
                        raise Exception(f"Failed to upload menu: {await resp.text()}")

        # Удаляем временный файл
        os.remove(file_path)

        await message.answer(
            f"✅ Организация '{org_name}' успешно создана!\n\n",
            reply_markup=get_main_buttons()

        )
    except Exception as e:
        logger.error(f"Error creating organization: {str(e)}")
        await message.answer(
            f"❌ Произошла ошибка при создании организации. Пожалуйста, попробуйте позже. {str(e)}"
        )
    finally:
        await state.clear()

@dp.callback_query(lambda c: c.data == "help")
async def help_callback(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(        
        reply_markup=get_help_buttons()
    )
    await callback_query.answer()

@dp.callback_query(lambda c: c.data == "back_to_main")
async def back_to_main_callback(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(
        "👋 Выберите действие:\n\n",
        reply_markup=get_main_buttons()
    )
    await callback_query.answer()

#Help menu 
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
#Кнопка Мои организации
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


# Generate Menu Page
@dp.callback_query(lambda c: c.data.startswith("generate_web_"))
async def generate_web_callback(callback_query: types.CallbackQuery):
    """Обработчик генерации веб-страницы меню"""
    org_id = int(callback_query.data.split('_')[-1])
    await callback_query.message.edit_text(
        "Выберите тему для вашего меню:",
        reply_markup=get_theme_buttons(org_id)
    )
    await callback_query.answer()




@dp.callback_query(lambda c: c.data.startswith("theme_"))
async def theme_selected_callback(callback_query: types.CallbackQuery):
    """Обработчик выбора темы"""
    data = callback_query.data.split('_')    
    theme= data[-1]
    org_id = int(data[-2])
    try:
        async with aiohttp.ClientSession() as session:
            # Получаем информацию об организации
            async with session.get(f"{API_URL}/organizations/{org_id}") as resp:
                if resp.status != 200:
                    raise Exception(f"Failed to get organization: {await resp.text()}")
                org = await resp.json()
        async with aiohttp.ClientSession() as session:
            # Получаем информацию о меню
            async with session.get(f"{API_URL}/organizations/{org_id}/menu") as resp:
                if resp.status != 200:
                    raise Exception(f"Failed to get organization: {await resp.text()}")
                menu_items = await resp.json()

        content = {}
        for item in menu_items:            
            if item['category'] not in content:
                content[item['category']] = []
            entity = {'name': item['name'],
                      'price': item['price'],
                      'description': item['description'],
                      'subcategory': item['subcategory']}
            content[item['category']].append(entity)
        
        # print(org)
        data = {'page_name': org['menu_table_name'],
                'title': org['name'],
                'description': org['description'],
                'theme': theme,
                'content': content
                   }
        print(data)
 
    except Exception as e:
        logger.error(f"Error in organization actions: {str(e)}")
    try:
        #Menu Generation
        async with aiohttp.ClientSession() as session:
            # Получаем информацию об организации
            async with session.post(f"{GEN_URL}/generate", json=data) as resp:
                if resp.status == 200:
                    result = await resp.json()
                    menu_url = result.get('url')
                    await callback_query.message.edit_text(
                        f"✅ Ваше меню успешно сгенерировано!\n\n"
                        f"🔗 Ссылка на меню: {menu_url}\n\n"
                        f"Вы можете поделиться этой ссылкой с вашими клиентами.",
                        reply_markup=get_back_to_org_buttons(org_id)
                    )
                else:
                    error_text = await resp.text()
                    await callback_query.message.edit_text(
                        f"❌ Ошибка при генерации меню: {error_text}",
                        reply_markup=get_back_to_org_buttons(org_id)
                    )
    except Exception as e:
        logger.error(f"Error generating menu: {str(e)}")
        await callback_query.message.edit_text(
            f"❌ Произошла ошибка при генерации меню: {str(e)}",
            reply_markup=get_back_to_org_buttons(org_id)
        )
    await callback_query.answer()
#____________________________________________________________________________________________________________
if __name__ == "__main__":
    import asyncio
    asyncio.run(dp.start_polling(bot))