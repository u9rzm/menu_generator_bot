from fastapi import  Form, FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path

from typing import Dict, List
from jinja2 import Environment, FileSystemLoader
import shutil


from base import PageData

app = FastAPI()

# Настройка шаблонов
templates = Jinja2Templates(directory="templates")
env = Environment(loader=FileSystemLoader("templates"))

# Подключение статики
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def form_page(request: Request):
    return templates.TemplateResponse("template.html", {"request": request})


@app.post("/generate")
async def generate_page(data:PageData):
    print(data.theme)
    
    target_dir = Path(f"static/pages/{data.page_name}")
    target_dir.mkdir(parents=True, exist_ok=True)
    # for image in images:
    #     img_path = images_dir / image.filename
    #     with img_path.open("wb") as buffer:
    #         shutil.copyfileobj(image.file, buffer)

    template = env.get_template("menu.html")
    # # Создание папки images внутри целевой директории
    # (target_dir / "images").mkdir(exist_ok=True)

    html_content = template.render(
            organization=data,
            categories=data.content,
            menu_url='menu_url',
            theme=data.theme
        )
    print(f"/pages/{data.page_name}/index.html")
    print(data)
    print(data.content)
    # Сохраняем HTML
    output_path = target_dir / "index.html"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    return JSONResponse({
        "status": "success",
        "url": f"/pages/{data.page_name}/index.html"
    })
