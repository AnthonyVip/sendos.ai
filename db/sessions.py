from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import create_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from core.settings import settings


engine = create_engine(settings.database_url, echo=False)
async_engine = create_async_engine(settings.database_url, echo=False)


async_session = sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)
