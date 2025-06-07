 # Menu Generator Bot

Telegram бот для создания и управления меню ресторанов и кафе.

## Текущая функциональность

- Базовый функционал бота
- Обработка команд и сообщений
- Управление состояниями
- Логирование действий
- Обработка ошибок



## Технологии

- Python 3.11+
- aiogram 3.x
- SQLAlchemy
- FastAPI
- PostgreSQL
- Pydantic
- Alembic

## Установка и запуск

1. Клонируйте репозиторий:
```bash
git clone https://github.com/u9rzm/menu_generator_bot.git
cd menu_generator_bot
```

2. Установите зависимости:
```bash
poetry install
```

3. Создайте файл .env с необходимыми переменными окружения:
```env
BOT_TOKEN=your_telegram_bot_token
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
```

4. Примените миграции:
```bash
alembic upgrade head
```

5. Запустите бота:
```bash
python -m app.bot.infrastructure.bot.main
```



## Лицензия

MIT License

## Авторы

- TitanPillow
