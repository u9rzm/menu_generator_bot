import os
import aiohttp
from typing import Optional
from aiogram import Bot, Dispatcher
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from ...application.use_cases.manage_qr_code import ManageQRCodeUseCase
from ...domain.models.qr_code import QRCodeType
from ...domain.exceptions import DomainException
from .base_handler import BaseHandler
from .logging.logger import Logger
from .keyboards.organization_keyboard import get_back_to_org_buttons

class QRCodeHandler(BaseHandler):
    """Handler for QR code-related operations"""
    
    def __init__(self, bot: Bot, dp: Dispatcher, qr_code_use_case: ManageQRCodeUseCase, logger: Logger):
        self.qr_code_use_case = qr_code_use_case
        super().__init__(bot, dp)
        self.logger = logger
        self.api_url = os.getenv("API_URL")
        self.gen_url = os.getenv("GEN_URL")

    def _register_handlers(self) -> None:
        """Register message and callback handlers"""
        self.dp.message.register(self.handle_generate_qr, Command("generate_qr"))
        self.dp.message.register(self.handle_get_qr, Command("get_qr"))
        self.dp.message.register(self.handle_delete_qr, Command("delete_qr"))
        self.dp.callback_query.register(self.handle_qr_callback, lambda c: c.data.startswith("qr_"))

    async def handle_generate_qr(self, callback_query: CallbackQuery):
        """Handle QR code generation request"""
        org_id = int(callback_query.data.split("_")[2])
        
        try:
            async with aiohttp.ClientSession() as session:
                # Generate QR code
                async with session.post(f"{self.api_url}/organizations/{org_id}/qr-codes") as resp:
                    if resp.status != 200:
                        raise Exception(f"Failed to generate QR code: {await resp.text()}")
                    qr_code = await resp.json()
                    
                # Create keyboard with QR code options
                keyboard = InlineKeyboardMarkup(
                    inline_keyboard=[
                        [InlineKeyboardButton(text="🗑 Удалить", callback_data=f"delete_qr_{org_id}_{qr_code['id']}")],
                        [InlineKeyboardButton(text="◀️ Назад", callback_data=f"org_actions_{org_id}")]
                    ]
                )
                
                await callback_query.message.answer_photo(
                    photo=f"{self.gen_url}/qr-codes/{qr_code['file_path']}",
                    caption="🔲 QR-код для вашей организации",
                    reply_markup=keyboard
                )
                
        except Exception as e:
            self.logger.error(f"Error generating QR code: {str(e)}")
            await callback_query.message.answer(
                "❌ Произошла ошибка при генерации QR-кода. Пожалуйста, попробуйте позже."
            )
            
    async def handle_show_qr_codes(self, callback_query: CallbackQuery):
        """Show organization QR codes"""
        org_id = int(callback_query.data.split("_")[2])
        
        try:
            async with aiohttp.ClientSession() as session:
                # Get organization QR codes
                async with session.get(f"{self.api_url}/organizations/{org_id}/qr-codes") as resp:
                    if resp.status != 200:
                        raise Exception(f"Failed to get QR codes: {await resp.text()}")
                    qr_codes = await resp.json()
                    
                    if not qr_codes:
                        await callback_query.message.answer(
                            "❌ Нет активных QR-кодов",
                            reply_markup=get_back_to_org_buttons(org_id)
                        )
                        return
                        
                # Create keyboard with QR code options
                keyboard = InlineKeyboardMarkup(
                    inline_keyboard=[
                        [InlineKeyboardButton(
                            text=f"🔲 QR-код #{qr_code['id']}",
                            callback_data=f"show_qr_{org_id}_{qr_code['id']}"
                        )]
                        for qr_code in qr_codes
                    ] + [[InlineKeyboardButton(text="◀️ Назад", callback_data=f"org_actions_{org_id}")]]
                )
                
                await callback_query.message.answer(
                    "🔲 Выберите QR-код для просмотра:",
                    reply_markup=keyboard
                )
                
        except Exception as e:
            self.logger.error(f"Error showing QR codes: {str(e)}")
            await callback_query.message.answer(
                "❌ Произошла ошибка при загрузке QR-кодов. Пожалуйста, попробуйте позже."
            )
            
    async def handle_show_qr(self, callback_query: CallbackQuery):
        """Show specific QR code"""
        _, _, org_id, qr_id = callback_query.data.split("_")
        org_id = int(org_id)
        qr_id = int(qr_id)
        
        try:
            async with aiohttp.ClientSession() as session:
                # Get QR code details
                async with session.get(f"{self.api_url}/organizations/{org_id}/qr-codes/{qr_id}") as resp:
                    if resp.status != 200:
                        raise Exception(f"Failed to get QR code: {await resp.text()}")
                    qr_code = await resp.json()
                    
                # Create keyboard with QR code options
                keyboard = InlineKeyboardMarkup(
                    inline_keyboard=[
                        [InlineKeyboardButton(text="🗑 Удалить", callback_data=f"delete_qr_{org_id}_{qr_id}")],
                        [InlineKeyboardButton(text="◀️ Назад к QR-кодам", callback_data=f"show_qr_codes_{org_id}")]
                    ]
                )
                
                await callback_query.message.answer_photo(
                    photo=f"{self.gen_url}/qr-codes/{qr_code['file_path']}",
                    caption=f"🔲 QR-код #{qr_id}\nСоздан: {qr_code['created_at']}",
                    reply_markup=keyboard
                )
                
        except Exception as e:
            self.logger.error(f"Error showing QR code: {str(e)}")
            await callback_query.message.answer(
                "❌ Произошла ошибка при загрузке QR-кода. Пожалуйста, попробуйте позже."
            )
            
    async def handle_delete_qr(self, callback_query: CallbackQuery):
        """Delete QR code"""
        _, _, org_id, qr_id = callback_query.data.split("_")
        org_id = int(org_id)
        qr_id = int(qr_id)
        
        try:
            async with aiohttp.ClientSession() as session:
                # Delete QR code
                async with session.delete(f"{self.api_url}/organizations/{org_id}/qr-codes/{qr_id}") as resp:
                    if resp.status != 200:
                        raise Exception(f"Failed to delete QR code: {await resp.text()}")
                        
                await callback_query.message.answer(
                    "✅ QR-код успешно удален!",
                    reply_markup=get_back_to_org_buttons(org_id)
                )
                
        except Exception as e:
            self.logger.error(f"Error deleting QR code: {str(e)}")
            await callback_query.message.answer(
                "❌ Произошла ошибка при удалении QR-кода. Пожалуйста, попробуйте позже."
            )

    async def handle_qr_callback(self, callback: CallbackQuery) -> None:
        """Handle QR code-related callback queries"""
        try:
            # Parse callback data
            data = callback.data.split("_")
            if len(data) < 3:
                await callback.answer("Неверный формат данных")
                return

            action = data[1]
            qr_type = data[2]

            # Validate QR code type
            try:
                qr_type = QRCodeType(qr_type)
            except ValueError:
                await callback.answer("Неверный тип QR-кода")
                return

            if action == "delete":
                success = await self.qr_code_use_case.delete_qr_code(
                    organization_id=callback.from_user.id,
                    qr_type=qr_type
                )
                if success:
                    await callback.message.edit_text("QR-код успешно удален")
                else:
                    await callback.message.edit_text("QR-код не найден")

            elif action == "get":
                qr_code = await self.qr_code_use_case.get_qr_code(
                    organization_id=callback.from_user.id,
                    qr_type=qr_type
                )
                if qr_code:
                    await callback.message.answer_photo(
                        photo=qr_code.file_path,
                        caption=f"Тип: {qr_code.qr_type.value}\nСоздан: {qr_code.created_at}"
                    )
                else:
                    await callback.message.edit_text("QR-код не найден")

        except DomainException as e:
            await self._handle_callback_domain_exception(callback, e)
        except Exception as e:
            await callback.answer("Произошла ошибка при обработке запроса") 