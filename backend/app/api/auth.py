from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from jose import jwt

from app.config import get_settings

security = HTTPBasic()


def create_access_token(username: str) -> str:
    settings = get_settings()
    expire = datetime.now(timezone.utc) + timedelta(hours=12)
    payload = {"sub": username, "exp": expire}
    return jwt.encode(payload, settings.secret_key, algorithm="HS256")


def verify_credentials(credentials: HTTPBasicCredentials = Depends(security)) -> str:
    settings = get_settings()
    if (
        credentials.username == settings.demo_username
        and credentials.password == settings.demo_password
    ):
        return credentials.username
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Identifiants invalides",
        headers={"WWW-Authenticate": "Basic"},
    )
