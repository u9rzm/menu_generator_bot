from typing import Optional, Dict, Any, List, Union
from app.bot.infrastructure.exceptions.handler_exceptions import ValidationError

def validate_organization_name(name: str) -> bool:
    """Validate organization name"""
    if not name:
        return False
    if len(name) < 3:
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

def validate_menu_item_name(name: str) -> bool:
    """Validate menu item name"""
    if not name:
        return False
    if len(name) < 2:
        return False
    if len(name) > 100:
        return False
    return True

def validate_menu_item_price(price: float) -> bool:
    """Validate menu item price"""
    if not price:
        return False
    if price <= 0:
        return False
    if price > 100000:
        return False
    return True

def validate_menu_item_description(description: Optional[str]) -> bool:
    """Validate menu item description"""
    if description is None:
        return True
    if len(description) > 500:
        return False
    return True

def validate_menu_category(category: str) -> bool:
    """Validate menu category"""
    if not category:
        return False
    if len(category) < 2:
        return False
    if len(category) > 50:
        return False
    return True

def validate_image_type(image_type: str) -> bool:
    """Validate image type"""
    valid_types = ["logo", "background", "photo"]
    return image_type in valid_types

def validate_qr_type(qr_type: str) -> bool:
    """Validate QR type"""
    valid_types = ["menu", "table", "order"]
    return qr_type in valid_types

def validate_qr_content(content: str) -> bool:
    """Validate QR content"""
    if not content:
        return False
    if len(content) > 1000:
        return False
    return True

def validate_theme_name(theme_name: str) -> bool:
    """Validate theme name"""
    if not theme_name:
        return False
    if len(theme_name) < 2:
        return False
    if len(theme_name) > 50:
        return False
    return True

def validate_theme_config(config: Dict[str, Any]) -> bool:
    """Validate theme config"""
    if not config:
        return False
    required_keys = ["colors", "fonts", "spacing"]
    return all(key in config for key in required_keys)

def validate_web_page_title(title: str) -> bool:
    """Validate web page title"""
    if not title:
        return False
    if len(title) < 2:
        return False
    if len(title) > 100:
        return False
    return True

def validate_web_page_content(content: str) -> bool:
    """Validate web page content"""
    if not content:
        return False
    if len(content) < 10:
        return False
    if len(content) > 10000:
        return False
    return True

def validate_web_page_config(config: Dict[str, Any]) -> bool:
    """Validate web page config"""
    if not config:
        return False
    required_keys = ["layout", "style", "meta"]
    return all(key in config for key in required_keys)

def validate_user_id(user_id: int) -> bool:
    """Validate user ID"""
    if not user_id:
        return False
    if user_id <= 0:
        return False
    return True

def validate_username(username: str) -> bool:
    """Validate username"""
    if not username:
        return False
    if len(username) < 3:
        return False
    if len(username) > 32:
        return False
    if not username.isalnum():
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
    if not language_code.isalpha():
        return False
    return True

def validate_phone_number(phone_number: str) -> bool:
    """Validate phone number"""
    if not phone_number:
        return False
    if len(phone_number) < 10:
        return False
    if len(phone_number) > 15:
        return False
    if not phone_number.isdigit():
        return False
    return True

def validate_email(email: str) -> bool:
    """Validate email"""
    if not email:
        return False
    if len(email) < 5:
        return False
    if len(email) > 254:
        return False
    if "@" not in email:
        return False
    if "." not in email:
        return False
    return True

def validate_url(url: str) -> bool:
    """Validate URL"""
    if not url:
        return False
    if len(url) < 5:
        return False
    if len(url) > 2048:
        return False
    if not url.startswith(("http://", "https://")):
        return False
    return True

def validate_date(date: str) -> bool:
    """Validate date"""
    if not date:
        return False
    if len(date) != 10:
        return False
    try:
        from datetime import datetime
        datetime.strptime(date, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def validate_time(time: str) -> bool:
    """Validate time"""
    if not time:
        return False
    if len(time) != 5:
        return False
    try:
        from datetime import datetime
        datetime.strptime(time, "%H:%M")
        return True
    except ValueError:
        return False

def validate_datetime(datetime_str: str) -> bool:
    """Validate datetime"""
    if not datetime_str:
        return False
    if len(datetime_str) != 19:
        return False
    try:
        from datetime import datetime
        datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
        return True
    except ValueError:
        return False

def validate_boolean(value: bool) -> bool:
    """Validate boolean"""
    return isinstance(value, bool)

def validate_integer(value: int) -> bool:
    """Validate integer"""
    return isinstance(value, int)

def validate_float(value: float) -> bool:
    """Validate float"""
    return isinstance(value, float)

def validate_string(value: str) -> bool:
    """Validate string"""
    return isinstance(value, str)

def validate_list(value: list) -> bool:
    """Validate list"""
    return isinstance(value, list)

def validate_dict(value: dict) -> bool:
    """Validate dict"""
    return isinstance(value, dict)

def validate_required_fields(
    data: Dict[str, Any],
    required_fields: List[str]
) -> bool:
    """Validate required fields"""
    return all(field in data for field in required_fields)

def validate_field_types(
    data: Dict[str, Any],
    field_types: Dict[str, type]
) -> bool:
    """Validate field types"""
    return all(
        isinstance(data.get(field), field_type)
        for field, field_type in field_types.items()
        if field in data
    )

def validate_field_values(
    data: Dict[str, Any],
    field_validators: Dict[str, callable]
) -> bool:
    """Validate field values"""
    return all(
        validator(data.get(field))
        for field, validator in field_validators.items()
        if field in data
    )

def validate_data(
    data: Dict[str, Any],
    required_fields: List[str],
    field_types: Dict[str, type],
    field_validators: Dict[str, callable]
) -> bool:
    """Validate data"""
    if not validate_required_fields(data, required_fields):
        return False
    if not validate_field_types(data, field_types):
        return False
    if not validate_field_values(data, field_validators):
        return False
    return True

def ensure_organization_name(name: str) -> None:
    """Ensure organization name is valid"""
    if not validate_organization_name(name):
        raise ValidationError("Invalid organization name")

def ensure_organization_description(description: str) -> None:
    """Ensure organization description is valid"""
    if not validate_organization_description(description):
        raise ValidationError("Invalid organization description")

def ensure_menu_item_name(name: str) -> None:
    """Ensure menu item name is valid"""
    if not validate_menu_item_name(name):
        raise ValidationError("Invalid menu item name")

def ensure_menu_item_price(price: float) -> None:
    """Ensure menu item price is valid"""
    if not validate_menu_item_price(price):
        raise ValidationError("Invalid menu item price")

def ensure_menu_item_description(description: Optional[str]) -> None:
    """Ensure menu item description is valid"""
    if not validate_menu_item_description(description):
        raise ValidationError("Invalid menu item description")

def ensure_menu_category(category: str) -> None:
    """Ensure menu category is valid"""
    if not validate_menu_category(category):
        raise ValidationError("Invalid menu category")

def ensure_image_type(image_type: str) -> None:
    """Ensure image type is valid"""
    if not validate_image_type(image_type):
        raise ValidationError("Invalid image type")

def ensure_qr_type(qr_type: str) -> None:
    """Ensure QR type is valid"""
    if not validate_qr_type(qr_type):
        raise ValidationError("Invalid QR type")

def ensure_qr_content(content: str) -> None:
    """Ensure QR content is valid"""
    if not validate_qr_content(content):
        raise ValidationError("Invalid QR content")

def ensure_theme_name(theme_name: str) -> None:
    """Ensure theme name is valid"""
    if not validate_theme_name(theme_name):
        raise ValidationError("Invalid theme name")

def ensure_theme_config(config: Dict[str, Any]) -> None:
    """Ensure theme config is valid"""
    if not validate_theme_config(config):
        raise ValidationError("Invalid theme config")

def ensure_web_page_title(title: str) -> None:
    """Ensure web page title is valid"""
    if not validate_web_page_title(title):
        raise ValidationError("Invalid web page title")

def ensure_web_page_content(content: str) -> None:
    """Ensure web page content is valid"""
    if not validate_web_page_content(content):
        raise ValidationError("Invalid web page content")

def ensure_web_page_config(config: Dict[str, Any]) -> None:
    """Ensure web page config is valid"""
    if not validate_web_page_config(config):
        raise ValidationError("Invalid web page config")

def ensure_user_id(user_id: int) -> None:
    """Ensure user ID is valid"""
    if not validate_user_id(user_id):
        raise ValidationError("Invalid user ID")

def ensure_username(username: str) -> None:
    """Ensure username is valid"""
    if not validate_username(username):
        raise ValidationError("Invalid username")

def ensure_first_name(first_name: str) -> None:
    """Ensure first name is valid"""
    if not validate_first_name(first_name):
        raise ValidationError("Invalid first name")

def ensure_last_name(last_name: str) -> None:
    """Ensure last name is valid"""
    if not validate_last_name(last_name):
        raise ValidationError("Invalid last name")

def ensure_language_code(language_code: str) -> None:
    """Ensure language code is valid"""
    if not validate_language_code(language_code):
        raise ValidationError("Invalid language code")

def ensure_phone_number(phone_number: str) -> None:
    """Ensure phone number is valid"""
    if not validate_phone_number(phone_number):
        raise ValidationError("Invalid phone number")

def ensure_email(email: str) -> None:
    """Ensure email is valid"""
    if not validate_email(email):
        raise ValidationError("Invalid email")

def ensure_url(url: str) -> None:
    """Ensure URL is valid"""
    if not validate_url(url):
        raise ValidationError("Invalid URL")

def ensure_date(date: str) -> None:
    """Ensure date is valid"""
    if not validate_date(date):
        raise ValidationError("Invalid date")

def ensure_time(time: str) -> None:
    """Ensure time is valid"""
    if not validate_time(time):
        raise ValidationError("Invalid time")

def ensure_datetime(datetime_str: str) -> None:
    """Ensure datetime is valid"""
    if not validate_datetime(datetime_str):
        raise ValidationError("Invalid datetime")

def ensure_boolean(value: bool) -> None:
    """Ensure boolean is valid"""
    if not validate_boolean(value):
        raise ValidationError("Invalid boolean")

def ensure_integer(value: int) -> None:
    """Ensure integer is valid"""
    if not validate_integer(value):
        raise ValidationError("Invalid integer")

def ensure_float(value: float) -> None:
    """Ensure float is valid"""
    if not validate_float(value):
        raise ValidationError("Invalid float")

def ensure_string(value: str) -> None:
    """Ensure string is valid"""
    if not validate_string(value):
        raise ValidationError("Invalid string")

def ensure_list(value: list) -> None:
    """Ensure list is valid"""
    if not validate_list(value):
        raise ValidationError("Invalid list")

def ensure_dict(value: dict) -> None:
    """Ensure dict is valid"""
    if not validate_dict(value):
        raise ValidationError("Invalid dict")

def ensure_required_fields(
    data: Dict[str, Any],
    required_fields: List[str]
) -> None:
    """Ensure required fields are present"""
    if not validate_required_fields(data, required_fields):
        raise ValidationError("Missing required fields")

def ensure_field_types(
    data: Dict[str, Any],
    field_types: Dict[str, type]
) -> None:
    """Ensure field types are valid"""
    if not validate_field_types(data, field_types):
        raise ValidationError("Invalid field types")

def ensure_field_values(
    data: Dict[str, Any],
    field_validators: Dict[str, callable]
) -> None:
    """Ensure field values are valid"""
    if not validate_field_values(data, field_validators):
        raise ValidationError("Invalid field values")

def ensure_data(
    data: Dict[str, Any],
    required_fields: List[str],
    field_types: Dict[str, type],
    field_validators: Dict[str, callable]
) -> None:
    """Ensure data is valid"""
    if not validate_data(data, required_fields, field_types, field_validators):
        raise ValidationError("Invalid data") 