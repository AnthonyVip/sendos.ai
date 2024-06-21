from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from modules.token import Token


token = Token()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(HTTPBearer())
):
    if not credentials.scheme == "Bearer":
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication scheme."
        )
    if not credentials.credentials:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials."
        )

    return token.verify_access_token(credentials.credentials)
