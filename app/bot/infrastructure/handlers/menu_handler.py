import os
import aiohttp
from aiogram import Bot
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from app.bot.infrastructure.handlers.base_handler import BaseHandler
from app.bot.infrastructure.logging.logger import Logger
from app.bot.infrastructure.keyboards.organization_keyboard import get_back_to_org_buttons

class MenuHandler(BaseHandler):
    """Handler for menu-related operations"""
    
    def __init__(self, bot: Bot, logger: Logger):
        super().__init__(bot, logger)
        self.api_url = os.getenv("API_URL")
        
    async def handle_show_menu(self, callback_query: CallbackQuery):
        """Show organization menu"""
        org_id = int(callback_query.data.split("_")[2])
        try:
            async with aiohttp.ClientSession() as session:
                # Get organization menu
                async with session.get(f"{self.api_url}/organizations/{org_id}/menu") as resp:
                    if resp.status != 200:
                        raise Exception(f"Failed to get menu: {await resp.text()}")
                    menu_items = await resp.json()
                    
                    if not menu_items:
                        await callback_query.message.answer("📋 Меню пусто")
                        return
                        
                # Group dishes by categories
                categories = {}
                for item in menu_items:
                    if item['is_available']:
                        category = item['category']
                        if category not in categories:
                            categories[category] = []
                        categories[category].append(item)
                        
                # Form message
                menu_text = "📋 Наше меню:\n\n"
                
                for category, items in categories.items():
                    menu_text += f"🍽 {category}:\n"
                    for item in items:
                        price = float(item['price'])
                        menu_text += f"• {item['name']} - {price:.2f} ₽\n"
                        if item.get('description'):
                            menu_text += f"  {item['description']}\n"
                    menu_text += "\n"
                    
                await callback_query.message.answer(menu_text)
                
        except Exception as e:
            self.logger.error(f"Error showing menu: {str(e)}")
            await callback_query.message.answer(
                "❌ Произошла ошибка при загрузке меню. Пожалуйста, попробуйте позже."
            )
            
    async def handle_menu_upload(self, message: Message, state: FSMContext):
        """Handle menu file upload"""
        data = await state.get_data()
        upload_type = data.get('type_of_menu_upload')
        
        if upload_type == "upload_menu_file":
            if not message.document:
                await message.answer(
                    "Пожалуйста, отправьте файл с меню в формате CSV."
                )
                return
                
            try:
                # Download file
                file_id = message.document.file_id
                file = await self.bot.get_file(file_id)
                file_path = f"temp_{file_id}.{message.document.file_name.split('.')[-1]}"
                
                # Use correct method for downloading
                await self.bot.download_file(file.file_path, file_path)
                
                # Send data to API
                async with aiohttp.ClientSession() as session:
                    # Register user
                    async with session.post(f"{self.api_url}/register_user?tid={message.from_user.id}") as resp:
                        if resp.status != 200:
                            raise Exception(f"Failed to register user: {await resp.text()}")
                        user = await resp.json()
                    
                    # Create organization
                    form_data = aiohttp.FormData()
                    form_data.add_field('name', data['org_name'])
                    form_data.add_field('description', data['org_description'])
                    form_data.add_field('owner_id', str(user['id']))
                    
                    async with session.post(f"{self.api_url}/organizations", data=form_data) as resp:
                        if resp.status != 200:
                            raise Exception(f"Failed to create organization: {await resp.text()}")
                        org = await resp.json()
                    
                    # Upload menu
                    with open(file_path, 'rb') as f:
                        form = aiohttp.FormData()
                        form.add_field('file', f, filename=message.document.file_name)
                        async with session.post(f"{self.api_url}/organizations/{org['id']}/menu", data=form) as resp:
                            if resp.status != 200:
                                raise Exception(f"Failed to upload menu: {await resp.text()}")
                
                # Create keyboard for further actions
                keyboard = InlineKeyboardMarkup(
                    inline_keyboard=[
                        [InlineKeyboardButton(text="📋 Показать меню", callback_data=f"show_menu_{org['id']}")],
                        [InlineKeyboardButton(text="📋 Загрузить Изображения", callback_data=f"upload_images_{org['id']}")],
                        [InlineKeyboardButton(text="🌐 Сгенерировать веб-страницу", callback_data=f"generate_web_{org['id']}")],
                        [InlineKeyboardButton(text="◀️ Назад к списку", callback_data="my_organizations")]
                    ]
                )
                
                # Delete temporary file
                os.remove(file_path)
                
                await message.answer(
                    f"✅ Организация '{data['org_name']}' успешно создана!\n\n",
                    reply_markup=keyboard
                )
                
                # Clear state
                await state.clear()
                
            except Exception as e:
                self.logger.error(f"Error creating organization: {str(e)}")
                await message.answer(
                    f"❌ Произошла ошибка при создании организации: {str(e)}\nПожалуйста, попробуйте позже."
                )
                
        else:  # upload_menu_sheets
            try:
                sheets_id = message.text.strip()
                # TODO: Add Google Sheets logic
                await message.answer(
                    "Извините, загрузка через Google Sheets временно недоступна."
                )
            except Exception as e:
                self.logger.error(f"Error processing Google Sheets: {str(e)}")
                await message.answer(
                    "❌ Произошла ошибка при обработке Google Sheets ID."
                ) 