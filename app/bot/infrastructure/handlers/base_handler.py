from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from aiogram import Bot, Dispatcher
from aiogram.types import Message, CallbackQuery
from ...domain.exceptions import DomainException
from app.bot.infrastructure.logging.logger import Logger

class BaseHandler(ABC):
    """Base class for all handlers"""
    
    def __init__(self, bot: Bot, dp: Dispatcher, logger: Logger):
        self.bot = bot
        self.dp = dp
        self.logger = logger
        self._register_handlers()

    @abstractmethod
    def _register_handlers(self) -> None:
        """Register message and callback handlers"""
        pass

    async def _handle_domain_exception(self, message: Message, error: DomainException) -> None:
        """Handle domain exceptions and send appropriate response to user"""
        error_messages = {
            ValidationError: "Проверьте правильность введенных данных",
            EntityNotFoundError: "Запрашиваемый объект не найден",
            DuplicateEntityError: "Такой объект уже существует",
            InvalidOperationError: "Операция не может быть выполнена в текущем состоянии",
            FileOperationError: "Ошибка при работе с файлом",
            QRCodeGenerationError: "Ошибка при генерации QR-кода",
            ImageProcessingError: "Ошибка при обработке изображения"
        }
        
        error_message = error_messages.get(type(error), "Произошла ошибка при выполнении операции")
        await message.answer(error_message)

    async def _handle_callback_domain_exception(self, callback: CallbackQuery, error: DomainException) -> None:
        """Handle domain exceptions for callback queries"""
        error_messages = {
            ValidationError: "Проверьте правильность введенных данных",
            EntityNotFoundError: "Запрашиваемый объект не найден",
            DuplicateEntityError: "Такой объект уже существует",
            InvalidOperationError: "Операция не может быть выполнена в текущем состоянии",
            FileOperationError: "Ошибка при работе с файлом",
            QRCodeGenerationError: "Ошибка при генерации QR-кода",
            ImageProcessingError: "Ошибка при обработке изображения"
        }
        
        error_message = error_messages.get(type(error), "Произошла ошибка при выполнении операции")
        await callback.answer(error_message, show_alert=True)

    async def log_user_info(self, message):
        """Log user information"""
        user = message.from_user
        chat = message.chat
        self.logger.info(
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