from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.config import settings

# Two separate scheme instances — Swagger treats them as independent locks
catalogue_bearer = HTTPBearer(scheme_name="CatalogueToken")
admin_bearer = HTTPBearer(scheme_name="AdminKey")

def create_access_token(email: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": email, "exp": expire}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

def decode_access_token(token: str) -> str:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        email: str = payload.get("sub")
        if not email:
            raise HTTPException(status_code=401, detail="Invalid token")
        return email
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

def require_catalogue_access(
    credentials: HTTPAuthorizationCredentials = Security(catalogue_bearer)
) -> str:
    return decode_access_token(credentials.credentials)

def require_admin(
    credentials: HTTPAuthorizationCredentials = Security(admin_bearer)
):
    if credentials.credentials != settings.ADMIN_API_KEY:
        raise HTTPException(status_code=403, detail="Admin access required")