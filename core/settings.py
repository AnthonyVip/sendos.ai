import os
from enum import Enum
from functools import lru_cache
from typing import List, Optional, Tuple

from dotenv import load_dotenv
from pydantic import SecretStr
from pydantic_settings import BaseSettings

load_dotenv()


class EnvironmentEnum(str, Enum):
    production = "production"
    local = "local"
    devel = "devel"


class GlobalConfig(BaseSettings):
    title: str = "Celes API"
    docs_url: str = "/docs"
    description: str = "This is the Sendos API"
    version: str = "1.0.0"
    openapi_url: str = "/openapi.json"
    redoc_url: str = "/redoc"
    api_prefix: str = "/api"
    openapi_prefix: str = os.environ.get("OPENAPI_PREFIX")
    secret_key: SecretStr = os.environ.get("SECRET_KEY")
    allowed_hosts: List[str] = ["*"]
    loggers: Tuple[str, str] = ("uvicorn.asgi", "uvicorn.access")
    environment: EnvironmentEnum
    debug: bool = False
    timezone: str = "UTC"
    jwt_subject: str = os.environ.get("JWT_SUBJECT")
    algorithm: str = os.environ.get("ALGORITHM")
    access_token_expire_minutes: int = os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES")  # noqa: E501

    postgres_user: str = os.environ.get("POSTGRES_USER")
    postgres_password: str = os.environ.get("POSTGRES_PASSWORD")
    postgres_port: int = int(os.environ.get("POSTGRES_PORT"))
    postgres_server: str = os.environ.get("POSTGRES_SERVER")
    postgres_db: str = os.environ.get("POSTGRES_DB")

    @property
    def database_url(self) -> str:
        return (
            "postgresql+asyncpg://"
            f"{self.postgres_user}:{self.postgres_password}@"
            f"{self.postgres_server}:{self.postgres_port}/"
            f"{self.postgres_db}"
        )

    class Config:
        case_sensitive = True


class LocalConfig(GlobalConfig):
    debug: bool = True
    environment: EnvironmentEnum = EnvironmentEnum.local


class DevelConfig(GlobalConfig):
    debug: bool = True
    environment: EnvironmentEnum = EnvironmentEnum.devel


class ProdConfig(GlobalConfig):
    debug: bool = False
    environment: EnvironmentEnum = EnvironmentEnum.production


class FactoryConfig:
    def __init__(self, environment: Optional[str]):
        self.environment = environment
        self.configurations_maps = {
            EnvironmentEnum.local.value: LocalConfig,
            EnvironmentEnum.devel.value: DevelConfig,
            EnvironmentEnum.production.value: ProdConfig,
        }

    def __call__(self) -> GlobalConfig:
        return self.configurations_maps[self.environment]()


@lru_cache()
def get_configuration() -> GlobalConfig:
    try:
        return FactoryConfig(os.environ.get("ENVIRONMENT"))()
    except KeyError:
        return FactoryConfig("local")()


settings = get_configuration()
