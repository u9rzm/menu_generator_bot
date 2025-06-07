# System Patterns

## Architecture Overview
The system follows a modular architecture with clear separation of concerns:

```
app/
├── api/        # FastAPI endpoints
├── bot/        # Telegram bot implementation
├── generator/  # Content generation logic
├── db/         # Database models and operations
└── static/     # Static file serving
```

## Design Patterns
1. Repository Pattern
   - Database operations abstracted through repositories
   - Clean separation of data access logic

2. Service Layer Pattern
   - Business logic encapsulated in service classes
   - Clear separation between API/bot and business logic

3. Dependency Injection
   - FastAPI dependency injection system
   - Modular and testable components

4. Factory Pattern
   - Object creation abstracted through factories
   - Flexible component instantiation

## Component Relationships
- Bot ↔ API: Shared business logic through services
- API ↔ DB: Data access through repositories
- Generator ↔ API: Content generation services
- Static ↔ API: File serving endpoints

## Technical Decisions
1. FastAPI
   - Modern async framework
   - Built-in OpenAPI documentation
   - Type hints and validation

2. Aiogram 3.x
   - Modern async Telegram bot framework
   - Type-safe development
   - Efficient message handling

3. SQLAlchemy
   - ORM for database operations
   - Migration support
   - Type-safe queries

4. Docker
   - Containerized deployment
   - Environment consistency
   - Easy scaling

## Security Patterns
- Environment variable configuration
- API authentication
- Input validation
- Error handling
- Rate limiting 