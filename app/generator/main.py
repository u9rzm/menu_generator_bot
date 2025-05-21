from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import logging
import traceback
from pydantic import BaseModel
from typing import Dict, List, Optional
from datetime import datetime
# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Menu Generator")

# Константы
STATIC_DIR = "/static"
TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "templates")
PAGES_DIR = "/static/pages"
NGINX_URL = os.getenv("NGINX_URL", "http://localhost")
PAGES_URL = os.getenv("PAGES_URL")
BACKGROUNDS_URL = os.getenv("BACKGROUNDS_URL")
IMAGES_URL = os.getenv("IMAGES_URL")
# Создаем директории если их нет
os.makedirs(STATIC_DIR, exist_ok=True)
os.makedirs(PAGES_DIR, exist_ok=True)

# Монтируем статические файлы
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Настраиваем шаблоны
templates = Jinja2Templates(directory=TEMPLATES_DIR)

# Модели данных
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

@app.post("/generate")
async def generate_menu(request: GenerateRequest):
    """Генерирует страницу меню"""
    try:
        # Получаем шаблон
        template = templates.env.get_template("menu.html")
        # Формируем данные для шаблона
        template_data = {
            "page_name": request.page_name,
            "title": request.title,
            "description": request.description,
            "theme": request.theme,
            "categories": request.content,
            "page_background": request.page_background,
            "header_background": request.header_background,
            "footer_background": request.footer_background,
            "organization": request.organization,
            "now": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        # Рендерим шаблон
        html_content = template.render(**template_data)

        # Сохраняем результат
        filename = f"index.html"
        os.makedirs(os.path.join(PAGES_DIR, request.org_id), exist_ok=True)
        orgpath = os.path.join(PAGES_DIR, request.org_id)
        filepath = os.path.join(orgpath, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)

        # Формируем URL для доступа к странице
        url = f"{NGINX_URL}/{PAGES_URL}/{request.org_id}/{filename}"

        return {
            "status": "success",
            "message": "Menu page generated successfully",
            "url": url
        }

    except Exception as e:
        logger.error(f"Error generating menu: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"} 