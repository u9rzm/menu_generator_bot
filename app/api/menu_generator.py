from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models import Organization, MenuItem
from app.templates import templates
from app.config import settings
import os

THEMES = {
    'modern-dark': 'Современный темный',
    'light-elegant': 'Светлый элегантный',
    'minimal': 'Минималистичный',
    'vintage': 'Винтажный',
    'futuristic': 'Футуристический',
    'nature': 'Природный'
}

def generate_menu_page(org_id: int, theme: str, db: Session) -> str:
    """Генерирует HTML страницу меню для организации"""
    if theme not in THEMES:
        raise HTTPException(status_code=400, detail=f"Неизвестная тема: {theme}")

    org = db.query(Organization).filter(Organization.id == org_id).first()
    if not org:
        raise HTTPException(status_code=404, detail=f"Организация не найдена: {org_id}")

    menu_items = db.query(MenuItem).filter(
        MenuItem.organization_id == org_id,
        MenuItem.is_available == True
    ).all()

    categories = {}
    for item in menu_items:
        if item.category not in categories:
            categories[item.category] = []
        categories[item.category].append(item)

    menu_url = f"{settings.BASE_URL}/menu/{org_id}"

    html_content = templates.TemplateResponse(
        'menu.html',
        {
            'request': {},
            'organization': org,
            'categories': categories,
            'menu_url': menu_url,
            'theme': theme
        }
    ).body.decode()

    filename = f"menu_{org_id}_{theme}.html"
    filepath = os.path.join(settings.STATIC_DIR, 'menu_pages', filename)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html_content)

    return filename

def get_menu_page_url(org_id: int, theme: str) -> str:
    """Возвращает URL для страницы меню"""
    filename = f"menu_{org_id}_{theme}.html"
    return f"{settings.BASE_URL}/static/menu_pages/{filename}"

def check_menu_page_exists(org_id: int, theme: str) -> bool:
    """Проверяет существование сгенерированной страницы"""
    filename = f"menu_{org_id}_{theme}.html"
    filepath = os.path.join(settings.STATIC_DIR, 'menu_pages', filename)
    return os.path.exists(filepath) 