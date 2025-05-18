import os
import logging
import aiohttp
# from collections import defaultdict
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

API_URL = os.getenv("API_URL")
BOT_TOKEN = os.getenv("BOT_TOKEN")
GEN_URL ='http://genhtm:2424'
# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
#Bot autorization
bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher(storage=MemoryStorage())
# Состояния для создания организации
class OrganizationStates(StatesGroup):
    waiting_for_name = State()
    waiting_for_description = State()
    waiting_for_type = State()
    waiting_for_menu = State()
    waiting_for_description_images = State()
    waiting_for_images = State()

# Временное хранилище для альбомов
SAVE_FOLDER = "static/images"
os.makedirs(SAVE_FOLDER, exist_ok=True)
# media_groups = #defaultdict(list)

#Buttons__________________________________________________________________________________________
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
#Theme menu
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
#Back menu
def get_action_before_create_buttons(org_id: int) -> InlineKeyboardMarkup:
    """Создает инлайн кнопки для возврата к организации"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📋 Загрузить Изображения", callback_data=f"upload_images_{org_id}")],
            [InlineKeyboardButton(text="◀️ Назад к организации", callback_data=f"org_actions_{org_id}")]
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
#Comands______________________________________________________________________________

# Start/ registring
@dp.message(Command("start"))
async def cmd_start(message: Message):
    """Обработчик команды /start"""
    log_user_info(message)    
    try:
        # Пытаемся зарегистрировать пользователя
        success = await register_user(message.from_user.id)
        
        # Отправляем приветственное сообщение в любом случае
        await message.answer(
            "👋 Добро пожаловать в Menu Generator Bot!\n\n"
            "Я помогу вам создать красивое меню для вашего заведения. "
            "Выберите действие из меню ниже:",
            reply_markup=get_main_buttons()
        )
        
        if not success:
            logger.error(f"Failed to register user {message.from_user.id}")
            
    except Exception as e:
        logger.error(f"Error in cmd_start: {str(e)}")
        logger.error(traceback.format_exc())
        await message.answer(
            "❌ Произошла ошибка. Пожалуйста, попробуйте позже или обратитесь в поддержку.",
            reply_markup=get_main_buttons()
        )
#User register or auth
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
                
                # Даже если пользователь уже существует (409), считаем это успехом
                if resp.status in (200, 409):
                    try:
                        user_data = await resp.json()
                        logger.info(f"User {user_id} processed successfully: {user_data}")
                    except:
                        logger.warning(f"Could not parse JSON response for user {user_id}")
                    return True
                else:
                    logger.error(f"Failed to register user {user_id}: {response_text}")
                    return False
                    
    except Exception as e:
        logger.error(f"Error registering user {user_id}: {str(e)}")
        logger.error(traceback.format_exc())
        return False
# Создать организацию_________________________________________________________________
@dp.callback_query(lambda c: c.data == "create_org")
async def create_org_callback(callback_query: types.CallbackQuery, state: FSMContext):
    """Начало процесса создания организации"""
    await callback_query.message.edit_text(
        text="Введите название вашей организации:"
    )
    await state.set_state(OrganizationStates.waiting_for_name)
    await callback_query.answer()

@dp.message(OrganizationStates.waiting_for_name)
async def process_org_name(message: Message, state: FSMContext):
    """Обработка названия организации"""
    await state.update_data(org_name=message.text)
    await message.answer(
        text="Отлично! Теперь введите описание вашей организации:"
    )
    await state.set_state(OrganizationStates.waiting_for_description)

@dp.message(OrganizationStates.waiting_for_description)
async def process_org_description(message: Message, state: FSMContext):
    """Обработка описания организации"""
    await state.update_data(org_description=message.text)    
    keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="📋 Загрузить файл меню", callback_data="upload_menu_file")],
                [InlineKeyboardButton(text="📋 Загрузить меню через GOOGLE sheets", callback_data="upload_menu_sheets")]                
            ]
        )
    # Получаем данные из state
    data = await state.get_data()
    org_name = data.get('org_name', 'организации')
    
    await message.answer(
        f"✅ Выберете способ загрузки меню '{org_name}'\n\n",
        reply_markup=keyboard
    )
    await state.set_state(OrganizationStates.waiting_for_type)

@dp.callback_query(lambda c: c.data in ["upload_menu_file", "upload_menu_sheets"])
async def process_menu_type_selection(callback_query: types.CallbackQuery, state: FSMContext):
    """Обработка выбора типа загрузки меню"""
    await state.update_data(type_of_menu_upload=callback_query.data)
    
    if callback_query.data == "upload_menu_file":
        await callback_query.message.edit_text(
            "Пожалуйста, отправьте файл с меню в формате CSV или Excel."
        )
    else:
        await callback_query.message.edit_text(
            "Пожалуйста, отправьте идентификатор Google таблицы."
        )
    
    await state.set_state(OrganizationStates.waiting_for_menu)
    await callback_query.answer()

@dp.message(OrganizationStates.waiting_for_menu)
async def process_org_menu(message: Message, state: FSMContext):
    """Обработка файла меню"""
    data = await state.get_data()
    upload_type = data.get('type_of_menu_upload')
    
    if upload_type == "upload_menu_file":
        if not message.document:
            await message.answer(
                "Пожалуйста, отправьте файл с меню в формате CSV или Excel."
            )
            return
            
        try:
            # Скачиваем файл
            file_id = message.document.file_id
            file = await bot.get_file(file_id)
            file_path = f"temp_{file_id}.{message.document.file_name.split('.')[-1]}"
            
            # Используем правильный метод для скачивания
            await bot.download_file(file.file_path, file_path)
            
            # Отправляем данные на API
            async with aiohttp.ClientSession() as session:
                # Регистрируем пользователя
                async with session.post(f"{API_URL}/register_user?tid={message.from_user.id}") as resp:
                    if resp.status != 200:
                        raise Exception(f"Failed to register user: {await resp.text()}")
                    user = await resp.json()
                
                # Создаем организацию
                form_data = aiohttp.FormData()
                form_data.add_field('name', data['org_name'])
                form_data.add_field('description', data['org_description'])
                form_data.add_field('owner_id', str(user['id']))
                
                async with session.post(f"{API_URL}/organizations", data=form_data) as resp:
                    if resp.status != 200:
                        raise Exception(f"Failed to create organization: {await resp.text()}")
                    org = await resp.json()
                
                # Загружаем меню
                with open(file_path, 'rb') as f:
                    form = aiohttp.FormData()
                    form.add_field('file', f, filename=message.document.file_name)
                    async with session.post(f"{API_URL}/organizations/{org['id']}/menu", data=form) as resp:
                        if resp.status != 200:
                            raise Exception(f"Failed to upload menu: {await resp.text()}")
            
            # Создаем клавиатуру для дальнейших действий
            keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="📋 Показать меню", callback_data=f"show_menu_{org['id']}")],
                    [InlineKeyboardButton(text="📋 Загрузить Изображения", callback_data=f"upload_images_{org['id']}")],
                    [InlineKeyboardButton(text="🌐 Сгенерировать веб-страницу", callback_data=f"generate_web_{org['id']}")],
                    [InlineKeyboardButton(text="◀️ Назад к списку", callback_data="my_organizations")]
                ]
            )
            
            # Удаляем временный файл
            os.remove(file_path)
            
            await message.answer(
                f"✅ Организация '{data['org_name']}' успешно создана!\n\n",
                reply_markup=keyboard
            )
            
            # Очищаем состояние
            await state.clear()
            
        except Exception as e:
            logger.error(f"Error creating organization: {str(e)}")
            await message.answer(
                f"❌ Произошла ошибка при создании организации: {str(e)}\nПожалуйста, попробуйте позже."
            )
            
    else:  # upload_menu_sheets
        try:
            sheets_id = message.text.strip()
            # TODO: Добавить логику для работы с Google Sheets
            await message.answer(
                "Извините, загрузка через Google Sheets временно недоступна."
            )
        except Exception as e:
            logger.error(f"Error processing Google Sheets: {str(e)}")
            await message.answer(
                "❌ Произошла ошибка при обработке Google Sheets ID."
            )

# Загрузка изображений

@dp.message(OrganizationStates.waiting_for_description_images)
async def process_org_images(message: Message, state: FSMContext):
    """Обработка Изображений организации"""
    await state.update_data(org_description=message.text)
    await message.answer(
        "Теперь отправьте файлы Изображений Позиций Меню.\n"
        "Формат изображения должен быть следующим:\n"
        "Имя файла соответствует названию в таблице меню \n"
        "JPG. Не юолее 200Кб \n"
    )
    await state.set_state(OrganizationStates.waiting_for_images)

@dp.message(OrganizationStates.waiting_for_images)
async def process_upload_images(message: Message, state: FSMContext):
    """Обработка загрузки изображений"""
    try:
        # Проверяем, что сообщение содержит фото
        if not message.photo and not message.document:
            await message.answer(
                text="❌ Пожалуйста, отправьте изображение или документ с изображением."
            )
            return

        # Получаем данные организации
        data = await state.get_data()
        org_id = data.get('org_id')

        if not org_id:
            await message.answer(
                text="❌ Ошибка: не найден ID организации. Пожалуйста, начните процесс заново."
            )
            return

        # Подготавливаем файл для отправки
        if message.photo:
            file_id = message.photo[-1].file_id
            file = await bot.get_file(file_id)
            file_path = file.file_path
            original_filename = f"photo_{file_id}.jpg"
        else:
            file_id = message.document.file_id
            file = await bot.get_file(file_id)
            file_path = file.file_path
            original_filename = message.document.file_name

        # Скачиваем файл
        downloaded_file = await bot.download_file(file_path)

        # Отправляем файл через API
        async with aiohttp.ClientSession() as session:
            form = aiohttp.FormData()
            form.add_field('files', downloaded_file, filename=original_filename)
            
            async with session.post(
                f"{API_URL}/organizations/{org_id}/images",
                data=form
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    logger.info(f"Successfully uploaded image: {result}")
                    
                    # Сохраняем информацию о загруженных изображениях
                    images = data.get('_images', [])
                    images.extend(result['uploaded_images'])
                    await state.update_data(_images=images)
                    
                    await message.answer(
                        text="✅ Изображение успешно загружено!\n"
                        "Отправьте следующее изображение или нажмите кнопку 'Завершить' когда закончите.",
                        reply_markup=get_back_to_org_buttons(org_id)
                    )
                else:
                    error_text = await response.text()
                    logger.error(f"Error uploading image: {error_text}")
                    await message.answer(
                        text="❌ Произошла ошибка при загрузке изображения. Пожалуйста, попробуйте снова."
                    )

    except Exception as e:
        logger.error(f"Error in process_upload_images: {str(e)}")
        logger.error(traceback.format_exc())
        await message.answer(
            text="❌ Произошла ошибка при обработке изображения. Пожалуйста, попробуйте снова."
        )

@dp.callback_query(lambda c: c.data == "back_to_main")
async def back_to_main_callback(callback_query: types.CallbackQuery):
    await callback_query.message.edit_text(
        "👋 Выберите действие:\n\n",
        reply_markup=get_main_buttons()
    )
    await callback_query.answer()

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
                    "У вас пока нет организаций.",
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
                    [InlineKeyboardButton(text="📋 Загрузить Изображения", callback_data=f"upload_images_{org_id}")],
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
    """Обработчик выбора темы и генерация"""
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
    # Формируем данные для отправки
        content = {}
        for item in menu_items:            
            if item['category'] not in content:
                content[item['category']] = []
            entity = {'name': item['name'],
                      'price': item['price'],
                      'description': item['description'],
                      'subcategory': item['subcategory']}
            content[item['category']].append(entity)        
        data = {'page_name': org['menu_table_name'],
                'title': org['name'],
                'description': org['description'],
                'theme': theme,
                'content': content
                   }
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
#____________________________________________________________________________________________________________
if __name__ == "__main__":
    import asyncio
    asyncio.run(dp.start_polling(bot))