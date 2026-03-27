from dishka.integrations.fastapi import FromDishka, inject
from fastapi import HTTPException, Security, status
from fastapi.security.api_key import APIKeyHeader

from src.core.config import Settings

api_key_scheme = APIKeyHeader(name="X-API-KEY", auto_error=True)


@inject
async def verify_api_key(*, api_key: str = Security(api_key_scheme), settings: FromDishka[Settings]) -> str:
    if api_key != settings.STATIC_API_KEY.get_secret_value():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key",
        )

    return api_key
