# pip install python-dotenv
import os
from dataclasses import dataclass, field

from dotenv import load_dotenv

from app.logger import log

load_dotenv()

@dataclass
class RedisConfig:
    HOST: str = 'localhost'
    PORT: int = 6379

@dataclass
class DatabaseConfig:
    HOST: str = "localhost"
    USER_NAME: str = "user"
    PASSWORD: str = "password"
    DB_NAME: str = "test_legprom"



@dataclass
class TokenConfig:
    SECRET: str = os.getenv("JWT_SECRET")
    ALGORITHM: str = os.getenv("JWT_ALGORITHM")


@dataclass
class PasswordHashConfig:
    SALT: bytes = os.getenv("PWD_SALT")
    ITERATIONS: int = int(os.getenv("PWD_ITERATIONS"))
    ALGORITHM: str = os.getenv("PWD_ALGORITHM")


@dataclass
class BaseConfig:
    password: PasswordHashConfig = field(default_factory=PasswordHashConfig)
    token: TokenConfig = field(default_factory=TokenConfig)
    db: DatabaseConfig = field(default_factory=DatabaseConfig)
    redis: RedisConfig = field(default_factory=RedisConfig)


@dataclass
class ProdConfig(BaseConfig):
    db: DatabaseConfig = field(default_factory=lambda: DatabaseConfig(
        HOST="mysql",
        DB_NAME= "internet_lab"
    ))
    redis: RedisConfig = field(default_factory=lambda: RedisConfig(
        HOST="redis"))


if os.environ.get("FASTAPI_ENV") == "production":
    config = ProdConfig()
    log.info(f'Загружена конфигурация {os.environ.get("FASTAPI_ENV")}')
else:
    config = BaseConfig()
