from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()


# Путь на диске к общей статике (в т.ч. коктейли в подкаталоге)
STATIC_DIR = "app/static"
COCKTAIL_DIR = os.path.join(STATIC_DIR, "cocktails")

# Монтируем всю папку static как /static
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
# app.mount("/static", StaticFiles(directory="static"), name="static")
# COCKTAIL_DIR = "app/cocktails"

@app.get("/api/cocktails")
def get_cocktails():
    print('succes')
    files = os.listdir(COCKTAIL_DIR)
    images = [
        f"/cocktails/{file}" for file in files
        if file.lower().endswith((".jpg", ".jpeg", ".png"))
    ]
    print('succes')
    return JSONResponse(images)

@app.get("/cocktails/{filename}")
def get_image(filename: str):
    file_path = os.path.join(COCKTAIL_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return JSONResponse({"error": "Коктели не найдены"}, status_code=404)
