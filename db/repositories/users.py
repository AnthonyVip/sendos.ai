from fastapi import HTTPException
from fastapi import status as http_status
from sqlmodel import select, create_engine
from sqlalchemy.exc import IntegrityError
from sqlmodel.ext.asyncio.session import AsyncSession

from db.tables.users import User
from schemas.users import UserCreate, UserRead
from modules.passwords import PasswordEncrypt
from core.settings import settings


engine = create_engine(settings.database_url, echo=True)


helper_password = PasswordEncrypt()


class UsersRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user: UserCreate) -> UserRead:
        db_user = User.model_validate(user)

        try:
            self.session.add(db_user)
            await self.session.commit()
            await self.session.refresh(db_user)

        except IntegrityError:
            raise HTTPException(
                status_code=http_status.HTTP_409_CONFLICT,
                detail="User already exists",
            )

        return db_user

    async def login(self, user: UserCreate) -> UserRead:
        db_user = await self.session.exec(
            select(User).where(User.email == user.email)
        )

        db_user = db_user.first()

        if not db_user:
            raise HTTPException(
                status_code=http_status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
            )

        if not helper_password.verify_password(
            password=user.password,
            hash=db_user.password
        ):
            raise HTTPException(
                status_code=http_status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
            )

        return db_user
