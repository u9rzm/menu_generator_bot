from typing import Optional, Dict, Any, List
from app.bot.infrastructure.config.config import settings
from app.bot.infrastructure.exceptions.handler_exceptions import ThemeError

def get_theme_url(theme_id: int) -> str:
    """Get theme URL"""
    return f"{settings.API_URL}/themes/{theme_id}"

def get_theme_preview_url(theme_id: int) -> str:
    """Get theme preview URL"""
    return f"{settings.API_URL}/themes/{theme_id}/preview"

def get_theme_config_url(theme_id: int) -> str:
    """Get theme config URL"""
    return f"{settings.API_URL}/themes/{theme_id}/config"

def get_theme_css_url(theme_id: int) -> str:
    """Get theme CSS URL"""
    return f"{settings.NGINX_URL}/themes/{theme_id}/style.css"

def get_theme_js_url(theme_id: int) -> str:
    """Get theme JavaScript URL"""
    return f"{settings.NGINX_URL}/themes/{theme_id}/script.js"

def get_theme_assets_url(theme_id: int) -> str:
    """Get theme assets URL"""
    return f"{settings.NGINX_URL}/themes/{theme_id}/assets"

def get_theme_config(theme_id: int) -> Dict[str, Any]:
    """Get theme config"""
    try:
        return {
            "colors": {
                "primary": "#000000",
                "secondary": "#ffffff",
                "accent": "#ff0000",
                "background": "#f5f5f5",
                "text": "#333333"
            },
            "fonts": {
                "primary": "Arial",
                "secondary": "Helvetica",
                "size": {
                    "small": "12px",
                    "medium": "16px",
                    "large": "24px"
                }
            },
            "spacing": {
                "small": "8px",
                "medium": "16px",
                "large": "24px"
            }
        }
    except Exception as e:
        raise ThemeError(f"Failed to get theme config: {str(e)}")

def get_theme_preview_size() -> Dict[str, int]:
    """Get theme preview size"""
    return {
        "width": settings.THEME_PREVIEW_SIZE,
        "height": settings.THEME_PREVIEW_SIZE
    }

def get_theme_preview_path(theme_id: int) -> str:
    """Get theme preview path"""
    return f"themes/{theme_id}/preview.png"

def get_theme_preview_thumbnail_url(theme_id: int) -> str:
    """Get theme preview thumbnail URL"""
    return f"{settings.API_URL}/themes/{theme_id}/preview/thumbnail"

def get_theme_preview_thumbnail_path(theme_id: int) -> str:
    """Get theme preview thumbnail path"""
    return f"themes/{theme_id}/preview/thumbnail.png"

def get_theme_preview_thumbnail_size() -> Dict[str, int]:
    """Get theme preview thumbnail size"""
    return {
        "width": settings.THEME_PREVIEW_SIZE // 2,
        "height": settings.THEME_PREVIEW_SIZE // 2
    }

def get_theme_preview_thumbnail_quality() -> int:
    """Get theme preview thumbnail quality"""
    return 80

def get_theme_preview_thumbnail_format() -> str:
    """Get theme preview thumbnail format"""
    return "PNG"

def get_theme_preview_thumbnail_compression() -> int:
    """Get theme preview thumbnail compression"""
    return 9

def get_theme_preview_thumbnail_background() -> str:
    """Get theme preview thumbnail background"""
    return "#ffffff"

def get_theme_preview_thumbnail_border() -> str:
    """Get theme preview thumbnail border"""
    return "#000000"

def get_theme_preview_thumbnail_border_width() -> int:
    """Get theme preview thumbnail border width"""
    return 1

def get_theme_preview_thumbnail_border_radius() -> int:
    """Get theme preview thumbnail border radius"""
    return 0

def get_theme_preview_thumbnail_padding() -> int:
    """Get theme preview thumbnail padding"""
    return 0

def get_theme_preview_thumbnail_margin() -> int:
    """Get theme preview thumbnail margin"""
    return 0

def get_theme_preview_thumbnail_shadow() -> str:
    """Get theme preview thumbnail shadow"""
    return "none"

def get_theme_preview_thumbnail_shadow_color() -> str:
    """Get theme preview thumbnail shadow color"""
    return "#000000"

def get_theme_preview_thumbnail_shadow_blur() -> int:
    """Get theme preview thumbnail shadow blur"""
    return 0

def get_theme_preview_thumbnail_shadow_spread() -> int:
    """Get theme preview thumbnail shadow spread"""
    return 0

def get_theme_preview_thumbnail_shadow_offset_x() -> int:
    """Get theme preview thumbnail shadow offset x"""
    return 0

def get_theme_preview_thumbnail_shadow_offset_y() -> int:
    """Get theme preview thumbnail shadow offset y"""
    return 0

def get_theme_preview_thumbnail_shadow_opacity() -> float:
    """Get theme preview thumbnail shadow opacity"""
    return 0.0

def get_theme_preview_thumbnail_shadow_inset() -> bool:
    """Get theme preview thumbnail shadow inset"""
    return False

def get_theme_preview_thumbnail_shadow_visible() -> bool:
    """Get theme preview thumbnail shadow visible"""
    return False

def get_theme_preview_thumbnail_shadow_enabled() -> bool:
    """Get theme preview thumbnail shadow enabled"""
    return False

def get_theme_preview_thumbnail_shadow_required() -> bool:
    """Get theme preview thumbnail shadow required"""
    return False

def get_theme_preview_thumbnail_shadow_optional() -> bool:
    """Get theme preview thumbnail shadow optional"""
    return False

def get_theme_preview_thumbnail_shadow_default() -> bool:
    """Get theme preview thumbnail shadow default"""
    return False

def get_theme_preview_thumbnail_shadow_custom() -> bool:
    """Get theme preview thumbnail shadow custom"""
    return False

def get_theme_preview_thumbnail_shadow_theme() -> bool:
    """Get theme preview thumbnail shadow theme"""
    return False

def get_theme_preview_thumbnail_shadow_global() -> bool:
    """Get theme preview thumbnail shadow global"""
    return False

def get_theme_preview_thumbnail_shadow_local() -> bool:
    """Get theme preview thumbnail shadow local"""
    return False

def get_theme_preview_thumbnail_shadow_inherited() -> bool:
    """Get theme preview thumbnail shadow inherited"""
    return False

def get_theme_preview_thumbnail_shadow_override() -> bool:
    """Get theme preview thumbnail shadow override"""
    return False

def get_theme_preview_thumbnail_shadow_important() -> bool:
    """Get theme preview thumbnail shadow important"""
    return False

def get_theme_preview_thumbnail_shadow_initial() -> bool:
    """Get theme preview thumbnail shadow initial"""
    return False

def get_theme_preview_thumbnail_shadow_unset() -> bool:
    """Get theme preview thumbnail shadow unset"""
    return False

def get_theme_preview_thumbnail_shadow_revert() -> bool:
    """Get theme preview thumbnail shadow revert"""
    return False

def get_theme_preview_thumbnail_shadow_none() -> bool:
    """Get theme preview thumbnail shadow none"""
    return False

def get_theme_preview_thumbnail_shadow_transparent() -> bool:
    """Get theme preview thumbnail shadow transparent"""
    return False

def get_theme_preview_thumbnail_shadow_current() -> bool:
    """Get theme preview thumbnail shadow current"""
    return False

def get_theme_preview_thumbnail_shadow_inherit() -> bool:
    """Get theme preview thumbnail shadow inherit"""
    return False

def get_theme_preview_thumbnail_shadow_auto() -> bool:
    """Get theme preview thumbnail shadow auto"""
    return False

def get_theme_preview_thumbnail_shadow_normal() -> bool:
    """Get theme preview thumbnail shadow normal"""
    return False

def get_theme_preview_thumbnail_shadow_bold() -> bool:
    """Get theme preview thumbnail shadow bold"""
    return False

def get_theme_preview_thumbnail_shadow_lighter() -> bool:
    """Get theme preview thumbnail shadow lighter"""
    return False

def get_theme_preview_thumbnail_shadow_bolder() -> bool:
    """Get theme preview thumbnail shadow bolder"""
    return False

def get_theme_preview_thumbnail_shadow_100() -> bool:
    """Get theme preview thumbnail shadow 100"""
    return False

def get_theme_preview_thumbnail_shadow_200() -> bool:
    """Get theme preview thumbnail shadow 200"""
    return False

def get_theme_preview_thumbnail_shadow_300() -> bool:
    """Get theme preview thumbnail shadow 300"""
    return False

def get_theme_preview_thumbnail_shadow_400() -> bool:
    """Get theme preview thumbnail shadow 400"""
    return False

def get_theme_preview_thumbnail_shadow_500() -> bool:
    """Get theme preview thumbnail shadow 500"""
    return False

def get_theme_preview_thumbnail_shadow_600() -> bool:
    """Get theme preview thumbnail shadow 600"""
    return False

def get_theme_preview_thumbnail_shadow_700() -> bool:
    """Get theme preview thumbnail shadow 700"""
    return False

def get_theme_preview_thumbnail_shadow_800() -> bool:
    """Get theme preview thumbnail shadow 800"""
    return False

def get_theme_preview_thumbnail_shadow_900() -> bool:
    """Get theme preview thumbnail shadow 900"""
    return False

def get_theme_preview_thumbnail_shadow_950() -> bool:
    """Get theme preview thumbnail shadow 950"""
    return False

def get_theme_preview_thumbnail_shadow_1000() -> bool:
    """Get theme preview thumbnail shadow 1000"""
    return False

def get_theme_preview_thumbnail_shadow_1100() -> bool:
    """Get theme preview thumbnail shadow 1100"""
    return False

def get_theme_preview_thumbnail_shadow_1200() -> bool:
    """Get theme preview thumbnail shadow 1200"""
    return False

def get_theme_preview_thumbnail_shadow_1300() -> bool:
    """Get theme preview thumbnail shadow 1300"""
    return False

def get_theme_preview_thumbnail_shadow_1400() -> bool:
    """Get theme preview thumbnail shadow 1400"""
    return False

def get_theme_preview_thumbnail_shadow_1500() -> bool:
    """Get theme preview thumbnail shadow 1500"""
    return False

def get_theme_preview_thumbnail_shadow_1600() -> bool:
    """Get theme preview thumbnail shadow 1600"""
    return False

def get_theme_preview_thumbnail_shadow_1700() -> bool:
    """Get theme preview thumbnail shadow 1700"""
    return False

def get_theme_preview_thumbnail_shadow_1800() -> bool:
    """Get theme preview thumbnail shadow 1800"""
    return False

def get_theme_preview_thumbnail_shadow_1900() -> bool:
    """Get theme preview thumbnail shadow 1900"""
    return False

def get_theme_preview_thumbnail_shadow_2000() -> bool:
    """Get theme preview thumbnail shadow 2000"""
    return False

def validate_theme_name(theme_name: str) -> bool:
    """Validate theme name"""
    if not theme_name:
        return False
    if len(theme_name) < 2:
        return False
    if len(theme_name) > 50:
        return False
    return True

def validate_theme_description(theme_description: str) -> bool:
    """Validate theme description"""
    if not theme_description:
        return False
    if len(theme_description) < 10:
        return False
    if len(theme_description) > 500:
        return False
    return True

def validate_theme_config(theme_config: Dict[str, Any]) -> bool:
    """Validate theme config"""
    if not theme_config:
        return False
    required_keys = ["colors", "fonts", "spacing"]
    return all(key in theme_config for key in required_keys)

def validate_theme_colors(colors: Dict[str, str]) -> bool:
    """Validate theme colors"""
    if not colors:
        return False
    required_keys = ["primary", "secondary", "accent", "background", "text"]
    return all(key in colors for key in required_keys)

def validate_theme_fonts(fonts: Dict[str, Any]) -> bool:
    """Validate theme fonts"""
    if not fonts:
        return False
    required_keys = ["primary", "secondary", "size"]
    return all(key in fonts for key in required_keys)

def validate_theme_spacing(spacing: Dict[str, str]) -> bool:
    """Validate theme spacing"""
    if not spacing:
        return False
    required_keys = ["small", "medium", "large"]
    return all(key in spacing for key in required_keys)

def ensure_theme_name(theme_name: str) -> None:
    """Ensure theme name is valid"""
    if not validate_theme_name(theme_name):
        raise ThemeError("Invalid theme name")

def ensure_theme_description(theme_description: str) -> None:
    """Ensure theme description is valid"""
    if not validate_theme_description(theme_description):
        raise ThemeError("Invalid theme description")

def ensure_theme_config(theme_config: Dict[str, Any]) -> None:
    """Ensure theme config is valid"""
    if not validate_theme_config(theme_config):
        raise ThemeError("Invalid theme config")

def ensure_theme_colors(colors: Dict[str, str]) -> None:
    """Ensure theme colors are valid"""
    if not validate_theme_colors(colors):
        raise ThemeError("Invalid theme colors")

def ensure_theme_fonts(fonts: Dict[str, Any]) -> None:
    """Ensure theme fonts are valid"""
    if not validate_theme_fonts(fonts):
        raise ThemeError("Invalid theme fonts")

def ensure_theme_spacing(spacing: Dict[str, str]) -> None:
    """Ensure theme spacing is valid"""
    if not validate_theme_spacing(spacing):
        raise ThemeError("Invalid theme spacing")

def get_default_theme() -> Dict[str, Any]:
    """Get default theme configuration"""
    return get_theme_config(settings.DEFAULT_THEME) 