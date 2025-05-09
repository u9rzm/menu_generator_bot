from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.api.routes import router as api_router
from app.config import settings
import os

app = FastAPI(title="Menu Generator API")

# Создаем директории если их нет
os.makedirs(settings.STATIC_DIR, exist_ok=True)
os.makedirs(os.path.join(settings.STATIC_DIR, "menu_pages"), exist_ok=True)

# Монтируем статические файлы
app.mount("/static", StaticFiles(directory=settings.STATIC_DIR), name="static")

# Настраиваем шаблоны
templates = Jinja2Templates(directory="app/templates")

# Подключаем роуты
app.include_router(api_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Menu Generator API"} 