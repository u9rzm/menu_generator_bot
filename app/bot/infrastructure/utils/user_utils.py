from typing import Optional, Dict, Any, List
from app.bot.infrastructure.config.config import settings
from app.bot.infrastructure.exceptions.handler_exceptions import UserError

def get_user_url(user_id: int) -> str:
    """Get user URL"""
    return f"{settings.NGINX_URL}/users/{user_id}"

def get_user_avatar_url(user_id: int) -> str:
    """Get user avatar URL"""
    return f"{settings.NGINX_URL}/users/{user_id}/avatar.jpg"

def get_user_config(user_id: int) -> Dict[str, Any]:
    """Get user configuration"""
    try:
        # Here you would typically load the user configuration from a file or database
        # For now, we'll return a default configuration
        return {
            "user_id": user_id,
            "username": f"user{user_id}",
            "first_name": "John",
            "last_name": "Doe",
            "language_code": "en",
            "url": get_user_url(user_id),
            "avatar_url": get_user_avatar_url(user_id),
            "settings": {
                "language": "en",
                "timezone": "UTC",
                "notifications": True,
                "theme": "light"
            },
            "organizations": [
                {
                    "org_id": 1,
                    "name": "Organization 1",
                    "role": "owner"
                },
                {
                    "org_id": 2,
                    "name": "Organization 2",
                    "role": "admin"
                }
            ]
        }
    except Exception as e:
        raise UserError(f"Failed to get user configuration: {str(e)}")

def validate_username(username: str) -> bool:
    """Validate username"""
    if not username:
        return False
    if len(username) < 3:
        return False
    if len(username) > 32:
        return False
    return True

def validate_first_name(first_name: str) -> bool:
    """Validate first name"""
    if not first_name:
        return False
    if len(first_name) < 2:
        return False
    if len(first_name) > 64:
        return False
    return True

def validate_last_name(last_name: str) -> bool:
    """Validate last name"""
    if not last_name:
        return False
    if len(last_name) < 2:
        return False
    if len(last_name) > 64:
        return False
    return True

def validate_language_code(language_code: str) -> bool:
    """Validate language code"""
    if not language_code:
        return False
    if len(language_code) != 2:
        return False
    return True

def validate_user_settings(settings: Dict[str, Any]) -> bool:
    """Validate user settings"""
    if not settings:
        return False
    required_settings = ["language", "timezone", "notifications", "theme"]
    for setting in required_settings:
        if setting not in settings:
            return False
        if not settings[setting]:
            return False
    return True

def validate_user_organizations(organizations: List[Dict[str, Any]]) -> bool:
    """Validate user organizations"""
    if not organizations:
        return False
    for org in organizations:
        if not validate_organization_name(org["name"]):
            return False
        if not validate_organization_role(org["role"]):
            return False
    return True

def validate_organization_role(role: str) -> bool:
    """Validate organization role"""
    if not role:
        return False
    valid_roles = ["owner", "admin", "member"]
    return role in valid_roles

def get_user_mobile_url(user_id: int) -> str:
    """Get user mobile URL"""
    return f"{settings.NGINX_URL}/users/{user_id}/mobile.html"

def get_user_desktop_url(user_id: int) -> str:
    """Get user desktop URL"""
    return f"{settings.NGINX_URL}/users/{user_id}/desktop.html"

def get_user_print_url(user_id: int) -> str:
    """Get user print URL"""
    return f"{settings.NGINX_URL}/users/{user_id}/print.html"

def get_user_share_url(user_id: int) -> str:
    """Get user share URL"""
    return f"{settings.NGINX_URL}/users/{user_id}/share.html"

def get_user_analytics_url(user_id: int) -> str:
    """Get user analytics URL"""
    return f"{settings.NGINX_URL}/users/{user_id}/analytics.html"

def get_user_settings_url(user_id: int) -> str:
    """Get user settings URL"""
    return f"{settings.NGINX_URL}/users/{user_id}/settings.html"

def get_user_help_url(user_id: int) -> str:
    """Get user help URL"""
    return f"{settings.NGINX_URL}/users/{user_id}/help.html" 