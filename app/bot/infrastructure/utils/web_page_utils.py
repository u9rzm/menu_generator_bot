from typing import Optional, Dict, Any
from app.bot.infrastructure.config.config import settings
from app.bot.infrastructure.exceptions.handler_exceptions import WebPageError

def get_web_page_url(org_id: int) -> str:
    """Get web page URL"""
    return f"{settings.NGINX_URL}/web-pages/{org_id}/index.html"

def get_web_page_preview_url(org_id: int) -> str:
    """Get web page preview URL"""
    return f"{settings.NGINX_URL}/web-pages/{org_id}/preview.jpg"

def get_web_page_css_url(org_id: int) -> str:
    """Get web page CSS URL"""
    return f"{settings.NGINX_URL}/web-pages/{org_id}/style.css"

def get_web_page_js_url(org_id: int) -> str:
    """Get web page JavaScript URL"""
    return f"{settings.NGINX_URL}/web-pages/{org_id}/script.js"

def get_web_page_assets_url(org_id: int) -> str:
    """Get web page assets URL"""
    return f"{settings.NGINX_URL}/web-pages/{org_id}/assets"

def get_web_page_config(org_id: int) -> Dict[str, Any]:
    """Get web page configuration"""
    try:
        # Here you would typically load the web page configuration from a file or database
        # For now, we'll return a default configuration
        return {
            "org_id": org_id,
            "title": settings.WEB_PAGE_TITLE,
            "description": settings.WEB_PAGE_DESCRIPTION,
            "url": get_web_page_url(org_id),
            "preview_url": get_web_page_preview_url(org_id),
            "css_url": get_web_page_css_url(org_id),
            "js_url": get_web_page_js_url(org_id),
            "assets_url": get_web_page_assets_url(org_id),
            "meta": {
                "viewport": "width=device-width, initial-scale=1.0",
                "description": settings.WEB_PAGE_DESCRIPTION,
                "keywords": "restaurant, menu, food, drinks",
                "author": "Restaurant Bot",
                "robots": "index, follow"
            },
            "social": {
                "facebook": f"https://facebook.com/restaurant{org_id}",
                "twitter": f"https://twitter.com/restaurant{org_id}",
                "instagram": f"https://instagram.com/restaurant{org_id}"
            },
            "contact": {
                "phone": "+1234567890",
                "email": f"restaurant{org_id}@example.com",
                "address": "123 Main St, City, Country"
            },
            "hours": {
                "monday": "9:00 AM - 10:00 PM",
                "tuesday": "9:00 AM - 10:00 PM",
                "wednesday": "9:00 AM - 10:00 PM",
                "thursday": "9:00 AM - 10:00 PM",
                "friday": "9:00 AM - 11:00 PM",
                "saturday": "10:00 AM - 11:00 PM",
                "sunday": "10:00 AM - 10:00 PM"
            }
        }
    except Exception as e:
        raise WebPageError(f"Failed to get web page configuration: {str(e)}")

def validate_web_page_title(title: str) -> bool:
    """Validate web page title"""
    if not title:
        return False
    if len(title) < 2:
        return False
    if len(title) > 100:
        return False
    return True

def validate_web_page_description(description: str) -> bool:
    """Validate web page description"""
    if not description:
        return False
    if len(description) < 10:
        return False
    if len(description) > 500:
        return False
    return True

def validate_web_page_meta(meta: Dict[str, str]) -> bool:
    """Validate web page meta tags"""
    if not meta:
        return False
    required_meta = [
        "viewport",
        "description",
        "keywords",
        "author",
        "robots"
    ]
    for tag in required_meta:
        if tag not in meta:
            return False
        if not meta[tag]:
            return False
    return True

def validate_web_page_social(social: Dict[str, str]) -> bool:
    """Validate web page social links"""
    if not social:
        return False
    required_social = ["facebook", "twitter", "instagram"]
    for platform in required_social:
        if platform not in social:
            return False
        if not social[platform]:
            return False
    return True

def validate_web_page_contact(contact: Dict[str, str]) -> bool:
    """Validate web page contact information"""
    if not contact:
        return False
    required_contact = ["phone", "email", "address"]
    for field in required_contact:
        if field not in contact:
            return False
        if not contact[field]:
            return False
    return True

def validate_web_page_hours(hours: Dict[str, str]) -> bool:
    """Validate web page hours"""
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

def get_web_page_mobile_url(org_id: int) -> str:
    """Get web page mobile URL"""
    return f"{settings.NGINX_URL}/web-pages/{org_id}/mobile.html"

def get_web_page_desktop_url(org_id: int) -> str:
    """Get web page desktop URL"""
    return f"{settings.NGINX_URL}/web-pages/{org_id}/desktop.html"

def get_web_page_print_url(org_id: int) -> str:
    """Get web page print URL"""
    return f"{settings.NGINX_URL}/web-pages/{org_id}/print.html"

def get_web_page_share_url(org_id: int) -> str:
    """Get web page share URL"""
    return f"{settings.NGINX_URL}/web-pages/{org_id}/share.html"

def get_web_page_analytics_url(org_id: int) -> str:
    """Get web page analytics URL"""
    return f"{settings.NGINX_URL}/web-pages/{org_id}/analytics.html"

def get_web_page_settings_url(org_id: int) -> str:
    """Get web page settings URL"""
    return f"{settings.NGINX_URL}/web-pages/{org_id}/settings.html"

def get_web_page_help_url(org_id: int) -> str:
    """Get web page help URL"""
    return f"{settings.NGINX_URL}/web-pages/{org_id}/help.html" 