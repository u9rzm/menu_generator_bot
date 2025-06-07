import os
import logging
import json
from datetime import datetime
from typing import Optional, Dict, Any
from app.bot.infrastructure.config.config import settings
from app.bot.infrastructure.utils.error_utils import get_error_details

def setup_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """Setup logger"""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger

def get_log_file_path() -> str:
    """Get log file path"""
    # Create logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)
    
    # Create log file name with current date
    current_date = datetime.now().strftime("%Y-%m-%d")
    return f"logs/bot_{current_date}.log"

def log_user_action(logger: logging.Logger, user_id: int, action: str, data: Optional[Dict[str, Any]] = None) -> None:
    """Log user action"""
    log_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "user_id": user_id,
        "action": action,
        "data": data or {}
    }
    logger.info(json.dumps(log_data))

def log_error(logger: logging.Logger, error: Exception, context: Optional[Dict[str, Any]] = None) -> None:
    """Log error"""
    error_details = get_error_details(error)
    log_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "error": error_details,
        "context": context or {}
    }
    logger.error(json.dumps(log_data))

def log_info(logger: logging.Logger, message: str, data: Optional[Dict[str, Any]] = None) -> None:
    """Log info"""
    log_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "message": message,
        "data": data or {}
    }
    logger.info(json.dumps(log_data))

def log_warning(logger: logging.Logger, message: str, data: Optional[Dict[str, Any]] = None) -> None:
    """Log warning"""
    log_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "message": message,
        "data": data or {}
    }
    logger.warning(json.dumps(log_data))

def log_debug(logger: logging.Logger, message: str, data: Optional[Dict[str, Any]] = None) -> None:
    """Log debug"""
    log_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "message": message,
        "data": data or {}
    }
    logger.debug(json.dumps(log_data))

def log_api_request(logger: logging.Logger, method: str, url: str, data: Optional[Dict[str, Any]] = None) -> None:
    """Log API request"""
    log_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "method": method,
        "url": url,
        "data": data or {}
    }
    logger.info(json.dumps(log_data))

def log_api_response(logger: logging.Logger, status_code: int, data: Optional[Dict[str, Any]] = None) -> None:
    """Log API response"""
    log_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "status_code": status_code,
        "data": data or {}
    }
    logger.info(json.dumps(log_data))

def log_bot_action(logger: logging.Logger, action: str, data: Optional[Dict[str, Any]] = None) -> None:
    """Log bot action"""
    log_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "action": action,
        "data": data or {}
    }
    logger.info(json.dumps(log_data))

def log_state_change(logger: logging.Logger, user_id: int, old_state: str, new_state: str) -> None:
    """Log state change"""
    log_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "user_id": user_id,
        "old_state": old_state,
        "new_state": new_state
    }
    logger.info(json.dumps(log_data))

def log_file_operation(logger: logging.Logger, operation: str, file_path: str, data: Optional[Dict[str, Any]] = None) -> None:
    """Log file operation"""
    log_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "operation": operation,
        "file_path": file_path,
        "data": data or {}
    }
    logger.info(json.dumps(log_data))

def log_validation(logger: logging.Logger, entity: str, data: Dict[str, Any], errors: Optional[Dict[str, Any]] = None) -> None:
    """Log validation"""
    log_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "entity": entity,
        "data": data,
        "errors": errors or {}
    }
    logger.info(json.dumps(log_data))

def log_callback(
    logger: logging.Logger,
    callback_data: str,
    chat_id: int,
    user_id: int,
    username: Optional[str]
) -> None:
    """Log callback query"""
    log_message = f"Callback: {callback_data} - Chat: {chat_id}, User: {user_id}"
    if username:
        log_message += f" (@{username})"
    logger.debug(log_message) 