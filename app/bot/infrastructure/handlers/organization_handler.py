import os
import aiohttp
from aiogram import Bot
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from app.bot.infrastructure.handlers.base_handler import BaseHandler
from app.bot.infrastructure.logging.logger import Logger
from app.bot.infrastructure.keyboards.organization_keyboard import get_main_buttons, get_back_to_org_buttons

class OrganizationHandler(BaseHandler):
    """Handler for organization-related operations"""
    
    def __init__(self, bot: Bot, logger: Logger):
        super().__init__(bot, logger)
        self.api_url = os.getenv("API_URL")
        
    async def handle_start(self, message: Message):
        """Handle /start command"""
        await self.log_user_info(message)
        try:
            # Try to register user
            success = await self.register_user(message.from_user.id)
            
            # Send welcome message in any case
            await message.answer(
                "👋 Добро пожаловать в Menu Generator Bot!\n\n"
                "Я помогу вам создать красивое меню для вашего заведения. "
                "Выберите действие из меню ниже:",
                reply_markup=get_main_buttons()
            )
            
            if not success:
                self.logger.error(f"Failed to register user {message.from_user.id}")
                
        except Exception as e:
            self.logger.error(f"Error in cmd_start: {str(e)}")
            await message.answer(
                "❌ Произошла ошибка. Пожалуйста, попробуйте позже или обратитесь в поддержку.",
                reply_markup=get_main_buttons()
            )
            
    async def register_user(self, user_id: int) -> bool:
        """Register user in the database"""
        try:
            self.logger.info(f"Attempting to register user {user_id} with API at {self.api_url}")
            async with aiohttp.ClientSession() as session:
                url = f"{self.api_url}/register_user?tid={user_id}"
                self.logger.info(f"Making POST request to {url}")
                
                async with session.post(url) as resp:
                    response_text = await resp.text()
                    self.logger.info(f"API response status: {resp.status}, body: {response_text}")
                    
                    # Even if user already exists (409), consider it success
                    if resp.status in (200, 409):
                        try:
                            user_data = await resp.json()
                            self.logger.info(f"User {user_id} processed successfully: {user_data}")
                        except:
                            self.logger.warning(f"Could not parse JSON response for user {user_id}")
                        return True
                    else:
                        self.logger.error(f"Failed to register user {user_id}: {response_text}")
                        return False
                        
        except Exception as e:
            self.logger.error(f"Error registering user {user_id}: {str(e)}")
            return False
            
    async def handle_create_org(self, callback_query: CallbackQuery, state: FSMContext):
        """Handle organization creation start"""
        await callback_query.message.edit_text(
            text="Введите название вашей организации:"
        )
        await state.set_state(OrganizationStates.waiting_for_name)
        await callback_query.answer()
        
    async def handle_org_name(self, message: Message, state: FSMContext):
        """Handle organization name input"""
        await state.update_data(org_name=message.text)
        await message.answer(
            text="Отлично! Теперь введите описание вашей организации:"
        )
        await state.set_state(OrganizationStates.waiting_for_description)
        
    async def handle_org_description(self, message: Message, state: FSMContext):
        """Handle organization description input"""
        await state.update_data(org_description=message.text)
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="📋 Загрузить файл меню", callback_data="upload_menu_file")],
                [InlineKeyboardButton(text="📋 Загрузить меню через GOOGLE sheets", callback_data="upload_menu_sheets")]
            ]
        )
        
        # Get organization data from state
        data = await state.get_data()
        org_name = data.get('org_name', 'организации')
        
        await message.answer(
            f"✅ Выберете способ загрузки меню '{org_name}'\n\n",
            reply_markup=keyboard
        )
        await state.set_state(OrganizationStates.waiting_for_type)
        
    async def handle_my_organizations(self, callback_query: CallbackQuery):
        """Handle my organizations button"""
        try:
            async with aiohttp.ClientSession() as session:
                # First get user ID from database
                async with session.get(f"{self.api_url}/users/telegram/{callback_query.from_user.id}") as resp:
                    if resp.status != 200:
                        raise Exception(f"Failed to get user: {await resp.text()}")
                    user = await resp.json()
                    
                # Now get list of user's organizations by their database ID
                async with session.get(f"{self.api_url}/organizations?owner_id={user['id']}") as resp:
                    if resp.status != 200:
                        raise Exception(f"Failed to get organizations: {await resp.text()}")
                    organizations = await resp.json()
                    
                if not organizations:
                    await callback_query.message.edit_text(
                        "У вас пока нет организаций.",
                        reply_markup=get_main_buttons()
                    )
                    return
                    
                # Create keyboard with organizations
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
            self.logger.error(f"Error fetching organizations: {str(e)}")
            await callback_query.message.edit_text(
                "❌ Произошла ошибка при загрузке организаций. Пожалуйста, попробуйте позже.",
                reply_markup=get_main_buttons()
            )
        await callback_query.answer()
        
    async def handle_org_actions(self, callback_query: CallbackQuery):
        """Handle organization actions"""
        org_id = int(callback_query.data.split("_")[2])
        try:
            async with aiohttp.ClientSession() as session:
                # Get organization information
                async with session.get(f"{self.api_url}/organizations/{org_id}") as resp:
                    if resp.status != 200:
                        raise Exception(f"Failed to get organization: {await resp.text()}")
                    org = await resp.json()
                    
                # Create keyboard with actions
                keyboard = InlineKeyboardMarkup(
                    inline_keyboard=[
                        [InlineKeyboardButton(text="📋 Показать QR код страницы", callback_data=f"qrcode_{org_id}")],
                        [InlineKeyboardButton(text="📋 Загрузить Изображения", callback_data=f"upload_images_{org_id}")],
                        [InlineKeyboardButton(text="🎨 Загрузить фоны", callback_data=f"upload_backgrounds_{org_id}")],
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
            self.logger.error(f"Error in organization actions: {str(e)}")
            await callback_query.message.edit_text(
                "❌ Произошла ошибка. Пожалуйста, попробуйте позже.",
                reply_markup=get_main_buttons()
            )
        await callback_query.answer() 