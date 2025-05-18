import logging
from aiogram.types import Message

logger = logging.getLogger(__name__)

def log_user_info(message: Message):
    user = message.from_user
    chat = message.chat
    logger.info(
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
