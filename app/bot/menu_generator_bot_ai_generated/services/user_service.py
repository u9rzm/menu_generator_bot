import aiohttp
import logging
import os

API_URL = os.getenv("API_URL")
logger = logging.getLogger(__name__)

async def register_user(user_id: int) -> bool:
    try:
        async with aiohttp.ClientSession() as session:
            url = f"{API_URL}/register_user?tid={user_id}"
            async with session.post(url) as resp:
                if resp.status == 200:
                    return True
                logger.error(f"Register failed: {await resp.text()}")
    except Exception as e:
        logger.error(f"Register exception: {e}")
    return False
