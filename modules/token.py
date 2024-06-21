import jwt
from fastapi import HTTPException
from datetime import datetime, timedelta

from core.settings import settings


class Token:
    def __init__(self):
        self.secret_key = settings.secret_key
        self.algorithm = settings.algorithm
        self.subject = settings.jwt_subject
        self.expire_time = settings.access_token_expire_minutes

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=self.expire_time)
        to_encode.update({"exp": expire})
        to_encode.update({"sub": self.subject})
        encoded_jwt = jwt.encode(
            to_encode,
            str(self.secret_key),
            algorithm=self.algorithm
        )
        return encoded_jwt

    def verify_access_token(self, token: str):
        try:
            payload = jwt.decode(
                token,
                str(self.secret_key),
                algorithms=[self.algorithm]
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")
