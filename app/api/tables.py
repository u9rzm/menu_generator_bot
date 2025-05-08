from sqlalchemy import inspect, text
from sqlalchemy.orm import Session
from typing import Dict, Any
import logging
import traceback
from fastapi import HTTPException

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_table_info(db: Session) -> Dict[str, Any]:
    """Get information about all tables in the database"""
    try:
        logger.info("Starting get_table_info")
        # Получаем engine из сессии
        engine = db.get_bind()
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        logger.info(f"Found tables: {tables}")
        
        result = {}
        for table in tables:
            try:
                # Get table structure
                columns = inspector.get_columns(table)
                column_info = [{"name": col["name"], "type": str(col["type"])} for col in columns]
                logger.info(f"Got structure for table {table}")
                
                # Get row count
                row_count = db.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar()
                logger.info(f"Got row count for table {table}: {row_count}")
                
                # Get sample data (first 5 rows)
                sample_data = db.execute(text(f"SELECT * FROM {table} LIMIT 5")).fetchall()
                logger.info(f"Got sample data for table {table}")
                
                result[table] = {
                    "structure": column_info,
                    "row_count": row_count,
                    "sample_data": [dict(row) for row in sample_data]
                }
            except Exception as e:
                logger.error(f"Error processing table {table}: {str(e)}")
                logger.error(traceback.format_exc())
                result[table] = {
                    "error": str(e),
                    "traceback": traceback.format_exc()
                }
        
        return result
    except Exception as e:
        logger.error(f"Error in get_table_info: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

def get_table_structure(db: Session, table_name: str) -> Dict[str, Any]:
    """Get structure of a specific table"""
    try:
        logger.info(f"Getting structure for table {table_name}")
        engine = db.get_bind()
        inspector = inspect(engine)
        
        if table_name not in inspector.get_table_names():
            raise HTTPException(status_code=404, detail=f"Table {table_name} not found")
        
        columns = inspector.get_columns(table_name)
        return {
            "table_name": table_name,
            "columns": [{"name": col["name"], "type": str(col["type"])} for col in columns]
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting table structure: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))

def get_table_data(db: Session, table_name: str, limit: int = 5) -> Dict[str, Any]:
    """Get data from a specific table"""
    try:
        logger.info(f"Getting data from table {table_name}")
        engine = db.get_bind()
        inspector = inspect(engine)
        
        if table_name not in inspector.get_table_names():
            raise HTTPException(status_code=404, detail=f"Table {table_name} not found")
        
        # Get row count
        row_count = db.execute(text(f"SELECT COUNT(*) FROM {table_name}")).scalar()
        
        # Get sample data
        sample_data = db.execute(text(f"SELECT * FROM {table_name} LIMIT {limit}")).fetchall()
        
        return {
            "table_name": table_name,
            "row_count": row_count,
            "sample_data": [dict(row) for row in sample_data]
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting table data: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e)) 