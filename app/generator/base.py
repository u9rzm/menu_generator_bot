from dataclasses import dataclass
from typing import Dict, List, Any
from pydantic import BaseModel
from typing import Optional
import os
NGINX_URL = os.getenv("NGINX_URL", "http://localhost")
class MenuItem(BaseModel):
    name: str
    price: float
    description: Optional[str] = None
    subcategory: Optional[str] = None
    image_url: Optional[str] = None
    def get_image_url(self) -> Optional[str]:
        if self.image_url:
            return f"{NGINX_URL}/images/{self.image_url}"
        return None

class MenuCategory(BaseModel):
    name: str
    items: List[MenuItem]

class Organization(BaseModel):
    title: str
    description: Optional[str] = None
    footer_text: Optional[str] = None

class GenerateRequest(BaseModel):
    org_id: str
    page_name: str
    title: str
    description: Optional[str] = None
    theme: str
    content: Dict[str, List[MenuItem]]
    page_background: Optional[str] = None
    header_background: Optional[str] = None
    footer_background: Optional[str] = None
    organization: Organization