from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db
from app.models import Organization, MenuItem
from app.api.menu_generator import (
    generate_menu_page,
    get_menu_page_url,
    check_menu_page_exists,
    THEMES
)

router = APIRouter()

class ThemeRequest(BaseModel):
    theme: str = 'modern-dark'

@router.post('/organizations/{org_id}/menu/generate')
async def generate_menu(org_id: int, request: ThemeRequest, db: Session = Depends(get_db)):
    """Генерирует страницу меню для организации"""
    try:
        if check_menu_page_exists(org_id, request.theme):
            url = get_menu_page_url(org_id, request.theme)
            return {
                'message': 'Страница уже существует',
                'url': url
            }

        generate_menu_page(org_id, request.theme, db)
        url = get_menu_page_url(org_id, request.theme)

        return {
            'message': 'Страница успешно сгенерирована',
            'url': url
        }

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail='Внутренняя ошибка сервера')

@router.get('/themes')
async def get_themes():
    """Возвращает список доступных тем"""
    return {
        'themes': THEMES
    }

@router.get('/organizations/{org_id}/menu/url')
async def get_menu_url(org_id: int, theme: str = 'modern-dark'):
    """Возвращает URL страницы меню"""
    try:
        if not check_menu_page_exists(org_id, theme):
            raise HTTPException(status_code=404, detail='Страница не найдена')

        url = get_menu_page_url(org_id, theme)
        return {'url': url}

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail='Внутренняя ошибка сервера')

@router.get("/organizations")
async def get_organizations(db: Session = Depends(get_db)):
    """Получает список организаций"""
    organizations = db.query(Organization).all()
    return organizations

@router.get("/organizations/{org_id}")
async def get_organization(org_id: int, db: Session = Depends(get_db)):
    """Получает информацию об организации"""
    org = db.query(Organization).filter(Organization.id == org_id).first()
    if not org:
        raise HTTPException(status_code=404, detail="Организация не найдена")
    return org

@router.get("/organizations/{org_id}/menu")
async def get_organization_menu(org_id: int, db: Session = Depends(get_db)):
    """Получает меню организации"""
    menu_items = db.query(MenuItem).filter(
        MenuItem.organization_id == org_id,
        MenuItem.is_available == True
    ).all()
    return menu_items

@router.post("/organizations")
async def create_organization(name: str, description: str, owner_id: int, db: Session = Depends(get_db)):
    """Создает новую организацию"""
    org = Organization(name=name, description=description, owner_id=owner_id)
    db.add(org)
    db.commit()
    db.refresh(org)
    return org

@router.post("/organizations/{org_id}/menu")
async def add_menu_item(
    org_id: int,
    name: str,
    price: float,
    category: str,
    description: str = None,
    db: Session = Depends(get_db)
):
    """Добавляет пункт меню"""
    menu_item = MenuItem(
        organization_id=org_id,
        name=name,
        price=price,
        category=category,
        description=description,
        is_available=True
    )
    db.add(menu_item)
    db.commit()
    db.refresh(menu_item)
    return menu_item 