FROM python:3.11-slim

WORKDIR /app

# Устанавливаем Poetry
RUN pip install --no-cache-dir poetry

# Копируем и устанавливаем зависимости
COPY pyproject.toml poetry.lock* ./
RUN poetry config virtualenvs.create false \
 && poetry install --no-root --no-interaction --no-ansi

# Копируем проект
COPY . .

# Загружаем переменные из .env
ENV $(cat .env | grep -v '^#' | xargs)

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]