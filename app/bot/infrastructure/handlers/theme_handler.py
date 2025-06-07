import os
import aiohttp
from aiogram import Bot
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from app.bot.infrastructure.handlers.base_handler import BaseHandler
from app.bot.infrastructure.logging.logger import Logger
from app.bot.infrastructure.keyboards.organization_keyboard import get_back_to_org_buttons

class ThemeHandler(BaseHandler):
    """Handler for theme-related operations"""
    
    def __init__(self, bot: Bot, logger: Logger):
        super().__init__(bot, logger)
        self.api_url = os.getenv("API_URL")
        
    async def handle_show_themes(self, callback_query: CallbackQuery):
        """Show available themes"""
        org_id = int(callback_query.data.split("_")[2])
        try:
            async with aiohttp.ClientSession() as session:
                # Get available themes
                async with session.get(f"{self.api_url}/themes") as resp:
                    if resp.status != 200:
                        raise Exception(f"Failed to get themes: {await resp.text()}")
                    themes = await resp.json()
                    
                    if not themes:
                        await callback_query.message.answer("❌ Нет доступных тем")
                        return
                        
                # Create keyboard with themes
                keyboard = InlineKeyboardMarkup(
                    inline_keyboard=[
                        [InlineKeyboardButton(text=theme['name'], callback_data=f"select_theme_{org_id}_{theme['id']}")]
                        for theme in themes
                    ] + [[InlineKeyboardButton(text="◀️ Назад", callback_data=f"org_actions_{org_id}")]]
                )
                
                await callback_query.message.answer(
                    "🎨 Выберите тему для вашей организации:",
                    reply_markup=keyboard
                )
                
        except Exception as e:
            self.logger.error(f"Error showing themes: {str(e)}")
            await callback_query.message.answer(
                "❌ Произошла ошибка при загрузке тем. Пожалуйста, попробуйте позже."
            )
            
    async def handle_select_theme(self, callback_query: CallbackQuery):
        """Handle theme selection"""
        _, _, org_id, theme_id = callback_query.data.split("_")
        org_id = int(org_id)
        theme_id = int(theme_id)
        
        try:
            async with aiohttp.ClientSession() as session:
                # Update organization theme
                async with session.put(
                    f"{self.api_url}/organizations/{org_id}/theme",
                    json={"theme_id": theme_id}
                ) as resp:
                    if resp.status != 200:
                        raise Exception(f"Failed to update theme: {await resp.text()}")
                        
                await callback_query.message.answer(
                    "✅ Тема успешно обновлена!",
                    reply_markup=get_back_to_org_buttons(org_id)
                )
                
        except Exception as e:
            self.logger.error(f"Error selecting theme: {str(e)}")
            await callback_query.message.answer(
                "❌ Произошла ошибка при обновлении темы. Пожалуйста, попробуйте позже."
            )
            
    async def handle_preview_theme(self, callback_query: CallbackQuery):
        """Show theme preview"""
        _, _, org_id, theme_id = callback_query.data.split("_")
        org_id = int(org_id)
        theme_id = int(theme_id)
        
        try:
            async with aiohttp.ClientSession() as session:
                # Get theme preview
                async with session.get(f"{self.api_url}/themes/{theme_id}/preview") as resp:
                    if resp.status != 200:
                        raise Exception(f"Failed to get theme preview: {await resp.text()}")
                    preview = await resp.json()
                    
                # Create keyboard with preview options
                keyboard = InlineKeyboardMarkup(
                    inline_keyboard=[
                        [InlineKeyboardButton(text="✅ Применить тему", callback_data=f"select_theme_{org_id}_{theme_id}")],
                        [InlineKeyboardButton(text="◀️ Назад к темам", callback_data=f"show_themes_{org_id}")]
                    ]
                )
                
                await callback_query.message.answer(
                    f"🎨 Предпросмотр темы:\n\n{preview['description']}",
                    reply_markup=keyboard
                )
                
        except Exception as e:
            self.logger.error(f"Error showing theme preview: {str(e)}")
            await callback_query.message.answer(
                "❌ Произошла ошибка при загрузке предпросмотра темы. Пожалуйста, попробуйте позже."
            ) 