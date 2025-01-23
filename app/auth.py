from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.consts import SECRET_TOKEN
security = HTTPBearer()

SECRET_TOKEN = SECRET_TOKEN


def validate_token(
        credentials: HTTPAuthorizationCredentials = Security(security)):
    print(SECRET_TOKEN, credentials.credentials)
    if credentials.credentials != SECRET_TOKEN:
        raise HTTPException(
            status_code=403,
            detail="Неверный или отсутствующий токен авторизации"
        )
    return credentials.credentials
