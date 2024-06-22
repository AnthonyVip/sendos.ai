from fastapi import APIRouter, Body, Depends, HTTPException, status

from db.repositories.users import UsersRepository
from routes.dependencies.database import get_repository
from schemas.users import UserCreate, UserResponse
from modules.passwords import PasswordEncrypt
from modules.token import Token


router = APIRouter()


token = Token()


@router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponse
)
async def create_user(
    user: UserCreate = Body(...),
    repository: UsersRepository = Depends(get_repository(UsersRepository)),
):
    _helper_password = PasswordEncrypt()

    if not _helper_password.validated_pass(user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid password"
        )

    user.password = _helper_password.get_password_hash(user.password)

    db_user = await repository.create(user)

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists"
        )

    _token = token.create_access_token(
        data={
            "email": db_user.email,
            "id": str(db_user.id)
        }
    )

    return UserResponse(jwt_token=_token)


@router.post("/login", response_model=UserResponse)
async def login_user(
    user: UserCreate = Body(...),
    repository: UsersRepository = Depends(get_repository(UsersRepository)),
):
    user_db = await repository.login(user)

    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    _token = token.create_access_token(
        data={
            "email": user_db.email,
            "id": str(user_db.id)
        }
    )

    return UserResponse(jwt_token=_token)
