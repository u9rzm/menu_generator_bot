import os
from aiogram import Bot
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from app.bot.infrastructure.handlers.base_handler import BaseHandler
from app.bot.infrastructure.logging.logger import Logger

class HelpHandler(BaseHandler):
    """Handler for help-related operations"""
    
    def __init__(self, bot: Bot, logger: Logger):
        super().__init__(bot, logger)
        
    async def handle_help(self, message: Message):
        """Show help message"""
        help_text = (
            "🤖 *Бот для управления организациями*\n\n"
            "*Основные команды:*\n"
            "/start - Начать работу с ботом\n"
            "/help - Показать это сообщение\n"
            "/create_org - Создать новую организацию\n"
            "/my_orgs - Показать список ваших организаций\n\n"
            "*Управление организацией:*\n"
            "• Загрузка меню\n"
            "• Управление изображениями\n"
            "• Генерация QR-кодов\n"
            "• Настройка темы\n\n"
            "*Дополнительная информация:*\n"
            "Для получения подробной информации о конкретной функции, "
            "используйте соответствующие кнопки в меню организации."
        )
        
        await message.answer(help_text, parse_mode="Markdown")
        
    async def handle_help_callback(self, callback_query: CallbackQuery):
        """Handle help callback queries"""
        help_type = callback_query.data.split("_")[1]
        
        help_texts = {
            "menu": (
                "📋 *Управление меню*\n\n"
                "• Загрузка меню через CSV файл\n"
                "• Просмотр текущего меню\n"
                "• Редактирование позиций\n"
                "• Управление категориями\n\n"
                "Для загрузки меню используйте кнопку 'Загрузить меню' "
                "и отправьте CSV файл в следующем формате:\n"
                "категория,название,цена,описание"
            ),
            "images": (
                "📸 *Управление изображениями*\n\n"
                "• Загрузка изображений\n"
                "• Просмотр галереи\n"
                "• Удаление изображений\n\n"
                "Поддерживаемые форматы: JPG, PNG, GIF\n"
                "Максимальный размер: 10MB"
            ),
            "qr": (
                "🔲 *Управление QR-кодами*\n\n"
                "• Генерация QR-кодов\n"
                "• Просмотр активных кодов\n"
                "• Удаление кодов\n\n"
                "QR-коды автоматически обновляются при изменении меню"
            ),
            "theme": (
                "🎨 *Управление темой*\n\n"
                "• Выбор готовой темы\n"
                "• Предпросмотр темы\n"
                "• Применение темы\n\n"
                "Тема влияет на внешний вид веб-страницы вашей организации"
            )
        }
        
        if help_type in help_texts:
            await callback_query.message.answer(
                help_texts[help_type],
                parse_mode="Markdown"
            )
        else:
            await callback_query.message.answer(
                "❌ Неизвестный тип помощи. Пожалуйста, выберите из списка."
            )
            
    async def handle_contact(self, message: Message):
        """Show contact information"""
        contact_text = (
            "📞 *Контактная информация*\n\n"
            "По всем вопросам обращайтесь:\n"
            "• Email: support@example.com\n"
            "• Телефон: +7 (999) 123-45-67\n"
            "• Telegram: @support_bot\n\n"
            "Время работы поддержки:\n"
            "Пн-Пт: 9:00 - 18:00 (МСК)"
        )
        
        await message.answer(contact_text, parse_mode="Markdown") 