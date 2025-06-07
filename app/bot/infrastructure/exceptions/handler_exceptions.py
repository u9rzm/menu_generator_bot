class HandlerException(Exception):
    """Base exception for handler errors"""
    pass

class ValidationError(HandlerException):
    """Exception for validation errors"""
    pass

class APIError(HandlerException):
    """Exception for API errors"""
    pass

class FileError(HandlerException):
    """Exception for file handling errors"""
    pass

class StateError(HandlerException):
    """Exception for state management errors"""
    pass

class CallbackError(HandlerException):
    """Exception for callback handling errors"""
    pass

class PermissionError(HandlerException):
    """Exception for permission errors"""
    pass

class ConfigurationError(HandlerException):
    """Exception for configuration errors"""
    pass 