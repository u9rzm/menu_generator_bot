from typing import Optional, Dict, Any
from app.bot.infrastructure.exceptions.handler_exceptions import (
    HandlerError,
    APIError,
    ValidationError,
    FileError,
    StateError,
    ThemeError,
    QRCodeError,
    WebPageError,
    MenuError,
    ImageError,
    OrganizationError,
    UserError
)

def get_error_message(error: Exception) -> str:
    """Get error message"""
    if isinstance(error, HandlerError):
        return str(error)
    elif isinstance(error, APIError):
        return f"API error: {str(error)}"
    elif isinstance(error, ValidationError):
        return f"Validation error: {str(error)}"
    elif isinstance(error, FileError):
        return f"File error: {str(error)}"
    elif isinstance(error, StateError):
        return f"State error: {str(error)}"
    elif isinstance(error, ThemeError):
        return f"Theme error: {str(error)}"
    elif isinstance(error, QRCodeError):
        return f"QR code error: {str(error)}"
    elif isinstance(error, WebPageError):
        return f"Web page error: {str(error)}"
    elif isinstance(error, MenuError):
        return f"Menu error: {str(error)}"
    elif isinstance(error, ImageError):
        return f"Image error: {str(error)}"
    elif isinstance(error, OrganizationError):
        return f"Organization error: {str(error)}"
    elif isinstance(error, UserError):
        return f"User error: {str(error)}"
    else:
        return f"Unknown error: {str(error)}"

def get_error_code(error: Exception) -> str:
    """Get error code"""
    if isinstance(error, HandlerError):
        return "HANDLER_ERROR"
    elif isinstance(error, APIError):
        return "API_ERROR"
    elif isinstance(error, ValidationError):
        return "VALIDATION_ERROR"
    elif isinstance(error, FileError):
        return "FILE_ERROR"
    elif isinstance(error, StateError):
        return "STATE_ERROR"
    elif isinstance(error, ThemeError):
        return "THEME_ERROR"
    elif isinstance(error, QRCodeError):
        return "QR_CODE_ERROR"
    elif isinstance(error, WebPageError):
        return "WEB_PAGE_ERROR"
    elif isinstance(error, MenuError):
        return "MENU_ERROR"
    elif isinstance(error, ImageError):
        return "IMAGE_ERROR"
    elif isinstance(error, OrganizationError):
        return "ORGANIZATION_ERROR"
    elif isinstance(error, UserError):
        return "USER_ERROR"
    else:
        return "UNKNOWN_ERROR"

def get_error_details(error: Exception) -> Dict[str, Any]:
    """Get error details"""
    return {
        "code": get_error_code(error),
        "message": get_error_message(error),
        "type": type(error).__name__,
        "args": error.args
    }

def is_validation_error(error: Exception) -> bool:
    """Check if error is a validation error"""
    return isinstance(error, ValidationError)

def is_api_error(error: Exception) -> bool:
    """Check if error is an API error"""
    return isinstance(error, APIError)

def is_file_error(error: Exception) -> bool:
    """Check if error is a file error"""
    return isinstance(error, FileError)

def is_state_error(error: Exception) -> bool:
    """Check if error is a state error"""
    return isinstance(error, StateError)

def is_theme_error(error: Exception) -> bool:
    """Check if error is a theme error"""
    return isinstance(error, ThemeError)

def is_qr_code_error(error: Exception) -> bool:
    """Check if error is a QR code error"""
    return isinstance(error, QRCodeError)

def is_web_page_error(error: Exception) -> bool:
    """Check if error is a web page error"""
    return isinstance(error, WebPageError)

def is_menu_error(error: Exception) -> bool:
    """Check if error is a menu error"""
    return isinstance(error, MenuError)

def is_image_error(error: Exception) -> bool:
    """Check if error is an image error"""
    return isinstance(error, ImageError)

def is_organization_error(error: Exception) -> bool:
    """Check if error is an organization error"""
    return isinstance(error, OrganizationError)

def is_user_error(error: Exception) -> bool:
    """Check if error is a user error"""
    return isinstance(error, UserError)

def is_handler_error(error: Exception) -> bool:
    """Check if error is a handler error"""
    return isinstance(error, HandlerError)

def is_unknown_error(error: Exception) -> bool:
    """Check if error is an unknown error"""
    return not any([
        is_validation_error(error),
        is_api_error(error),
        is_file_error(error),
        is_state_error(error),
        is_theme_error(error),
        is_qr_code_error(error),
        is_web_page_error(error),
        is_menu_error(error),
        is_image_error(error),
        is_organization_error(error),
        is_user_error(error),
        is_handler_error(error)
    ]) 