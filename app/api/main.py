from fastapi import FastAPI, HTTPException, Depends, UploadFile, File, Form, Request, Query
from fastapi.responses import JSONResponse
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
import json
import aiohttp

from domain.db.database import get_db, init_db, get_db_session
from domain.db.models import Menu, MenuData, Organization, OrganizationData, MenuItem, User, UserData, Image, ImageData
from domain.entity.tables import get_table_info, get_table_structure, get_table_data

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

# Константы
BASE_URL = "http://api:2424"
STATIC_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
PAGES_DIR = os.path.join(STATIC_DIR, "pages")
IMAGE_DATA_DIR = os.path.join(STATIC_DIR, "image_data")
# Создаем директории если их нет
logger.info(f"Creating static directories:")
logger.info(f"STATIC_DIR: {STATIC_DIR}")
logger.info(f"PAGES_DIR: {PAGES_DIR}")
logger.info(f"IMAGE_DATA_DIR: {IMAGE_DATA_DIR}")
os.makedirs(STATIC_DIR, exist_ok=True)
os.makedirs(PAGES_DIR, exist_ok=True)
os.makedirs(IMAGE_DATA_DIR, exist_ok=True)

# Проверяем права доступа к директориям
for directory in [STATIC_DIR, PAGES_DIR, IMAGE_DATA_DIR]:
    if os.path.exists(directory):
        logger.info(f"Directory {directory} exists and has permissions: {oct(os.stat(directory).st_mode)[-3:]}")

# Монтируем статические файлы
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
# Настраиваем шаблоны
templates = Jinja2Templates(directory="templates")
# Модели данных
class ThemeRequest(BaseModel):
    theme: str = 'modern-dark'
class ImageUploadRequest(BaseModel):
    image_name: str
    stored_name: str

class OrganizationUpdateRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    owner_id: Optional[int] = None

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
# User endpoints
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
    db: Session = Depends(get_db_session)
):
    try:
        # Создание объекта меню
        menu_data = MenuData(
            name=name,
            price=Decimal(str(price)),
            category=category,
            description=description,
            subcategory=subcategory,
            is_available=is_available,
            image_url=None  # Изображения будут добавляться отдельно
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
        # Генерируем имя таблицы меню, удаляя все недопустимые символы
        # Оставляем только буквы, цифры и подчеркивания
        sanitized_name = ''.join(c for c in name.lower() if c.isalnum() or c == '_')
        menu_table_name = f"menu_{sanitized_name}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
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
            image_name TEXT,
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
                    INSERT INTO {org.menu_table_name} (name, price, category, description, subcategory, image_name)
                    VALUES (:name, :price, :category, :description, :subcategory, :image_name)
                    """
                    db.execute(text(insert_sql), {
                        'name': row['name'],
                        'price': Decimal(row['price']),
                        'category': row['category'],
                        'description': row.get('description'),
                        'subcategory': row.get('subcategory'),
                        'image_name': row.get('image_name')  # Добавляем имя изображения
                    })
        elif file.filename.endswith(('.xls', '.xlsx')):
            import pandas as pd
            df = pd.read_excel(file_path)
            for _, row in df.iterrows():
                insert_sql = f"""
                INSERT INTO {org.menu_table_name} (name, price, category, description, subcategory, image_name)
                VALUES (:name, :price, :category, :description, :subcategory, :image_name)
                """
                db.execute(text(insert_sql), {
                    'name': row['name'],
                    'price': Decimal(str(row['price'])),
                    'category': row['category'],
                    'description': row.get('description'),
                    'subcategory': row.get('subcategory'),
                    'image_name': row.get('image_name')  # Добавляем имя изображения
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
                "image_name": row.image_name,  # Добавляем имя изображения в ответ
                "created": row.created.isoformat() if row.created else None,
                "updated": row.updated.isoformat() if row.updated else None
            })

        return menu_items
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    # finally:
    #     db.close()

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

# API endpoints
@app.get("/")
async def root():
    return {"message": "Menu Generator API"}

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


@app.post('/organizations/{org_id}/menu/generate/{theme}')
async def generate_menu(org_id: int, theme: str, db: Session = Depends(get_db_session)):
# async def generate_menu(org_id: int , request: ThemeRequest):
    """Генерирует страницу меню для организации"""
    print(f'Type of base entry \n{type(db)}')
    try:
        if check_menu_page_exists(org_id, theme):
            url = get_menu_page_url(org_id, theme)
            return {
                'message': 'Страница уже существует',
                'url': url
            }
        if theme not in THEMES:
            raise HTTPException(status_code=400, detail=f"Неизвестная тема: {theme}")
        
       
        org = get_organization_menu(db, org_id) 
        print(f'MENU READED_____________ \n{org}')
        menu_url = f"{BASE_URL}/menu/{org_id}"

        template = templates.env.get_template("menu.html")

        # html_content = template.render(
        #     organization=org,
        #     categories=categories,
        #     menu_url=menu_url,
        #     theme=theme
        # )

        # filename = f"menu_{org_id}_{theme}.html"
        # filepath = os.path.join(PAGES_DIR, filename)
        # try:
        #     with open(filepath, 'w', encoding='utf-8') as f:
        #         f.write(html_content)  
        # except HTTPException as e:
        #     raise e (detail=f'Ошибка Создания страницы {e}')
        # return filename
        # generate_menu_page(org_id, request.theme, db)
        url = get_menu_page_url(org_id, theme)

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
        user = User.get_by_tid(db, tid)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user.to_dataclass().to_dict()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()
#_________________________________________________________________________________________

# Image handling endpoints
@app.post("/organizations/{org_id}/images")
async def upload_images(
    org_id: int,
    request: ImageUploadRequest,
    db: Session = Depends(get_db_session)
):
    try:
        # Check if organization exists
        org = Organization.get_by_id(db, org_id)
        if not org:
            raise HTTPException(status_code=404, detail="Organization not found")

        # Create organization's image directory if it doesn't exist
        org_image_dir = os.path.join(IMAGE_DATA_DIR, str(org_id))
        logger.info(f"Creating image directory at: {org_image_dir}")
        os.makedirs(org_image_dir, exist_ok=True)

        # Save metadata to database using Image model
        image_data = ImageData(
            organization_id=org_id,
            original_filename=request.image_name,
            stored_filename=request.stored_name
        )
        image = Image.create(db, image_data)
        logger.info(f"Successfully saved image metadata to database: {image.to_dataclass().to_dict()}")
        
        return {"uploaded_image": image.to_dataclass().to_dict()}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error registering image: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@app.get("/organizations/{org_id}/images")
async def get_organization_images(
    org_id: int,
    db: Session = Depends(get_db_session)
):
    try:
        # Check if organization exists
        org = Organization.get_by_id(db, org_id)
        if not org:
            raise HTTPException(status_code=404, detail="Organization not found")

        # Get images using Image model
        images = Image.get_by_organization(db, org_id)
        
        # Add full URL to each image
        result = []
        for image in images:
            image_data = image.to_dataclass().to_dict()
            image_data['url'] = f"/static/image_data/{org_id}/{image.stored_filename}"
            result.append(image_data)
            
        return {"images": result}
    except Exception as e:
        logger.error(f"Error getting images: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@app.get("/images/{image_id}")
async def get_image(
    image_id: int,
    db: Session = Depends(get_db_session)
):
    try:
        image = Image.get_by_id(db, image_id)
        if not image:
            raise HTTPException(status_code=404, detail="Image not found")
        return image.to_dataclass().to_dict()
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting image: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

@app.put("/organizations/{org_id}")
async def update_organization(
    org_id: int,
    update_data: OrganizationUpdateRequest,
    db: Session = Depends(get_db_session)
):
    """Обновляет параметры организации"""
    try:
        # Проверяем существование организации
        org = Organization.get_by_id(db, org_id)
        if not org:
            raise HTTPException(status_code=404, detail="Организация не найдена")

        # Создаем словарь с обновляемыми полями
        update_dict = {}
        if update_data.name is not None:
            update_dict['name'] = update_data.name
        if update_data.description is not None:
            update_dict['description'] = update_data.description
        if update_data.owner_id is not None:
            update_dict['owner_id'] = update_data.owner_id

        # Обновляем организацию
        for key, value in update_dict.items():
            setattr(org, key, value)

        # Сохраняем изменения
        db.commit()
        db.refresh(org)

        return org.to_dataclass().to_dict()

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating organization: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()