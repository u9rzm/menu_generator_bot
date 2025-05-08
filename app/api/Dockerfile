FROM python:3.12.1-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV API_PORT=2424

WORKDIR /app/

# Установка системных зависимостей с повторными попытками
RUN for i in $(seq 1 3); do \
    apt-get update && \
    apt-get install -y --no-install-recommends \
        python3-dev \
        curl \
        libpq-dev \
        gcc \
        && rm -rf /var/lib/apt/lists/* \
        && break || sleep 15; \
    done

# Установка Python пакетов
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir psycopg2-binary && \
    pip install python-multipart && \
    pip install --no-cache-dir poetry

COPY pyproject.toml /app/
RUN poetry config virtualenvs.create false && \
    poetry install --no-root --no-interaction --no-ansi

EXPOSE ${API_PORT}

# Создаем скрипт для запуска
RUN echo '#!/bin/sh\n\
echo "Starting API server..."\n\
cd /app/\n\
uvicorn main:app --reload --host 0.0.0.0 --port ${API_PORT}' > /start.sh && \
chmod +x /start.sh

# Добавляем healthcheck
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${API_PORT}/health || exit 1

# Создаем директорию для шаблонов
RUN mkdir -p /app/templates

# Копируем файлы приложения
COPY . /app/

CMD ["/start.sh"]

