FROM python:3.12.1-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt update -y && \
    apt install -y python3-dev

RUN pip install --upgrade pip
RUN pip install poetry
ADD pyproject.toml .
RUN poetry config virtualenvs.create false
# RUN poetry add fastapi
RUN poetry install --no-root --no-interaction --no-ansi

# Устанавливаем watchdog для автоперезагрузки
RUN pip install watchdog

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f ${API_URL}/health || exit 1

# Запускаем бота с автоперезагрузкой
CMD ["watchmedo", "auto-restart", "--directory=/app", "--pattern=*.py", "--recursive", "--", "python", "bot.py"]