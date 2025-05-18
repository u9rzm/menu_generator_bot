from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from keyboards.main import get_main_buttons
from services.user_service import register_user
from utils.logging import log_user_info

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    log_user_info(message)
    success = await register_user(message.from_user.id)
    if success:
        await message.answer("👋 Добро пожаловать!", reply_markup=get_main_buttons())
    else:
        await message.answer("❌ Ошибка при регистрации. Попробуйте позже.")
