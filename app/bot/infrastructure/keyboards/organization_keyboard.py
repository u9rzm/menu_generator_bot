from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_back_to_org_buttons(org_id: int) -> InlineKeyboardMarkup:
    """Get back to organization buttons"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="◀️ Назад к организации", callback_data=f"org_actions_{org_id}")]
        ]
    )

def get_org_actions_keyboard(org_id: int) -> InlineKeyboardMarkup:
    """Get organization actions keyboard"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📋 Меню", callback_data=f"show_menu_{org_id}")],
            [InlineKeyboardButton(text="📸 Изображения", callback_data=f"show_images_{org_id}")],
            [InlineKeyboardButton(text="🔲 QR-коды", callback_data=f"show_qr_codes_{org_id}")],
            [InlineKeyboardButton(text="🎨 Тема", callback_data=f"show_themes_{org_id}")],
            [InlineKeyboardButton(text="🌐 Веб-страница", callback_data=f"generate_web_{org_id}")],
            [InlineKeyboardButton(text="◀️ Назад к списку", callback_data="my_organizations")]
        ]
    )

def get_menu_upload_keyboard(org_id: int) -> InlineKeyboardMarkup:
    """Get menu upload keyboard"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📤 Загрузить CSV", callback_data=f"upload_menu_file_{org_id}")],
            [InlineKeyboardButton(text="📊 Google Sheets", callback_data=f"upload_menu_sheets_{org_id}")],
            [InlineKeyboardButton(text="◀️ Назад", callback_data=f"org_actions_{org_id}")]
        ]
    )

def get_image_upload_keyboard(org_id: int) -> InlineKeyboardMarkup:
    """Get image upload keyboard"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📤 Загрузить логотип", callback_data=f"upload_image_{org_id}_logo")],
            [InlineKeyboardButton(text="📤 Загрузить фон", callback_data=f"upload_image_{org_id}_background")],
            [InlineKeyboardButton(text="📤 Загрузить фото", callback_data=f"upload_image_{org_id}_photo")],
            [InlineKeyboardButton(text="◀️ Назад", callback_data=f"org_actions_{org_id}")]
        ]
    )

def get_qr_code_keyboard(org_id: int) -> InlineKeyboardMarkup:
    """Get QR code keyboard"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔲 Сгенерировать QR-код", callback_data=f"generate_qr_{org_id}")],
            [InlineKeyboardButton(text="📋 Список QR-кодов", callback_data=f"show_qr_codes_{org_id}")],
            [InlineKeyboardButton(text="◀️ Назад", callback_data=f"org_actions_{org_id}")]
        ]
    )

def get_theme_keyboard(org_id: int) -> InlineKeyboardMarkup:
    """Get theme keyboard"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🎨 Выбрать тему", callback_data=f"show_themes_{org_id}")],
            [InlineKeyboardButton(text="◀️ Назад", callback_data=f"org_actions_{org_id}")]
        ]
    )

def get_web_page_keyboard(org_id: int) -> InlineKeyboardMarkup:
    """Get web page keyboard"""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🌐 Сгенерировать", callback_data=f"generate_web_{org_id}")],
            [InlineKeyboardButton(text="🔗 Получить ссылку", callback_data=f"get_web_link_{org_id}")],
            [InlineKeyboardButton(text="◀️ Назад", callback_data=f"org_actions_{org_id}")]
        ]
    ) 