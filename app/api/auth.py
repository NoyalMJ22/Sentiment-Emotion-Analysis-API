from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
from app.core.config import settings
from app.core.logger import logger

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

async def get_api_key(api_key_header: str = Security(api_key_header)):
    """
    Dependency that checks the X-API-Key header against the settings.
    """
    if api_key_header == settings.API_KEY:
        return api_key_header
        
    logger.warning("Failed authentication attempt!")
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing X-API-Key header",
    )
