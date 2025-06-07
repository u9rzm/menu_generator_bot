from typing import Optional, Union, Dict, Any, List
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
    ParseMode
)
from app.bot.infrastructure.utils.logging_utils import log_user_action
from app.bot.infrastructure.exceptions.handler_exceptions import ValidationError

def create_inline_keyboard(buttons: List[List[Dict[str, Any]]]) -> InlineKeyboardMarkup:
    """Create inline keyboard"""
    keyboard = []
    for row in buttons:
        keyboard_row = []
        for button in row:
            keyboard_row.append(
                InlineKeyboardButton(
                    text=button.get("text", ""),
                    callback_data=button.get("callback_data", ""),
                    url=button.get("url"),
                    login_url=button.get("login_url"),
                    switch_inline_query=button.get("switch_inline_query"),
                    switch_inline_query_current_chat=button.get("switch_inline_query_current_chat"),
                    callback_game=button.get("callback_game"),
                    pay=button.get("pay", False)
                )
            )
        keyboard.append(keyboard_row)
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def create_reply_keyboard(
    buttons: List[List[Dict[str, Any]]],
    resize_keyboard: bool = True,
    one_time_keyboard: bool = False,
    selective: bool = False
) -> ReplyKeyboardMarkup:
    """Create reply keyboard"""
    keyboard = []
    for row in buttons:
        keyboard_row = []
        for button in row:
            keyboard_row.append(
                KeyboardButton(
                    text=button.get("text", ""),
                    request_contact=button.get("request_contact", False),
                    request_location=button.get("request_location", False),
                    request_poll=button.get("request_poll")
                )
            )
        keyboard.append(keyboard_row)
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=resize_keyboard,
        one_time_keyboard=one_time_keyboard,
        selective=selective
    )

def get_callback_data(callback_query: CallbackQuery) -> dict[str, str]:
    """Parse callback data"""
    try:
        action, *params = callback_query.data.split(":")
        return {
            "action": action,
            "params": params
        }
    except Exception as e:
        raise ValidationError(f"Failed to parse callback data: {str(e)}")

def get_message_text(message: Union[Message, CallbackQuery]) -> Optional[str]:
    """Get message text"""
    if isinstance(message, Message):
        return message.text
    elif isinstance(message, CallbackQuery):
        return message.data
    return None

def get_message_chat_id(message: Union[Message, CallbackQuery]) -> Optional[int]:
    """Get message chat ID"""
    if isinstance(message, Message):
        return message.chat.id
    elif isinstance(message, CallbackQuery):
        return message.message.chat.id
    return None

def get_message_user_id(message: Union[Message, CallbackQuery]) -> Optional[int]:
    """Get message user ID"""
    if isinstance(message, Message):
        return message.from_user.id
    elif isinstance(message, CallbackQuery):
        return message.from_user.id
    return None

def get_message_username(message: Union[Message, CallbackQuery]) -> Optional[str]:
    """Get message username"""
    if isinstance(message, Message):
        return message.from_user.username
    elif isinstance(message, CallbackQuery):
        return message.from_user.username
    return None

def get_message_first_name(message: Union[Message, CallbackQuery]) -> Optional[str]:
    """Get message first name"""
    if isinstance(message, Message):
        return message.from_user.first_name
    elif isinstance(message, CallbackQuery):
        return message.from_user.first_name
    return None

def get_message_last_name(message: Union[Message, CallbackQuery]) -> Optional[str]:
    """Get message last name"""
    if isinstance(message, Message):
        return message.from_user.last_name
    elif isinstance(message, CallbackQuery):
        return message.from_user.last_name
    return None

def get_message_language_code(message: Union[Message, CallbackQuery]) -> Optional[str]:
    """Get message language code"""
    if isinstance(message, Message):
        return message.from_user.language_code
    elif isinstance(message, CallbackQuery):
        return message.from_user.language_code
    return None

def get_message_chat_type(message: Union[Message, CallbackQuery]) -> Optional[str]:
    """Get message chat type"""
    if isinstance(message, Message):
        return message.chat.type
    elif isinstance(message, CallbackQuery):
        return message.message.chat.type
    return None

def get_message_date(message: Union[Message, CallbackQuery]) -> Optional[int]:
    """Get message date"""
    if isinstance(message, Message):
        return message.date
    elif isinstance(message, CallbackQuery):
        return message.message.date
    return None

def get_message_id(message: Union[Message, CallbackQuery]) -> Optional[int]:
    """Get message ID"""
    if isinstance(message, Message):
        return message.message_id
    elif isinstance(message, CallbackQuery):
        return message.message.message_id
    return None

def get_message_reply_to_message(message: Message) -> Optional[Message]:
    """Get message reply to message"""
    return message.reply_to_message

def get_message_forward_from(message: Message) -> Optional[Dict[str, Any]]:
    """Get message forward from"""
    return message.forward_from

def get_message_forward_from_chat(message: Message) -> Optional[Dict[str, Any]]:
    """Get message forward from chat"""
    return message.forward_from_chat

def get_message_forward_date(message: Message) -> Optional[int]:
    """Get message forward date"""
    return message.forward_date

def get_message_edit_date(message: Message) -> Optional[int]:
    """Get message edit date"""
    return message.edit_date

def get_message_media_group_id(message: Message) -> Optional[str]:
    """Get message media group ID"""
    return message.media_group_id

def get_message_author_signature(message: Message) -> Optional[str]:
    """Get message author signature"""
    return message.author_signature

def get_message_text_entities(message: Message) -> Optional[List[Dict[str, Any]]]:
    """Get message text entities"""
    return message.entities

def get_message_caption_entities(message: Message) -> Optional[List[Dict[str, Any]]]:
    """Get message caption entities"""
    return message.caption_entities

def get_message_audio(message: Message) -> Optional[Dict[str, Any]]:
    """Get message audio"""
    return message.audio

def get_message_document(message: Message) -> Optional[Dict[str, Any]]:
    """Get message document"""
    return message.document

def get_message_animation(message: Message) -> Optional[Dict[str, Any]]:
    """Get message animation"""
    return message.animation

def get_message_photo(message: Message) -> Optional[List[Dict[str, Any]]]:
    """Get message photo"""
    return message.photo

def get_message_sticker(message: Message) -> Optional[Dict[str, Any]]:
    """Get message sticker"""
    return message.sticker

def get_message_video(message: Message) -> Optional[Dict[str, Any]]:
    """Get message video"""
    return message.video

def get_message_video_note(message: Message) -> Optional[Dict[str, Any]]:
    """Get message video note"""
    return message.video_note

def get_message_voice(message: Message) -> Optional[Dict[str, Any]]:
    """Get message voice"""
    return message.voice

def get_message_caption(message: Message) -> Optional[str]:
    """Get message caption"""
    return message.caption

def get_message_contact(message: Message) -> Optional[Dict[str, Any]]:
    """Get message contact"""
    return message.contact

def get_message_dice(message: Message) -> Optional[Dict[str, Any]]:
    """Get message dice"""
    return message.dice

def get_message_game(message: Message) -> Optional[Dict[str, Any]]:
    """Get message game"""
    return message.game

def get_message_poll(message: Message) -> Optional[Dict[str, Any]]:
    """Get message poll"""
    return message.poll

def get_message_venue(message: Message) -> Optional[Dict[str, Any]]:
    """Get message venue"""
    return message.venue

def get_message_location(message: Message) -> Optional[Dict[str, Any]]:
    """Get message location"""
    return message.location

def get_message_invoice(message: Message) -> Optional[Dict[str, Any]]:
    """Get message invoice"""
    return message.invoice

def get_message_successful_payment(message: Message) -> Optional[Dict[str, Any]]:
    """Get message successful payment"""
    return message.successful_payment

def get_message_connected_website(message: Message) -> Optional[str]:
    """Get message connected website"""
    return message.connected_website

def get_message_passport_data(message: Message) -> Optional[Dict[str, Any]]:
    """Get message passport data"""
    return message.passport_data

def get_message_proximity_alert_triggered(message: Message) -> Optional[Dict[str, Any]]:
    """Get message proximity alert triggered"""
    return message.proximity_alert_triggered

def get_message_voice_chat_scheduled(message: Message) -> Optional[Dict[str, Any]]:
    """Get message voice chat scheduled"""
    return message.voice_chat_scheduled

def get_message_voice_chat_started(message: Message) -> Optional[Dict[str, Any]]:
    """Get message voice chat started"""
    return message.voice_chat_started

def get_message_voice_chat_ended(message: Message) -> Optional[Dict[str, Any]]:
    """Get message voice chat ended"""
    return message.voice_chat_ended

def get_message_voice_chat_participants_invited(message: Message) -> Optional[Dict[str, Any]]:
    """Get message voice chat participants invited"""
    return message.voice_chat_participants_invited

def get_message_reply_markup(message: Message) -> Optional[Union[InlineKeyboardMarkup, ReplyKeyboardMarkup]]:
    """Get message reply markup"""
    return message.reply_markup

def get_file_id(message: Message) -> str:
    """Get file ID from message"""
    if message.photo:
        return message.photo[-1].file_id
    elif message.document:
        return message.document.file_id
    else:
        raise ValidationError("Message has no file")

def get_file_name(message: Message) -> str:
    """Get file name from message"""
    if message.document:
        return message.document.file_name
    else:
        raise ValidationError("Message has no file name")

def get_file_size(message: Message) -> int:
    """Get file size from message"""
    if message.document:
        return message.document.file_size
    elif message.photo:
        return message.photo[-1].file_size
    else:
        raise ValidationError("Message has no file size")

def get_file_type(message: Message) -> str:
    """Get file type from message"""
    if message.photo:
        return "photo"
    elif message.document:
        return "document"
    else:
        raise ValidationError("Message has no file type")

def get_user_id(message: Union[Message, CallbackQuery]) -> int:
    """Get user ID from message or callback query"""
    if isinstance(message, Message):
        return message.from_user.id
    else:
        return message.from_user.id

def get_chat_id(message: Union[Message, CallbackQuery]) -> int:
    """Get chat ID from message or callback query"""
    if isinstance(message, Message):
        return message.chat.id
    else:
        return message.message.chat.id

def get_username(message: Union[Message, CallbackQuery]) -> Optional[str]:
    """Get username from message or callback query"""
    if isinstance(message, Message):
        return message.from_user.username
    else:
        return message.from_user.username

def get_first_name(message: Union[Message, CallbackQuery]) -> str:
    """Get first name from message or callback query"""
    if isinstance(message, Message):
        return message.from_user.first_name
    else:
        return message.from_user.first_name

def get_last_name(message: Union[Message, CallbackQuery]) -> Optional[str]:
    """Get last name from message or callback query"""
    if isinstance(message, Message):
        return message.from_user.last_name
    else:
        return message.from_user.last_name

def get_language_code(message: Union[Message, CallbackQuery]) -> str:
    """Get language code from message or callback query"""
    if isinstance(message, Message):
        return message.from_user.language_code
    else:
        return message.from_user.language_code

def validate_message_text(text: str, min_length: int = 1, max_length: int = 4096) -> bool:
    """Validate message text"""
    if not text:
        return False
    if len(text) < min_length:
        return False
    if len(text) > max_length:
        return False
    return True

def ensure_message_text(text: str, min_length: int = 1, max_length: int = 4096) -> None:
    """Ensure message text"""
    if not validate_message_text(text, min_length, max_length):
        raise ValidationError(
            f"Message text must be between {min_length} and {max_length} characters"
        )

def validate_callback_data(data: str, max_length: int = 64) -> bool:
    """Validate callback data"""
    if not data:
        return False
    if len(data) > max_length:
        return False
    return True

def ensure_callback_data(data: str, max_length: int = 64) -> None:
    """Ensure callback data"""
    if not validate_callback_data(data, max_length):
        raise ValidationError(
            f"Callback data must not exceed {max_length} characters"
        )

def validate_inline_keyboard(buttons: List[List[Dict[str, Any]]]) -> bool:
    """Validate inline keyboard"""
    if not buttons:
        return False
    for row in buttons:
        if not row:
            return False
        for button in row:
            if not button.get("text"):
                return False
            if not button.get("callback_data") and not button.get("url"):
                return False
    return True

def ensure_inline_keyboard(buttons: List[List[Dict[str, Any]]]) -> None:
    """Ensure inline keyboard"""
    if not validate_inline_keyboard(buttons):
        raise ValidationError("Invalid inline keyboard")

def validate_reply_keyboard(buttons: List[List[Dict[str, Any]]]) -> bool:
    """Validate reply keyboard"""
    if not buttons:
        return False
    for row in buttons:
        if not row:
            return False
        for button in row:
            if not button.get("text"):
                return False
    return True

def ensure_reply_keyboard(buttons: List[List[Dict[str, Any]]]) -> None:
    """Ensure reply keyboard"""
    if not validate_reply_keyboard(buttons):
        raise ValidationError("Invalid reply keyboard")

def get_parse_mode(text: str) -> Optional[str]:
    """Get parse mode"""
    if "<b>" in text or "</b>" in text:
        return ParseMode.HTML
    if "*" in text or "_" in text:
        return ParseMode.MARKDOWN
    return None

def validate_parse_mode(text: str, parse_mode: Optional[str]) -> bool:
    """Validate parse mode"""
    if not parse_mode:
        return True
    if parse_mode == ParseMode.HTML:
        return "<" in text and ">" in text
    if parse_mode == ParseMode.MARKDOWN:
        return "*" in text or "_" in text
    return False

def ensure_parse_mode(text: str, parse_mode: Optional[str]) -> None:
    """Ensure parse mode"""
    if not validate_parse_mode(text, parse_mode):
        raise ValidationError("Invalid parse mode") 