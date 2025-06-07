from typing import Optional, Dict, Any, List
from app.bot.infrastructure.config.config import settings
from app.bot.infrastructure.exceptions.handler_exceptions import MenuError

def get_menu_url(org_id: int) -> str:
    """Get menu URL"""
    return f"{settings.NGINX_URL}/menus/{org_id}/menu.json"

def get_menu_preview_url(org_id: int) -> str:
    """Get menu preview URL"""
    return f"{settings.NGINX_URL}/menus/{org_id}/preview.jpg"

def get_menu_pdf_url(org_id: int) -> str:
    """Get menu PDF URL"""
    return f"{settings.NGINX_URL}/menus/{org_id}/menu.pdf"

def get_menu_image_url(org_id: int, image_id: int) -> str:
    """Get menu image URL"""
    return f"{settings.NGINX_URL}/menus/{org_id}/images/{image_id}.jpg"

def get_menu_config(org_id: int) -> Dict[str, Any]:
    """Get menu configuration"""
    try:
        # Here you would typically load the menu configuration from a file or database
        # For now, we'll return a default configuration
        return {
            "org_id": org_id,
            "categories": [
                {
                    "id": 1,
                    "name": "Appetizers",
                    "items": [
                        {
                            "id": 1,
                            "name": "Bruschetta",
                            "description": "Toasted bread with tomatoes and herbs",
                            "price": 8.99,
                            "image_id": 1
                        },
                        {
                            "id": 2,
                            "name": "Calamari",
                            "description": "Fried squid with marinara sauce",
                            "price": 12.99,
                            "image_id": 2
                        }
                    ]
                },
                {
                    "id": 2,
                    "name": "Main Courses",
                    "items": [
                        {
                            "id": 3,
                            "name": "Steak",
                            "description": "Grilled beef with vegetables",
                            "price": 24.99,
                            "image_id": 3
                        },
                        {
                            "id": 4,
                            "name": "Salmon",
                            "description": "Baked salmon with rice",
                            "price": 22.99,
                            "image_id": 4
                        }
                    ]
                },
                {
                    "id": 3,
                    "name": "Desserts",
                    "items": [
                        {
                            "id": 5,
                            "name": "Cheesecake",
                            "description": "New York style cheesecake",
                            "price": 7.99,
                            "image_id": 5
                        },
                        {
                            "id": 6,
                            "name": "Tiramisu",
                            "description": "Classic Italian dessert",
                            "price": 8.99,
                            "image_id": 6
                        }
                    ]
                }
            ]
        }
    except Exception as e:
        raise MenuError(f"Failed to get menu configuration: {str(e)}")

def validate_menu_category(category: str) -> bool:
    """Validate menu category"""
    if not category:
        return False
    if len(category) < 2:
        return False
    if len(category) > 50:
        return False
    return True

def validate_menu_item_name(name: str) -> bool:
    """Validate menu item name"""
    if not name:
        return False
    if len(name) < 2:
        return False
    if len(name) > 100:
        return False
    return True

def validate_menu_item_description(description: str) -> bool:
    """Validate menu item description"""
    if not description:
        return False
    if len(description) > 500:
        return False
    return True

def validate_menu_item_price(price: float) -> bool:
    """Validate menu item price"""
    if price <= 0:
        return False
    if price > 1000:
        return False
    return True

def validate_menu_item_image(image_id: int) -> bool:
    """Validate menu item image"""
    if image_id <= 0:
        return False
    return True

def validate_menu_categories(categories: List[Dict[str, Any]]) -> bool:
    """Validate menu categories"""
    if not categories:
        return False
    for category in categories:
        if not validate_menu_category(category["name"]):
            return False
        if not validate_menu_items(category["items"]):
            return False
    return True

def validate_menu_items(items: List[Dict[str, Any]]) -> bool:
    """Validate menu items"""
    if not items:
        return False
    for item in items:
        if not validate_menu_item_name(item["name"]):
            return False
        if not validate_menu_item_description(item["description"]):
            return False
        if not validate_menu_item_price(item["price"]):
            return False
        if not validate_menu_item_image(item["image_id"]):
            return False
    return True

def get_menu_mobile_url(org_id: int) -> str:
    """Get menu mobile URL"""
    return f"{settings.NGINX_URL}/menus/{org_id}/mobile.html"

def get_menu_desktop_url(org_id: int) -> str:
    """Get menu desktop URL"""
    return f"{settings.NGINX_URL}/menus/{org_id}/desktop.html"

def get_menu_print_url(org_id: int) -> str:
    """Get menu print URL"""
    return f"{settings.NGINX_URL}/menus/{org_id}/print.html"

def get_menu_share_url(org_id: int) -> str:
    """Get menu share URL"""
    return f"{settings.NGINX_URL}/menus/{org_id}/share.html"

def get_menu_analytics_url(org_id: int) -> str:
    """Get menu analytics URL"""
    return f"{settings.NGINX_URL}/menus/{org_id}/analytics.html"

def get_menu_settings_url(org_id: int) -> str:
    """Get menu settings URL"""
    return f"{settings.NGINX_URL}/menus/{org_id}/settings.html"

def get_menu_help_url(org_id: int) -> str:
    """Get menu help URL"""
    return f"{settings.NGINX_URL}/menus/{org_id}/help.html" 