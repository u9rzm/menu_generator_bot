from typing import Optional, Dict, Any, List
from app.bot.infrastructure.config.config import settings
from app.bot.infrastructure.exceptions.handler_exceptions import OrganizationError

def get_organization_url(org_id: int) -> str:
    """Get organization URL"""
    return f"{settings.NGINX_URL}/organizations/{org_id}"

def get_organization_logo_url(org_id: int) -> str:
    """Get organization logo URL"""
    return f"{settings.NGINX_URL}/organizations/{org_id}/logo.jpg"

def get_organization_background_url(org_id: int) -> str:
    """Get organization background URL"""
    return f"{settings.NGINX_URL}/organizations/{org_id}/background.jpg"

def get_organization_config(org_id: int) -> Dict[str, Any]:
    """Get organization configuration"""
    try:
        # Here you would typically load the organization configuration from a file or database
        # For now, we'll return a default configuration
        return {
            "org_id": org_id,
            "name": f"Organization {org_id}",
            "description": f"Description for organization {org_id}",
            "url": get_organization_url(org_id),
            "logo_url": get_organization_logo_url(org_id),
            "background_url": get_organization_background_url(org_id),
            "contact": {
                "phone": "+1234567890",
                "email": f"org{org_id}@example.com",
                "address": "123 Main St, City, Country"
            },
            "social": {
                "facebook": f"https://facebook.com/org{org_id}",
                "twitter": f"https://twitter.com/org{org_id}",
                "instagram": f"https://instagram.com/org{org_id}"
            },
            "hours": {
                "monday": "9:00 AM - 10:00 PM",
                "tuesday": "9:00 AM - 10:00 PM",
                "wednesday": "9:00 AM - 10:00 PM",
                "thursday": "9:00 AM - 10:00 PM",
                "friday": "9:00 AM - 11:00 PM",
                "saturday": "10:00 AM - 11:00 PM",
                "sunday": "10:00 AM - 10:00 PM"
            },
            "settings": {
                "theme_id": settings.DEFAULT_THEME,
                "language": "en",
                "currency": "USD",
                "timezone": "UTC"
            }
        }
    except Exception as e:
        raise OrganizationError(f"Failed to get organization configuration: {str(e)}")

def validate_organization_name(name: str) -> bool:
    """Validate organization name"""
    if not name:
        return False
    if len(name) < 2:
        return False
    if len(name) > 100:
        return False
    return True

def validate_organization_description(description: str) -> bool:
    """Validate organization description"""
    if not description:
        return False
    if len(description) < 10:
        return False
    if len(description) > 500:
        return False
    return True

def validate_organization_contact(contact: Dict[str, str]) -> bool:
    """Validate organization contact information"""
    if not contact:
        return False
    required_contact = ["phone", "email", "address"]
    for field in required_contact:
        if field not in contact:
            return False
        if not contact[field]:
            return False
    return True

def validate_organization_social(social: Dict[str, str]) -> bool:
    """Validate organization social links"""
    if not social:
        return False
    required_social = ["facebook", "twitter", "instagram"]
    for platform in required_social:
        if platform not in social:
            return False
        if not social[platform]:
            return False
    return True

def validate_organization_hours(hours: Dict[str, str]) -> bool:
    """Validate organization hours"""
    if not hours:
        return False
    required_days = [
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday",
        "saturday",
        "sunday"
    ]
    for day in required_days:
        if day not in hours:
            return False
        if not hours[day]:
            return False
    return True

def validate_organization_settings(settings: Dict[str, Any]) -> bool:
    """Validate organization settings"""
    if not settings:
        return False
    required_settings = ["theme_id", "language", "currency", "timezone"]
    for setting in required_settings:
        if setting not in settings:
            return False
        if not settings[setting]:
            return False
    return True

def get_organization_mobile_url(org_id: int) -> str:
    """Get organization mobile URL"""
    return f"{settings.NGINX_URL}/organizations/{org_id}/mobile.html"

def get_organization_desktop_url(org_id: int) -> str:
    """Get organization desktop URL"""
    return f"{settings.NGINX_URL}/organizations/{org_id}/desktop.html"

def get_organization_print_url(org_id: int) -> str:
    """Get organization print URL"""
    return f"{settings.NGINX_URL}/organizations/{org_id}/print.html"

def get_organization_share_url(org_id: int) -> str:
    """Get organization share URL"""
    return f"{settings.NGINX_URL}/organizations/{org_id}/share.html"

def get_organization_analytics_url(org_id: int) -> str:
    """Get organization analytics URL"""
    return f"{settings.NGINX_URL}/organizations/{org_id}/analytics.html"

def get_organization_settings_url(org_id: int) -> str:
    """Get organization settings URL"""
    return f"{settings.NGINX_URL}/organizations/{org_id}/settings.html"

def get_organization_help_url(org_id: int) -> str:
    """Get organization help URL"""
    return f"{settings.NGINX_URL}/organizations/{org_id}/help.html" 