class DomainException(Exception):
    """Base exception for domain layer"""
    pass

class ValidationError(DomainException):
    """Raised when validation fails"""
    pass

class EntityNotFoundError(DomainException):
    """Raised when an entity is not found"""
    pass

class DuplicateEntityError(DomainException):
    """Raised when trying to create a duplicate entity"""
    pass

class InvalidOperationError(DomainException):
    """Raised when an operation is invalid for the current state"""
    pass

class FileOperationError(DomainException):
    """Raised when a file operation fails"""
    pass

class QRCodeGenerationError(DomainException):
    """Raised when QR code generation fails"""
    pass

class ImageProcessingError(DomainException):
    """Raised when image processing fails"""
    pass 