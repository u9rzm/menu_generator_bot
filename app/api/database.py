from sqlalchemy import MetaData, create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.exc import SQLAlchemyError, OperationalError
from contextlib import contextmanager
import os
import time
import logging
import traceback
from typing import Generator

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_db_engine_with_retry(max_retries: int = 5, retry_delay: int = 5):
    """Create database engine with retry mechanism"""
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        logger.error("DATABASE_URL environment variable is not set")
        raise ValueError("DATABASE_URL environment variable is not set")

    logger.info(f"Connecting to database at {DATABASE_URL}")

    for attempt in range(max_retries):
        try:
            logger.info(f"Attempting to create database engine (attempt {attempt + 1}/{max_retries})")
            engine = create_engine(
                DATABASE_URL,
                pool_size=5,
                max_overflow=10,
                pool_timeout=30,
                pool_recycle=1800,
                echo=True  # Enable SQL query logging
            )
            
            # Test the connection
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            logger.info("Database connection successful")
            return engine
            
        except OperationalError as e:
            logger.error(f"Database connection error (attempt {attempt + 1}/{max_retries}): {e}")
            logger.error(traceback.format_exc())
            if attempt < max_retries - 1:
                logger.info(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                logger.error("Max retries reached. Could not connect to database.")
                raise
        except Exception as e:
            logger.error(f"Unexpected error during database connection: {e}")
            logger.error(traceback.format_exc())
            raise

# Create engine with connection pool settings
engine = create_db_engine_with_retry()

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Create base class for models
Base = declarative_base()
metadata = MetaData()

def init_db() -> None:
    """Initialize database by creating all tables"""
    max_retries = 5
    retry_delay = 5
    
    for attempt in range(max_retries):
        try:
            logger.info(f"Attempting to create database tables (attempt {attempt + 1}/{max_retries})")
            Base.metadata.create_all(bind=engine)
            logger.info("Database tables created successfully")
            return
        except SQLAlchemyError as e:
            logger.error(f"Error creating database tables (attempt {attempt + 1}/{max_retries}): {e}")
            logger.error(traceback.format_exc())
            if attempt < max_retries - 1:
                logger.info(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
            else:
                logger.error("Max retries reached. Could not create database tables.")
                raise

@contextmanager
def get_db() -> Generator[Session, None, None]:
    """Context manager for database sessions"""
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error: {e}")
        logger.error(traceback.format_exc())
        raise
    finally:
        db.close()

def get_db_session() -> Session:
    """Get database session without context manager"""
    return SessionLocal()

