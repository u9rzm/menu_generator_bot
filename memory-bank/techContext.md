# Technical Context

## Technology Stack
### Core Technologies
- Python 3.11+
- FastAPI 0.115.x
- Aiogram 3.3.0
- SQLAlchemy 2.0.x
- PostgreSQL
- Docker
- Nginx

### Development Tools
- Poetry for dependency management
- Docker Compose for local development
- Git for version control

## Development Setup
1. Environment Requirements
   - Python 3.11 or higher
   - Docker and Docker Compose
   - Poetry package manager

2. Dependencies
   ```toml
   python = ">=3.11"
   fastapi = ">=0.115.12,<0.116.0"
   python-dotenv = ">=1.1.0,<2.0.0"
   uvicorn = ">=0.34.2,<0.35.0"
   sqlalchemy = ">=2.0.40,<3.0.0"
   jinja2 = ">=3.1.3,<4.0.0"
   aiogram = "3.3.0"
   asyncpg = "^0.29.0"
   aiohttp = "^3.9.3"
   pillow = "^11.2.1"
   ```

## Technical Constraints
1. Python Version
   - Minimum: 3.11
   - Maximum: Latest 3.x

2. Database
   - PostgreSQL required
   - Async driver (asyncpg)

3. API
   - RESTful endpoints
   - Async operations
   - OpenAPI documentation

4. Bot
   - Telegram Bot API
   - Async message handling
   - State management

## Deployment Requirements
1. Docker Environment
   - Container orchestration
   - Volume management
   - Network configuration

2. Nginx Configuration
   - Reverse proxy setup
   - SSL/TLS termination
   - Static file serving

3. Database
   - Persistent storage
   - Backup strategy
   - Migration management

## Development Workflow
1. Local Development
   - Poetry for dependency management
   - Docker Compose for services
   - Hot-reload for development

2. Testing
   - Unit tests
   - Integration tests
   - API tests

3. Deployment
   - Docker image building
   - Container orchestration
   - Environment configuration 