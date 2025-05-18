from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_main_buttons():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📝 Создать организацию", callback_data="create_org")],
            [InlineKeyboardButton(text="🏢 Мои организации", callback_data="my_organizations")],
            [InlineKeyboardButton(text="❓ Помощь", callback_data="help")]
        ]
    )
