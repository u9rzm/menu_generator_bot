from fastapi import FastAPI, HTTPException, Depends, UploadFile, File, Form, Request, Query
from fastapi.responses import JSONResponse, HTMLResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from decimal import Decimal
import os
import shutil
from datetime import datetime
from contextlib import asynccontextmanager
import logging
import traceback
from sqlalchemy.sql import text
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from domain.db.database import get_db, init_db, get_db_session
from domain.db.models import Menu, MenuData, Main, MainData, Organization, OrganizationData, MenuItem, User, UserData
from domain.entity.tables import get_table_info , get_table_structure, get_table_data

# from routes.users import router as router_users

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")
        logger.error(traceback.format_exc())
        raise
    yield

app = FastAPI(title="Menu API", lifespan=lifespan)
#Routers

# app.include_router(router_users)

# Конфигурация
BASE_URL = "http://api:2424"
STATIC_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
PAGES_DIR = os.path.join(STATIC_DIR, "pages")

# Создаем директории если их нет
os.makedirs(STATIC_DIR, exist_ok=True)
os.makedirs(PAGES_DIR, exist_ok=True)

# Монтируем статические файлы
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Настраиваем шаблоны
templates = Jinja2Templates(directory="templates")



# Модели данных
class ThemeRequest(BaseModel):
    theme: str = 'modern-dark'

# Константы
THEMES = {
    'modern-dark': 'Современный темный',
    'light-elegant': 'Светлый элегантный',
    'minimal': 'Минималистичный',
    'vintage': 'Винтажный',
    'futuristic': 'Футуристический',
    'nature': 'Природный'
}

#templates
templates = Jinja2Templates(directory="templates")


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {str(exc)}")
    logger.error(traceback.format_exc())
    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal server error: {str(exc)}"}
    )
#Healthcheck___________________________________________________________________________
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
#Debug Tabels
@app.get("/debug/tables")
async def debug_tables():
    """Debug endpoint to check table structures and data"""
    try:
        logger.info("Starting debug_tables endpoint")
        db = get_db_session()
        try:
            return get_table_info(db)
        finally:
            db.close()
    except Exception as e:
        logger.error(f"Error in debug_tables: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))
#Debug Users________________________________________________
# # User endpoints
@app.get("/users", response_model=List[dict])
def get_users(
    skip: int = 0,
    limit: int = 100,
    owners_only: bool = False,
    db: Session = Depends(get_db)
):
    try:
        if owners_only:
            items = User.get_owners(db)
        else:
            items = db.query(User).offset(skip).limit(limit).all()
        return [item.to_dataclass().to_dict() for item in items]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Получение всех элементов меню
@app.get("/menu", response_model=List[dict])
def get_menu(
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = None,
    db: Session = Depends(get_db_session)
):
    try:
        query = db.query(Menu)
        if category:
            query = query.filter(Menu.category == category)
        items = query.offset(skip).limit(limit).all()
        return [item.to_dataclass().to_dict() for item in items]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

# Получение элемента меню по ID
@app.get("/menu/{menu_id}", response_model=dict)
def get_menu_item(menu_id: int, db: Session = Depends(get_db_session)):
    try:
        item = Menu.get_by_id(db, menu_id)
        if not item:
            raise HTTPException(status_code=404, detail="Menu item not found")
        return item.to_dataclass().to_dict()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

# Создание нового элемента меню
@app.post("/menu", response_model=dict)
def create_menu_item(
    name: str = Form(...),
    price: float = Form(...),
    category: str = Form(...),
    description: Optional[str] = Form(None),
    subcategory: Optional[str] = Form(None),
    is_available: bool = Form(True),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db_session)
):
    try:
        # Обработка изображения, если оно есть
        image_url = None
        if image:
            upload_dir = os.getenv("UPLOAD_DIR", "/files")
            os.makedirs(upload_dir, exist_ok=True)
            file_path = os.path.join(upload_dir, image.filename)
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(image.file, buffer)
            image_url = f"/files/{image.filename}"

        # Создание объекта меню
        menu_data = MenuData(
            name=name,
            price=Decimal(str(price)),
            category=category,
            description=description,
            subcategory=subcategory,
            is_available=is_available,
            image_url=image_url
        )

        # Сохранение в базу данных
        menu_item = Menu.create(db, menu_data)
        return menu_item.to_dataclass().to_dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

# Обновление элемента меню
@app.put("/menu/{menu_id}", response_model=dict)
def update_menu_item(
    menu_id: int,
    name: Optional[str] = Form(None),
    price: Optional[float] = Form(None),
    category: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    subcategory: Optional[str] = Form(None),
    is_available: Optional[bool] = Form(None),
    image: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db_session)
):
    try:
        # Получение существующего элемента
        menu_item = Menu.get_by_id(db, menu_id)
        if not menu_item:
            raise HTTPException(status_code=404, detail="Menu item not found")

        # Обработка изображения, если оно есть
        image_url = None
        if image:
            upload_dir = os.getenv("UPLOAD_DIR", "/files")
            os.makedirs(upload_dir, exist_ok=True)
            file_path = os.path.join(upload_dir, image.filename)
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(image.file, buffer)
            image_url = f"/files/{image.filename}"

        # Создание объекта с обновленными данными
        update_data = MenuData(
            name=name or menu_item.name,
            price=Decimal(str(price)) if price is not None else menu_item.price,
            category=category or menu_item.category,
            description=description if description is not None else menu_item.description,
            subcategory=subcategory if subcategory is not None else menu_item.subcategory,
            is_available=is_available if is_available is not None else menu_item.is_available,
            image_url=image_url or menu_item.image_url
        )

        # Обновление в базе данных
        updated_item = Menu.update(db, menu_id, update_data)
        return updated_item.to_dataclass().to_dict()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

# Удаление элемента меню
@app.delete("/menu/{menu_id}")
def delete_menu_item(menu_id: int, db: Session = Depends(get_db_session)):
    try:
        success = Menu.delete(db, menu_id)
        if not success:
            raise HTTPException(status_code=404, detail="Menu item not found")
        return {"status": "success", "message": "Menu item deleted"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

# Получение категорий меню
@app.get("/menu/categories", response_model=List[str])
def get_categories(db: Session = Depends(get_db_session)):
    try:
        categories = db.query(Menu.category).distinct().all()
        return [category[0] for category in categories]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

# Organization endpoints
@app.post("/organizations", response_model=dict)
def create_organization(
    name: str = Form(...),
    description: Optional[str] = Form(None),
    owner_id: int = Form(...),
    db: Session = Depends(get_db_session)
):
    """Create new organization"""
    try:
        # Генерируем имя таблицы меню
        menu_table_name = f"menu_{name.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Создаем таблицу меню
        create_menu_table_sql = f"""
        CREATE TABLE {menu_table_name} (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT,
            price NUMERIC NOT NULL,
            category TEXT NOT NULL,
            subcategory TEXT,
            is_available BOOLEAN DEFAULT TRUE,
            image_url TEXT,
            created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        db.execute(text(create_menu_table_sql))
        db.commit()

        # Создаем организацию
        org_data = OrganizationData(
            name=name,
            description=description,
            owner_id=owner_id,
            menu_table_name=menu_table_name
        )
        org = Organization.create(db, org_data)
        return org.to_dataclass().to_dict()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@app.get("/organizations", response_model=List[dict])
def get_organizations(
    skip: int = 0,
    limit: int = 100,
    owner_id: Optional[int] = None,
    db: Session = Depends(get_db_session)
):
    """Get all organizations or filter by owner"""
    try:
        if owner_id:
            orgs = Organization.get_by_owner(db, owner_id)
        else:
            orgs = Organization.get_all(db, skip, limit)
        return [org.to_dataclass().to_dict() for org in orgs]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@app.get("/organizations/{org_id}", response_model=dict)
def get_organization(org_id: int, db: Session = Depends(get_db_session)):
    """Get organization by ID"""
    try:
        org = Organization.get_by_id(db, org_id)
        if not org:
            raise HTTPException(status_code=404, detail="Organization not found")
        return org.to_dataclass().to_dict()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@app.post("/organizations/{org_id}/menu")
async def upload_menu(
    org_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db_session)
):
    """Upload menu for organization"""
    try:
        # Проверяем существование организации
        org = Organization.get_by_id(db, org_id)
        if not org:
            raise HTTPException(status_code=404, detail="Organization not found")

        # Сохраняем файл
        file_path = f"temp_{file.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Читаем и обрабатываем файл
        if file.filename.endswith('.csv'):
            import csv
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    insert_sql = f"""
                    INSERT INTO {org.menu_table_name} (name, price, category, description, subcategory)
                    VALUES (:name, :price, :category, :description, :subcategory)
                    """
                    db.execute(text(insert_sql), {
                        'name': row['name'],
                        'price': Decimal(row['price']),
                        'category': row['category'],
                        'description': row.get('description'),
                        'subcategory': row.get('subcategory')
                    })
        elif file.filename.endswith(('.xls', '.xlsx')):
            import pandas as pd
            df = pd.read_excel(file_path)
            for _, row in df.iterrows():
                insert_sql = f"""
                INSERT INTO {org.menu_table_name} (name, price, category, description, subcategory)
                VALUES (:name, :price, :category, :description, :subcategory)
                """
                db.execute(text(insert_sql), {
                    'name': row['name'],
                    'price': Decimal(str(row['price'])),
                    'category': row['category'],
                    'description': row.get('description'),
                    'subcategory': row.get('subcategory')
                })
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format")

        db.commit()

        # Удаляем временный файл
        os.remove(file_path)

        return {"status": "success", "message": "Menu uploaded successfully"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@app.get("/organizations/{org_id}/menu")
def get_organization_menu(
    org_id: int,
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = None,
    db: Session = Depends(get_db_session)
):
    """Get menu for specific organization"""
    try:
        # Получаем организацию
        org = Organization.get_by_id(db, org_id)
        if not org:
            raise HTTPException(status_code=404, detail="Organization not found")

        # Формируем SQL запрос
        query = f"""
        SELECT * FROM {org.menu_table_name}
        """
        params = {}
        
        if category:
            query += " WHERE category = :category"
            params['category'] = category
            
        query += " ORDER BY category, name LIMIT :limit OFFSET :skip"
        params['limit'] = limit
        params['skip'] = skip

        # Выполняем запрос
        result = db.execute(text(query), params)
        menu_items = []
        for row in result:
            menu_items.append({
                "id": row.id,
                "name": row.name,
                "description": row.description,
                "price": float(row.price),
                "category": row.category,
                "subcategory": row.subcategory,
                "is_available": row.is_available,
                "image_url": row.image_url,
                "created": row.created.isoformat() if row.created else None,
                "updated": row.updated.isoformat() if row.updated else None
            })

        return menu_items
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@app.get("/organizations/{org_id}/menu/categories")
def get_organization_menu_categories(
    org_id: int,
    db: Session = Depends(get_db_session)
):
    """Get menu categories for specific organization"""
    try:
        # Получаем организацию
        org = Organization.get_by_id(db, org_id)
        if not org:
            raise HTTPException(status_code=404, detail="Organization not found")

        # Получаем уникальные категории
        query = f"""
        SELECT DISTINCT category FROM {org.menu_table_name}
        ORDER BY category
        """
        result = db.execute(text(query))
        categories = [row[0] for row in result]
        
        return categories
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()



# API endpoints
@app.get("/")
async def root():
    return {"message": "Menu Generator API"}

@app.post('/api/organizations/{org_id}/menu/generate')
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

@app.get('/api/themes')
async def get_themes():
    """Возвращает список доступных тем"""
    return {
        'themes': THEMES
    }

@app.get('/api/organizations/{org_id}/menu/url')
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

@app.get("/api/organizations")
async def get_organizations(db: Session = Depends(get_db)):
    """Получает список организаций"""
    organizations = db.query(Organization).all()
    return organizations

@app.get("/api/organizations/{org_id}")
async def get_organization(org_id: int, db: Session = Depends(get_db)):
    """Получает информацию об организации"""
    org = db.query(Organization).filter(Organization.id == org_id).first()
    if not org:
        raise HTTPException(status_code=404, detail="Организация не найдена")
    return org

@app.get("/api/organizations/{org_id}/menu")
async def get_organization_menu(org_id: int, db: Session = Depends(get_db)):
    """Получает меню организации"""
    menu_items = db.query(MenuItem).filter(
        MenuItem.organization_id == org_id,
        MenuItem.is_available == True
    ).all()
    return menu_items

@app.post("/api/organizations")
async def create_organization(name: str, description: str, owner_id: int, db: Session = Depends(get_db)):
    """Создает новую организацию"""
    org = Organization(name=name, description=description, owner_id=owner_id)
    db.add(org)
    db.commit()
    db.refresh(org)
    return org

@app.post("/api/organizations/{org_id}/menu")
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

# Эндпоинты для отображения страниц
@app.get("/menu/{org_id}", response_class=HTMLResponse)
async def view_menu(org_id: int, theme: str = 'modern-dark', request: Request = None, db: Session = Depends(get_db)):
    """Отображает страницу меню"""
    try:
        # Проверяем существование страницы
        if not check_menu_page_exists(org_id, theme):
            # Если страница не существует, генерируем её
            generate_menu_page(org_id, theme, db)
        
        # Читаем сгенерированную страницу
        filename = f"menu_{org_id}_{theme}.html"
        filepath = os.path.join(PAGES_DIR, filename)
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return content

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail='Внутренняя ошибка сервера')





class ThemeRequest(BaseModel):
    theme: str = 'modern-dark'


#GET
@app.get('/themes')
async def get_themes():
    """Возвращает список доступных тем"""
    return {
        'themes': THEMES
    }

@app.get('/organizations/{org_id}/menu/url')
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

@app.get("/organizations")
async def get_organizations(db: Session = Depends(get_db)):
    """Получает список организаций"""
    organizations = db.query(Organization).all()
    return organizations

@app.get("/organizations/{org_id}")
async def get_organization(org_id: int, db: Session = Depends(get_db)):
    print("""Получает информацию об организации""")
    org = db.query(Organization).filter(Organization.id == org_id).first()
    if not org:
        raise HTTPException(status_code=404, detail="Организация не найдена")
    return org

@app.get("/organizations/{org_id}/menu")
async def get_organization_menu(org_id: int, db: Session = Depends(get_db)):
    print(
    """Получает меню организации"""
    )
    menu_items = db.query(MenuItem).filter(
        MenuItem.organization_id == org_id,
        MenuItem.is_available == True
    ).all()
    return menu_items
#POST


@app.post("/organizations")
async def create_organization(name: str, description: str, owner_id: int, db: Session = Depends(get_db)):
    """Создает новую организацию"""
    org = Organization(name=name, description=description, owner_id=owner_id)
    db.add(org)
    db.commit()
    db.refresh(org)
    return org

@app.post("/organizations/{org_id}/menu")
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

#  функции Generation page
def check_menu_page_exists(org_id: int, theme: str) -> bool:
    """Проверяет существование сгенерированной страницы"""
    filename = f"menu_{org_id}_{theme}.html"
    filepath = os.path.join(PAGES_DIR, filename)
    return os.path.exists(filepath)
def get_menu_page_url(org_id: int, theme: str) -> str:
    """Возвращает URL для страницы меню"""
    filename = f"menu_{org_id}_{theme}.html"
    return f"{BASE_URL}/static/pages/{filename}"



def generate_menu_page(org_id: int, theme: str, db: Session):
    print(f"Генерируем HTML страницу меню для организации\n " )
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

    menu_url = f"{BASE_URL}/menu/{org_id}"

    template = templates.env.get_template("menu.html")
    html_content = template.render(
        organization=org,
        categories=categories,
        menu_url=menu_url,
        theme=theme
    )
    print('sdfsdfsdfsdf')
    filename = f"menu_{org_id}_{theme}.html"
    filepath = os.path.join(PAGES_DIR, filename)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html_content)

    return filename


@app.post('/organizations/{org_id}/menu/generate')
async def generate_menu(org_id: int, request: ThemeRequest, db: Session = Depends(get_db)):
    print(f'Generating: {org_id}')
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
        raise HTTPException(status_code=500, detail=f'Внутренняя ошибка сервера {e}')
    
#Users____________________________________________________________________________________
#POST
@app.post("/register_user")
async def register_user(tid: int = Query(...), db: Session = Depends(get_db_session)):
    """Register a new user or return existing user"""
    try:
        logger.info(f"Attempting to register user with tid: {tid}")
        
        # Проверяем существование пользователя
        existing_user = User.get_by_tid(db, tid)
        if existing_user:
            logger.info(f"User with tid {tid} already exists")
            return existing_user.to_dataclass().to_dict()
        
        # Создаем нового пользователя
        user_data = UserData(tid=tid, owner=False)
        new_user = User.create(db, user_data)
        logger.info(f"Successfully registered new user with tid: {tid}")
        
        return new_user.to_dataclass().to_dict()
    except Exception as e:
        logger.error(f"Error registering user: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()
@app.post("/users", response_model=dict)
def create_user(
    tid: int = Form(...),
    owner: bool = Form(False),
    db: Session = Depends(get_db_session)
):
    try:
        user_data = UserData(
            tid=tid,
            owner=owner
        )
        user_item = User.create(db, user_data)
        return user_item.to_dataclass().to_dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()
#GET
@app.get("/users/{user_id}", response_model=dict)
def get_user(user_id: int, db: Session = Depends(get_db_session)):
    try:
        item = User.get_by_id(db, user_id)
        if not item:
            raise HTTPException(status_code=404, detail="User not found")
        return item.to_dataclass().to_dict()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@app.get("/users/telegram/{tid}", response_model=dict)
def get_user_by_tid(tid: int, db: Session = Depends(get_db_session)):
    try:
        item = User.get_by_tid(db, tid)
        if not item:
            raise HTTPException(status_code=404, detail="User not found")
        return item.to_dataclass().to_dict()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()
#_________________________________________________________________________________________





# @app.get("/debug/tables/{table_name}/structure")
# async def debug_table_structure(table_name: str):
#     """Debug endpoint to check specific table structure"""
#     try:
#         logger.info(f"Starting debug_table_structure endpoint for {table_name}")
#         db = get_db_session()
#         try:
#             return get_table_structure(db, table_name)
#         finally:
#             db.close()
#     except Exception as e:
#         logger.error(f"Error in debug_table_structure: {str(e)}")
#         logger.error(traceback.format_exc())
#         raise HTTPException(status_code=500, detail=str(e))

# @app.get("/debug/tables/{table_name}/data")
# async def debug_table_data(table_name: str, limit: int = 5):
#     """Debug endpoint to check specific table data"""
#     try:
#         logger.info(f"Starting debug_table_data endpoint for {table_name}")
#         db = get_db_session()
#         try:
#             return get_table_data(db, table_name, limit)
#         finally:
#             db.close()
#     except Exception as e:
#         logger.error(f"Error in debug_table_data: {str(e)}")
#         logger.error(traceback.format_exc())
#         raise HTTPException(status_code=500, detail=str(e))

# # Main table endpoints
# @app.get("/main", response_model=List[dict])
# def get_main_items(
#     skip: int = 0,
#     limit: int = 100,
#     owner: Optional[str] = None,
#     db: Session = Depends(get_db_session)
# ):
#     try:
#         if owner:
#             items = Main.get_by_owner(db, owner)
#         else:
#             items = Main.get_all(db, skip, limit)
#         return [item.to_dataclass().to_dict() for item in items]
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
#     finally:
#         db.close()

# @app.get("/main/{main_id}", response_model=dict)
# def get_main_item(main_id: int, db: Session = Depends(get_db_session)):
#     try:
#         item = Main.get_by_id(db, main_id)
#         if not item:
#             raise HTTPException(status_code=404, detail="Main item not found")
#         return item.to_dataclass().to_dict()
#     except HTTPException:
#         raise
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
#     finally:
#         db.close()

# @app.post("/main", response_model=dict)
# def create_main_item(
#     name: str = Form(...),
#     owner: str = Form(...),
#     name_menu_table: str = Form(...),
#     db: Session = Depends(get_db)
# ):
#     try:
#         main_data = MainData(
#             name=name,
#             owner=owner,
#             name_menu_table=name_menu_table
#         )
#         main_item = Main.create(db, main_data)
#         return main_item.to_dataclass().to_dict()
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

#______________________________________________________________________

# @app.get("/users/{user_id}", response_model=dict)
# def get_user(user_id: int, db: Session = Depends(get_db_session)):
#     try:
#         item = User.get_by_id(db, user_id)
#         if not item:
#             raise HTTPException(status_code=404, detail="User not found")
#         return item.to_dataclass().to_dict()
#     except HTTPException:
#         raise
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
#     finally:
#         db.close()

# @app.get("/users/telegram/{tid}", response_model=dict)
# def get_user_by_tid(tid: int, db: Session = Depends(get_db_session)):
#     try:
#         item = User.get_by_tid(db, tid)
#         if not item:
#             raise HTTPException(status_code=404, detail="User not found")
#         return item.to_dataclass().to_dict()
#     except HTTPException:
#         raise
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
#     finally:
#         db.close()

# @app.post("/users", response_model=dict)
# def create_user(
#     tid: int = Form(...),
#     owner: bool = Form(False),
#     db: Session = Depends(get_db_session)
# ):
#     try:
#         user_data = UserData(
#             tid=tid,
#             owner=owner
#         )
#         user_item = User.create(db, user_data)
#         return user_item.to_dataclass().to_dict()
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
#     finally:
#         db.close()

# @app.post("/register_user")
# async def register_user(tid: int = Query(...), db: Session = Depends(get_db_session)):
#     """Register a new user or return existing user"""
#     try:
#         logger.info(f"Attempting to register user with tid: {tid}")
        
#         # Проверяем существование пользователя
#         existing_user = User.get_by_tid(db, tid)
#         if existing_user:
#             logger.info(f"User with tid {tid} already exists")
#             return existing_user.to_dataclass().to_dict()
        
#         # Создаем нового пользователя
#         user_data = UserData(tid=tid, owner=False)
#         new_user = User.create(db, user_data)
#         logger.info(f"Successfully registered new user with tid: {tid}")
        
#         return new_user.to_dataclass().to_dict()
#     except Exception as e:
#         logger.error(f"Error registering user: {str(e)}")
#         logger.error(traceback.format_exc())
#         raise HTTPException(status_code=500, detail=str(e))
#     finally:
#         db.close()