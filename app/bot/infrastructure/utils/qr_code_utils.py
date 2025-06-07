from typing import Optional, Dict, Any, List
from app.bot.infrastructure.config.config import settings
from app.bot.infrastructure.exceptions.handler_exceptions import QRCodeError

def get_qr_code_url(qr_code_id: int) -> str:
    """Get QR code URL"""
    return f"{settings.API_URL}/qr-codes/{qr_code_id}"

def get_qr_code_image_url(qr_code_id: int) -> str:
    """Get QR code image URL"""
    return f"{settings.API_URL}/qr-codes/{qr_code_id}/image"

def get_qr_code_download_url(qr_code_id: int) -> str:
    """Get QR code download URL"""
    return f"{settings.API_URL}/qr-codes/{qr_code_id}/download"

def get_qr_code_config(qr_code_id: int) -> Dict[str, Any]:
    """Get QR code config"""
    try:
        return {
            "size": settings.QR_CODE_SIZE,
            "version": settings.QR_CODE_VERSION,
            "error_correction": settings.QR_CODE_ERROR_CORRECTION,
            "box_size": 10,
            "border": 4,
            "fill_color": "black",
            "back_color": "white"
        }
    except Exception as e:
        raise QRCodeError(f"Failed to get QR code config: {str(e)}")

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

def validate_qr_size(size: int) -> bool:
    """Validate QR size"""
    if not size:
        return False
    if size < 100:
        return False
    if size > 1000:
        return False
    return True

def validate_qr_version(version: int) -> bool:
    """Validate QR version"""
    if not version:
        return False
    if version < 1:
        return False
    if version > 40:
        return False
    return True

def validate_qr_error_correction(error_correction: str) -> bool:
    """Validate QR error correction"""
    valid_levels = ["L", "M", "Q", "H"]
    return error_correction in valid_levels

def validate_qr_box_size(box_size: int) -> bool:
    """Validate QR box size"""
    if not box_size:
        return False
    if box_size < 1:
        return False
    if box_size > 20:
        return False
    return True

def validate_qr_border(border: int) -> bool:
    """Validate QR border"""
    if not border:
        return False
    if border < 0:
        return False
    if border > 10:
        return False
    return True

def validate_qr_fill_color(fill_color: str) -> bool:
    """Validate QR fill color"""
    if not fill_color:
        return False
    if len(fill_color) != 7:
        return False
    if not fill_color.startswith("#"):
        return False
    return True

def validate_qr_back_color(back_color: str) -> bool:
    """Validate QR back color"""
    if not back_color:
        return False
    if len(back_color) != 7:
        return False
    if not back_color.startswith("#"):
        return False
    return True

def ensure_qr_type(qr_type: str) -> None:
    """Ensure QR type is valid"""
    if not validate_qr_type(qr_type):
        raise QRCodeError("Invalid QR type")

def ensure_qr_content(content: str) -> None:
    """Ensure QR content is valid"""
    if not validate_qr_content(content):
        raise QRCodeError("Invalid QR content")

def ensure_qr_size(size: int) -> None:
    """Ensure QR size is valid"""
    if not validate_qr_size(size):
        raise QRCodeError("Invalid QR size")

def ensure_qr_version(version: int) -> None:
    """Ensure QR version is valid"""
    if not validate_qr_version(version):
        raise QRCodeError("Invalid QR version")

def ensure_qr_error_correction(error_correction: str) -> None:
    """Ensure QR error correction is valid"""
    if not validate_qr_error_correction(error_correction):
        raise QRCodeError("Invalid QR error correction")

def ensure_qr_box_size(box_size: int) -> None:
    """Ensure QR box size is valid"""
    if not validate_qr_box_size(box_size):
        raise QRCodeError("Invalid QR box size")

def ensure_qr_border(border: int) -> None:
    """Ensure QR border is valid"""
    if not validate_qr_border(border):
        raise QRCodeError("Invalid QR border")

def ensure_qr_fill_color(fill_color: str) -> None:
    """Ensure QR fill color is valid"""
    if not validate_qr_fill_color(fill_color):
        raise QRCodeError("Invalid QR fill color")

def ensure_qr_back_color(back_color: str) -> None:
    """Ensure QR back color is valid"""
    if not validate_qr_back_color(back_color):
        raise QRCodeError("Invalid QR back color")

def get_qr_code_preview_url(org_id: int, qr_id: int) -> str:
    """Get QR code preview URL"""
    return f"{settings.NGINX_URL}/qr-codes/{org_id}/{qr_id}/preview.jpg"

def get_qr_code_download_url(org_id: int, qr_id: int) -> str:
    """Get QR code download URL"""
    return f"{settings.NGINX_URL}/qr-codes/{org_id}/{qr_id}/download.png"

def get_qr_code_embed_url(org_id: int, qr_id: int) -> str:
    """Get QR code embed URL"""
    return f"{settings.NGINX_URL}/qr-codes/{org_id}/{qr_id}/embed.html"

def get_qr_code_stats_url(org_id: int, qr_id: int) -> str:
    """Get QR code stats URL"""
    return f"{settings.NGINX_URL}/qr-codes/{org_id}/{qr_id}/stats.json"

def get_qr_code_actions_url(org_id: int, qr_id: int) -> str:
    """Get QR code actions URL"""
    return f"{settings.NGINX_URL}/qr-codes/{org_id}/{qr_id}/actions.json"

def get_qr_code_web_page_url(org_id: int, qr_id: int) -> str:
    """Get QR code web page URL"""
    return f"{settings.NGINX_URL}/qr-codes/{org_id}/{qr_id}/web-page.html"

def get_qr_code_mobile_url(org_id: int, qr_id: int) -> str:
    """Get QR code mobile URL"""
    return f"{settings.NGINX_URL}/qr-codes/{org_id}/{qr_id}/mobile.html"

def get_qr_code_desktop_url(org_id: int, qr_id: int) -> str:
    """Get QR code desktop URL"""
    return f"{settings.NGINX_URL}/qr-codes/{org_id}/{qr_id}/desktop.html"

def get_qr_code_print_url(org_id: int, qr_id: int) -> str:
    """Get QR code print URL"""
    return f"{settings.NGINX_URL}/qr-codes/{org_id}/{qr_id}/print.html"

def get_qr_code_share_url(org_id: int, qr_id: int) -> str:
    """Get QR code share URL"""
    return f"{settings.NGINX_URL}/qr-codes/{org_id}/{qr_id}/share.html"

def get_qr_code_analytics_url(org_id: int, qr_id: int) -> str:
    """Get QR code analytics URL"""
    return f"{settings.NGINX_URL}/qr-codes/{org_id}/{qr_id}/analytics.html"

def get_qr_code_settings_url(org_id: int, qr_id: int) -> str:
    """Get QR code settings URL"""
    return f"{settings.NGINX_URL}/qr-codes/{org_id}/{qr_id}/settings.html"

def get_qr_code_help_url(org_id: int, qr_id: int) -> str:
    """Get QR code help URL"""
    return f"{settings.NGINX_URL}/qr-codes/{org_id}/{qr_id}/help.html" 