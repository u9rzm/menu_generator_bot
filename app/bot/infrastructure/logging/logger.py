import os
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime

class Logger:
    """Logger for bot operations"""
    
    def __init__(self, name: str = "bot"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # Create logs directory if it doesn't exist
        os.makedirs("logs", exist_ok=True)
        
        # Create file handler
        log_file = f"logs/{name}_{datetime.now().strftime('%Y%m%d')}.log"
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        file_handler.setLevel(logging.INFO)
        
        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add handlers to logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        
    def info(self, message: str):
        """Log info message"""
        self.logger.info(message)
        
    def error(self, message: str):
        """Log error message"""
        self.logger.error(message)
        
    def warning(self, message: str):
        """Log warning message"""
        self.logger.warning(message)
        
    def debug(self, message: str):
        """Log debug message"""
        self.logger.debug(message)
        
    def critical(self, message: str):
        """Log critical message"""
        self.logger.critical(message) 