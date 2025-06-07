import os
import aiohttp
from typing import Any, Dict, Optional, List, Union
from app.bot.infrastructure.config.config import settings
from app.bot.infrastructure.utils.logging_utils import log_api_request, log_api_response
from app.bot.infrastructure.exceptions.handler_exceptions import APIError

async def make_request(
    method: str,
    endpoint: str,
    data: Optional[Dict[str, Any]] = None,
    params: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, str]] = None,
    files: Optional[Dict[str, Any]] = None,
    timeout: int = 30
) -> Dict[str, Any]:
    """Make API request"""
    url = f"{settings.API_URL}{endpoint}"
    
    log_api_request(
        method=method,
        url=url,
        data={
            "data": data,
            "params": params,
            "headers": headers,
            "files": files
        }
    )
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.request(
                method=method,
                url=url,
                json=data,
                params=params,
                headers=headers,
                data=files,
                timeout=timeout
            ) as response:
                response_data = await response.json()
                
                log_api_response(
                    status_code=response.status,
                    data=response_data
                )
                
                if response.status >= 400:
                    raise APIError(
                        f"API request failed with status {response.status}: {response_data}"
                    )
                
                return response_data
    except aiohttp.ClientError as e:
        raise APIError(f"API request failed: {str(e)}")
    except Exception as e:
        raise APIError(f"Unexpected error during API request: {str(e)}")

async def get(
    endpoint: str,
    params: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, str]] = None,
    timeout: int = 30
) -> Dict[str, Any]:
    """Make GET request"""
    return await make_request(
        method="GET",
        endpoint=endpoint,
        params=params,
        headers=headers,
        timeout=timeout
    )

async def post(
    endpoint: str,
    data: Optional[Dict[str, Any]] = None,
    params: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, str]] = None,
    files: Optional[Dict[str, Any]] = None,
    timeout: int = 30
) -> Dict[str, Any]:
    """Make POST request"""
    return await make_request(
        method="POST",
        endpoint=endpoint,
        data=data,
        params=params,
        headers=headers,
        files=files,
        timeout=timeout
    )

async def put(
    endpoint: str,
    data: Optional[Dict[str, Any]] = None,
    params: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, str]] = None,
    files: Optional[Dict[str, Any]] = None,
    timeout: int = 30
) -> Dict[str, Any]:
    """Make PUT request"""
    return await make_request(
        method="PUT",
        endpoint=endpoint,
        data=data,
        params=params,
        headers=headers,
        files=files,
        timeout=timeout
    )

async def patch(
    endpoint: str,
    data: Optional[Dict[str, Any]] = None,
    params: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, str]] = None,
    files: Optional[Dict[str, Any]] = None,
    timeout: int = 30
) -> Dict[str, Any]:
    """Make PATCH request"""
    return await make_request(
        method="PATCH",
        endpoint=endpoint,
        data=data,
        params=params,
        headers=headers,
        files=files,
        timeout=timeout
    )

async def delete(
    endpoint: str,
    params: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, str]] = None,
    timeout: int = 30
) -> Dict[str, Any]:
    """Make DELETE request"""
    return await make_request(
        method="DELETE",
        endpoint=endpoint,
        params=params,
        headers=headers,
        timeout=timeout
    )

async def register_user(
    user_id: int,
    username: Optional[str] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    language_code: Optional[str] = None
) -> Dict[str, Any]:
    """Register user"""
    data = {
        "user_id": user_id,
        "username": username,
        "first_name": first_name,
        "last_name": last_name,
        "language_code": language_code
    }
    return await post("/users", data=data)

async def get_user(user_id: int) -> Dict[str, Any]:
    """Get user"""
    return await get(f"/users/{user_id}")

async def update_user(
    user_id: int,
    data: Dict[str, Any]
) -> Dict[str, Any]:
    """Update user"""
    return await put(f"/users/{user_id}", data=data)

async def delete_user(user_id: int) -> Dict[str, Any]:
    """Delete user"""
    return await delete(f"/users/{user_id}")

async def create_organization(
    user_id: int,
    name: str,
    description: Optional[str] = None
) -> Dict[str, Any]:
    """Create organization"""
    data = {
        "user_id": user_id,
        "name": name,
        "description": description
    }
    return await post("/organizations", data=data)

async def get_organization(organization_id: int) -> Dict[str, Any]:
    """Get organization"""
    return await get(f"/organizations/{organization_id}")

async def update_organization(
    organization_id: int,
    data: Dict[str, Any]
) -> Dict[str, Any]:
    """Update organization"""
    return await put(f"/organizations/{organization_id}", data=data)

async def delete_organization(organization_id: int) -> Dict[str, Any]:
    """Delete organization"""
    return await delete(f"/organizations/{organization_id}")

async def get_user_organizations(user_id: int) -> List[Dict[str, Any]]:
    """Get user organizations"""
    return await get(f"/users/{user_id}/organizations")

async def create_menu(
    organization_id: int,
    name: str,
    description: Optional[str] = None
) -> Dict[str, Any]:
    """Create menu"""
    data = {
        "organization_id": organization_id,
        "name": name,
        "description": description
    }
    return await post("/menus", data=data)

async def get_menu(menu_id: int) -> Dict[str, Any]:
    """Get menu"""
    return await get(f"/menus/{menu_id}")

async def update_menu(
    menu_id: int,
    data: Dict[str, Any]
) -> Dict[str, Any]:
    """Update menu"""
    return await put(f"/menus/{menu_id}", data=data)

async def delete_menu(menu_id: int) -> Dict[str, Any]:
    """Delete menu"""
    return await delete(f"/menus/{menu_id}")

async def get_organization_menus(organization_id: int) -> List[Dict[str, Any]]:
    """Get organization menus"""
    return await get(f"/organizations/{organization_id}/menus")

async def create_menu_item(
    menu_id: int,
    name: str,
    price: float,
    description: Optional[str] = None,
    category: Optional[str] = None
) -> Dict[str, Any]:
    """Create menu item"""
    data = {
        "menu_id": menu_id,
        "name": name,
        "price": price,
        "description": description,
        "category": category
    }
    return await post("/menu-items", data=data)

async def get_menu_item(menu_item_id: int) -> Dict[str, Any]:
    """Get menu item"""
    return await get(f"/menu-items/{menu_item_id}")

async def update_menu_item(
    menu_item_id: int,
    data: Dict[str, Any]
) -> Dict[str, Any]:
    """Update menu item"""
    return await put(f"/menu-items/{menu_item_id}", data=data)

async def delete_menu_item(menu_item_id: int) -> Dict[str, Any]:
    """Delete menu item"""
    return await delete(f"/menu-items/{menu_item_id}")

async def get_menu_items(menu_id: int) -> List[Dict[str, Any]]:
    """Get menu items"""
    return await get(f"/menus/{menu_id}/items")

async def create_theme(
    name: str,
    description: Optional[str] = None,
    config: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Create theme"""
    data = {
        "name": name,
        "description": description,
        "config": config
    }
    return await post("/themes", data=data)

async def get_theme(theme_id: int) -> Dict[str, Any]:
    """Get theme"""
    return await get(f"/themes/{theme_id}")

async def update_theme(
    theme_id: int,
    data: Dict[str, Any]
) -> Dict[str, Any]:
    """Update theme"""
    return await put(f"/themes/{theme_id}", data=data)

async def delete_theme(theme_id: int) -> Dict[str, Any]:
    """Delete theme"""
    return await delete(f"/themes/{theme_id}")

async def get_themes() -> List[Dict[str, Any]]:
    """Get themes"""
    return await get("/themes")

async def create_qr_code(
    organization_id: int,
    type: str,
    content: str,
    config: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Create QR code"""
    data = {
        "organization_id": organization_id,
        "type": type,
        "content": content,
        "config": config
    }
    return await post("/qr-codes", data=data)

async def get_qr_code(qr_code_id: int) -> Dict[str, Any]:
    """Get QR code"""
    return await get(f"/qr-codes/{qr_code_id}")

async def update_qr_code(
    qr_code_id: int,
    data: Dict[str, Any]
) -> Dict[str, Any]:
    """Update QR code"""
    return await put(f"/qr-codes/{qr_code_id}", data=data)

async def delete_qr_code(qr_code_id: int) -> Dict[str, Any]:
    """Delete QR code"""
    return await delete(f"/qr-codes/{qr_code_id}")

async def get_organization_qr_codes(organization_id: int) -> List[Dict[str, Any]]:
    """Get organization QR codes"""
    return await get(f"/organizations/{organization_id}/qr-codes")

async def create_web_page(
    organization_id: int,
    title: str,
    content: str,
    config: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Create web page"""
    data = {
        "organization_id": organization_id,
        "title": title,
        "content": content,
        "config": config
    }
    return await post("/web-pages", data=data)

async def get_web_page(web_page_id: int) -> Dict[str, Any]:
    """Get web page"""
    return await get(f"/web-pages/{web_page_id}")

async def update_web_page(
    web_page_id: int,
    data: Dict[str, Any]
) -> Dict[str, Any]:
    """Update web page"""
    return await put(f"/web-pages/{web_page_id}", data=data)

async def delete_web_page(web_page_id: int) -> Dict[str, Any]:
    """Delete web page"""
    return await delete(f"/web-pages/{web_page_id}")

async def get_organization_web_pages(organization_id: int) -> List[Dict[str, Any]]:
    """Get organization web pages"""
    return await get(f"/organizations/{organization_id}/web-pages")

async def upload_file(
    file_path: str,
    file_type: str,
    organization_id: Optional[int] = None
) -> Dict[str, Any]:
    """Upload file"""
    with open(file_path, "rb") as f:
        files = {"file": f}
        data = {
            "file_type": file_type,
            "organization_id": organization_id
        }
        return await post("/files", data=data, files=files)

async def get_file(file_id: int) -> Dict[str, Any]:
    """Get file"""
    return await get(f"/files/{file_id}")

async def delete_file(file_id: int) -> Dict[str, Any]:
    """Delete file"""
    return await delete(f"/files/{file_id}")

async def get_organization_files(
    organization_id: int,
    file_type: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Get organization files"""
    params = {"file_type": file_type} if file_type else None
    return await get(f"/organizations/{organization_id}/files", params=params)

async def upload_menu(org_id: int, file_path: str) -> Dict[str, Any]:
    """Upload menu to API"""
    with open(file_path, 'rb') as f:
        return await make_request(
            method="POST",
            endpoint=f"/organizations/{org_id}/menu",
            files={"file": f}
        )
        
async def get_menu(org_id: int) -> list[Dict[str, Any]]:
    """Get menu from API"""
    return await make_request(
        method="GET",
        endpoint=f"/organizations/{org_id}/menu"
    )
    
async def upload_image(
    org_id: int,
    image_type: str,
    file_path: str
) -> Dict[str, Any]:
    """Upload image to API"""
    with open(file_path, 'rb') as f:
        return await make_request(
            method="POST",
            endpoint=f"/organizations/{org_id}/images",
            data={"image_type": image_type},
            files={"file": f}
        )
        
async def get_images(org_id: int) -> list[Dict[str, Any]]:
    """Get images from API"""
    return await make_request(
        method="GET",
        endpoint=f"/organizations/{org_id}/images"
    )
    
async def delete_image(org_id: int, image_id: int) -> None:
    """Delete image from API"""
    await make_request(
        method="DELETE",
        endpoint=f"/organizations/{org_id}/images/{image_id}"
    )
    
async def generate_qr_code(org_id: int) -> Dict[str, Any]:
    """Generate QR code in API"""
    return await make_request(
        method="POST",
        endpoint=f"/organizations/{org_id}/qr-codes"
    )
    
async def get_qr_codes(org_id: int) -> list[Dict[str, Any]]:
    """Get QR codes from API"""
    return await make_request(
        method="GET",
        endpoint=f"/organizations/{org_id}/qr-codes"
    )
    
async def get_themes() -> list[Dict[str, Any]]:
    """Get themes from API"""
    return await make_request(
        method="GET",
        endpoint="/themes"
    )
    
async def set_theme(org_id: int, theme_id: int) -> Dict[str, Any]:
    """Set theme in API"""
    return await make_request(
        method="PUT",
        endpoint=f"/organizations/{org_id}/theme",
        data={"theme_id": theme_id}
    )
    
async def generate_web_page(org_id: int) -> Dict[str, Any]:
    """Generate web page in API"""
    return await make_request(
        method="POST",
        endpoint=f"/organizations/{org_id}/web-page"
    ) 