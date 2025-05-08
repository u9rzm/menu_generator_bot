from fastapi import FastAPI, HTTPException, Depends, UploadFile, File, Form
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

from database import get_db, init_db, get_db_session
from models import Menu, MenuData, Main, MainData, User, UserData
from tables import get_table_info, get_table_structure, get_table_data

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

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {str(exc)}")
    logger.error(traceback.format_exc())
    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal server error: {str(exc)}"}
    )

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

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

@app.get("/debug/tables/{table_name}/structure")
async def debug_table_structure(table_name: str):
    """Debug endpoint to check specific table structure"""
    try:
        logger.info(f"Starting debug_table_structure endpoint for {table_name}")
        db = get_db_session()
        try:
            return get_table_structure(db, table_name)
        finally:
            db.close()
    except Exception as e:
        logger.error(f"Error in debug_table_structure: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/debug/tables/{table_name}/data")
async def debug_table_data(table_name: str, limit: int = 5):
    """Debug endpoint to check specific table data"""
    try:
        logger.info(f"Starting debug_table_data endpoint for {table_name}")
        db = get_db_session()
        try:
            return get_table_data(db, table_name, limit)
        finally:
            db.close()
    except Exception as e:
        logger.error(f"Error in debug_table_data: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

# Main table endpoints
@app.get("/main", response_model=List[dict])
def get_main_items(
    skip: int = 0,
    limit: int = 100,
    owner: Optional[str] = None,
    db: Session = Depends(get_db)
):
    try:
        if owner:
            items = Main.get_by_owner(db, owner)
        else:
            items = Main.get_all(db, skip, limit)
        return [item.to_dataclass().to_dict() for item in items]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/main/{main_id}", response_model=dict)
def get_main_item(main_id: int, db: Session = Depends(get_db)):
    try:
        item = Main.get_by_id(db, main_id)
        if not item:
            raise HTTPException(status_code=404, detail="Main item not found")
        return item.to_dataclass().to_dict()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/main", response_model=dict)
def create_main_item(
    name: str = Form(...),
    owner: str = Form(...),
    name_menu_table: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        main_data = MainData(
            name=name,
            owner=owner,
            name_menu_table=name_menu_table
        )
        main_item = Main.create(db, main_data)
        return main_item.to_dataclass().to_dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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

@app.get("/users/{user_id}", response_model=dict)
def get_user(user_id: int, db: Session = Depends(get_db)):
    try:
        item = User.get_by_id(db, user_id)
        if not item:
            raise HTTPException(status_code=404, detail="User not found")
        return item.to_dataclass().to_dict()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/users/telegram/{tid}", response_model=dict)
def get_user_by_tid(tid: int, db: Session = Depends(get_db)):
    try:
        item = User.get_by_tid(db, tid)
        if not item:
            raise HTTPException(status_code=404, detail="User not found")
        return item.to_dataclass().to_dict()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/users", response_model=dict)
def create_user(
    tid: int = Form(...),
    owner: bool = Form(False),
    db: Session = Depends(get_db)
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





# Получение всех элементов меню
@app.get("/menu", response_model=List[dict])
def get_menu(
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    try:
        query = db.query(Menu)
        if category:
            query = query.filter(Menu.category == category)
        items = query.offset(skip).limit(limit).all()
        return [item.to_dataclass().to_dict() for item in items]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Получение элемента меню по ID
@app.get("/menu/{menu_id}", response_model=dict)
def get_menu_item(menu_id: int, db: Session = Depends(get_db)):
    try:
        item = Menu.get_by_id(db, menu_id)
        if not item:
            raise HTTPException(status_code=404, detail="Menu item not found")
        return item.to_dataclass().to_dict()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

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
    db: Session = Depends(get_db)
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
    db: Session = Depends(get_db)
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

# Удаление элемента меню
@app.delete("/menu/{menu_id}")
def delete_menu_item(menu_id: int, db: Session = Depends(get_db)):
    try:
        success = Menu.delete(db, menu_id)
        if not success:
            raise HTTPException(status_code=404, detail="Menu item not found")
        return {"status": "success", "message": "Menu item deleted"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Получение категорий меню
@app.get("/menu/categories", response_model=List[str])
def get_categories(db: Session = Depends(get_db)):
    try:
        categories = db.query(Menu.category).distinct().all()
        return [category[0] for category in categories]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
