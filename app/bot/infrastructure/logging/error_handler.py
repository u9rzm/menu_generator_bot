import functools
from typing import Callable, Any
from ...domain.exceptions import DomainException
from .logger import Logger

logger = Logger()

def log_errors(func: Callable) -> Callable:
    """Decorator for logging errors in async functions"""
    @functools.wraps(func)
    async def wrapper(*args, **kwargs) -> Any:
        try:
            return await func(*args, **kwargs)
        except DomainException as e:
            logger.error(
                f"Domain error in {func.__name__}: {str(e)}",
                extra={
                    'function': func.__name__,
                    'error_type': type(e).__name__,
                    'args': args,
                    'kwargs': kwargs
                }
            )
            raise
        except Exception as e:
            logger.exception(
                f"Unexpected error in {func.__name__}: {str(e)}",
                extra={
                    'function': func.__name__,
                    'error_type': type(e).__name__,
                    'args': args,
                    'kwargs': kwargs
                }
            )
            raise

    return wrapper

def log_sync_errors(func: Callable) -> Callable:
    """Decorator for logging errors in synchronous functions"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        try:
            return func(*args, **kwargs)
        except DomainException as e:
            logger.error(
                f"Domain error in {func.__name__}: {str(e)}",
                extra={
                    'function': func.__name__,
                    'error_type': type(e).__name__,
                    'args': args,
                    'kwargs': kwargs
                }
            )
            raise
        except Exception as e:
            logger.exception(
                f"Unexpected error in {func.__name__}: {str(e)}",
                extra={
                    'function': func.__name__,
                    'error_type': type(e).__name__,
                    'args': args,
                    'kwargs': kwargs
                }
            )
            raise

    return wrapper 