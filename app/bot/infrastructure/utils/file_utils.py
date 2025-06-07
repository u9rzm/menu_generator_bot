import os
import aiofiles
from typing import Optional, Dict, Any, List
from app.bot.infrastructure.config.config import settings
from app.bot.infrastructure.exceptions.handler_exceptions import FileError

async def save_file(
    file_path: str,
    content: bytes,
    mode: str = "wb"
) -> None:
    """Save file"""
    try:
        async with aiofiles.open(file_path, mode) as f:
            await f.write(content)
    except Exception as e:
        raise FileError(f"Failed to save file: {str(e)}")

async def read_file(
    file_path: str,
    mode: str = "rb"
) -> bytes:
    """Read file"""
    try:
        async with aiofiles.open(file_path, mode) as f:
            return await f.read()
    except Exception as e:
        raise FileError(f"Failed to read file: {str(e)}")

def get_file_extension(file_path: str) -> str:
    """Get file extension"""
    return os.path.splitext(file_path)[1].lower()

def is_valid_image_type(file_path: str) -> bool:
    """Check if file is a valid image type"""
    extension = get_file_extension(file_path)
    return extension in settings.ALLOWED_IMAGE_TYPES

def is_valid_menu_type(file_path: str) -> bool:
    """Check if file is a valid menu type"""
    extension = get_file_extension(file_path)
    return extension in settings.ALLOWED_MENU_TYPES

def is_valid_file_size(file_path: str) -> bool:
    """Check if file size is valid"""
    try:
        size = os.path.getsize(file_path)
        return size <= settings.MAX_FILE_SIZE
    except Exception as e:
        raise FileError(f"Failed to get file size: {str(e)}")

def get_temp_file_path(
    file_name: str,
    extension: Optional[str] = None
) -> str:
    """Get temporary file path"""
    if extension:
        file_name = f"{file_name}.{extension}"
    return os.path.join(settings.TEMP_DIR, file_name)

def ensure_temp_dir() -> None:
    """Ensure temporary directory exists"""
    try:
        os.makedirs(settings.TEMP_DIR, exist_ok=True)
    except Exception as e:
        raise FileError(f"Failed to create temporary directory: {str(e)}")

def cleanup_temp_files() -> None:
    """Clean up temporary files"""
    try:
        for file_name in os.listdir(settings.TEMP_DIR):
            file_path = os.path.join(settings.TEMP_DIR, file_name)
            try:
                os.remove(file_path)
            except Exception:
                pass
    except Exception as e:
        raise FileError(f"Failed to clean up temporary files: {str(e)}")

def get_file_size(file_path: str) -> int:
    """Get file size"""
    try:
        return os.path.getsize(file_path)
    except Exception as e:
        raise FileError(f"Failed to get file size: {str(e)}")

def get_file_type(file_path: str) -> str:
    """Get file type"""
    extension = get_file_extension(file_path)
    if extension in settings.ALLOWED_IMAGE_TYPES:
        return "image"
    elif extension in settings.ALLOWED_MENU_TYPES:
        return "menu"
    else:
        return "unknown"

def get_file_name(file_path: str) -> str:
    """Get file name"""
    return os.path.basename(file_path)

def get_file_dir(file_path: str) -> str:
    """Get file directory"""
    return os.path.dirname(file_path)

def get_file_path(
    directory: str,
    file_name: str,
    extension: Optional[str] = None
) -> str:
    """Get file path"""
    if extension:
        file_name = f"{file_name}.{extension}"
    return os.path.join(directory, file_name)

def ensure_dir(directory: str) -> None:
    """Ensure directory exists"""
    try:
        os.makedirs(directory, exist_ok=True)
    except Exception as e:
        raise FileError(f"Failed to create directory: {str(e)}")

def is_file_exists(file_path: str) -> bool:
    """Check if file exists"""
    return os.path.isfile(file_path)

def is_dir_exists(directory: str) -> bool:
    """Check if directory exists"""
    return os.path.isdir(directory)

def list_files(
    directory: str,
    extension: Optional[str] = None
) -> List[str]:
    """List files in directory"""
    try:
        files = []
        for file_name in os.listdir(directory):
            if extension:
                if file_name.endswith(extension):
                    files.append(file_name)
            else:
                files.append(file_name)
        return files
    except Exception as e:
        raise FileError(f"Failed to list files: {str(e)}")

def list_dirs(directory: str) -> List[str]:
    """List directories in directory"""
    try:
        return [
            d for d in os.listdir(directory)
            if os.path.isdir(os.path.join(directory, d))
        ]
    except Exception as e:
        raise FileError(f"Failed to list directories: {str(e)}")

def move_file(
    source_path: str,
    target_path: str
) -> None:
    """Move file"""
    try:
        os.rename(source_path, target_path)
    except Exception as e:
        raise FileError(f"Failed to move file: {str(e)}")

def copy_file(
    source_path: str,
    target_path: str
) -> None:
    """Copy file"""
    try:
        with open(source_path, "rb") as source:
            with open(target_path, "wb") as target:
                target.write(source.read())
    except Exception as e:
        raise FileError(f"Failed to copy file: {str(e)}")

def delete_file(file_path: str) -> None:
    """Delete file"""
    try:
        os.remove(file_path)
    except Exception as e:
        raise FileError(f"Failed to delete file: {str(e)}")

def delete_dir(directory: str) -> None:
    """Delete directory"""
    try:
        os.rmdir(directory)
    except Exception as e:
        raise FileError(f"Failed to delete directory: {str(e)}")

def get_file_info(file_path: str) -> Dict[str, Any]:
    """Get file info"""
    try:
        stat = os.stat(file_path)
        return {
            "size": stat.st_size,
            "created": stat.st_ctime,
            "modified": stat.st_mtime,
            "accessed": stat.st_atime,
            "mode": stat.st_mode,
            "uid": stat.st_uid,
            "gid": stat.st_gid
        }
    except Exception as e:
        raise FileError(f"Failed to get file info: {str(e)}")

def get_dir_info(directory: str) -> Dict[str, Any]:
    """Get directory info"""
    try:
        stat = os.stat(directory)
        return {
            "created": stat.st_ctime,
            "modified": stat.st_mtime,
            "accessed": stat.st_atime,
            "mode": stat.st_mode,
            "uid": stat.st_uid,
            "gid": stat.st_gid
        }
    except Exception as e:
        raise FileError(f"Failed to get directory info: {str(e)}")

def get_file_permissions(file_path: str) -> int:
    """Get file permissions"""
    try:
        return os.stat(file_path).st_mode & 0o777
    except Exception as e:
        raise FileError(f"Failed to get file permissions: {str(e)}")

def set_file_permissions(
    file_path: str,
    permissions: int
) -> None:
    """Set file permissions"""
    try:
        os.chmod(file_path, permissions)
    except Exception as e:
        raise FileError(f"Failed to set file permissions: {str(e)}")

def get_file_owner(file_path: str) -> Dict[str, int]:
    """Get file owner"""
    try:
        stat = os.stat(file_path)
        return {
            "uid": stat.st_uid,
            "gid": stat.st_gid
        }
    except Exception as e:
        raise FileError(f"Failed to get file owner: {str(e)}")

def set_file_owner(
    file_path: str,
    uid: int,
    gid: int
) -> None:
    """Set file owner"""
    try:
        os.chown(file_path, uid, gid)
    except Exception as e:
        raise FileError(f"Failed to set file owner: {str(e)}")

def get_file_mime_type(file_path: str) -> str:
    """Get file MIME type"""
    import mimetypes
    try:
        return mimetypes.guess_type(file_path)[0] or "application/octet-stream"
    except Exception as e:
        raise FileError(f"Failed to get file MIME type: {str(e)}")

def get_file_hash(file_path: str) -> str:
    """Get file hash"""
    import hashlib
    try:
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except Exception as e:
        raise FileError(f"Failed to get file hash: {str(e)}")

def get_file_checksum(file_path: str) -> str:
    """Get file checksum"""
    import hashlib
    try:
        hash_sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()
    except Exception as e:
        raise FileError(f"Failed to get file checksum: {str(e)}")

def get_file_signature(file_path: str) -> str:
    """Get file signature"""
    import hashlib
    try:
        hash_sha1 = hashlib.sha1()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha1.update(chunk)
        return hash_sha1.hexdigest()
    except Exception as e:
        raise FileError(f"Failed to get file signature: {str(e)}")

def get_file_metadata(file_path: str) -> Dict[str, Any]:
    """Get file metadata"""
    try:
        return {
            "name": get_file_name(file_path),
            "extension": get_file_extension(file_path),
            "size": get_file_size(file_path),
            "type": get_file_type(file_path),
            "mime_type": get_file_mime_type(file_path),
            "hash": get_file_hash(file_path),
            "checksum": get_file_checksum(file_path),
            "signature": get_file_signature(file_path),
            "permissions": get_file_permissions(file_path),
            "owner": get_file_owner(file_path),
            "info": get_file_info(file_path)
        }
    except Exception as e:
        raise FileError(f"Failed to get file metadata: {str(e)}")

def validate_file(
    file_path: str,
    required_type: Optional[str] = None,
    max_size: Optional[int] = None
) -> bool:
    """Validate file"""
    try:
        if not is_file_exists(file_path):
            return False
        
        if required_type:
            if required_type == "image" and not is_valid_image_type(file_path):
                return False
            elif required_type == "menu" and not is_valid_menu_type(file_path):
                return False
        
        if max_size:
            if get_file_size(file_path) > max_size:
                return False
        
        return True
    except Exception as e:
        raise FileError(f"Failed to validate file: {str(e)}")

def ensure_file(
    file_path: str,
    required_type: Optional[str] = None,
    max_size: Optional[int] = None
) -> None:
    """Ensure file is valid"""
    if not validate_file(file_path, required_type, max_size):
        raise FileError("Invalid file") 