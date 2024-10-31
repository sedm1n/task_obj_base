import logging
from dataclasses import dataclass

from environs import Env

format = "%(asctime)s - %(levelname)s - %(module)s - %(message)s"

logging.basicConfig(level=logging.DEBUG, format=format, filename="app.log")



@dataclass
class DatabaseConfig:
    host: str
    port: int 
    database: str
    user: str
    password: str


@dataclass
class AppConfig:
    database: DatabaseConfig


def load_config() -> AppConfig:
    """"
    Load config from .env
    """
    env = Env()
    env.read_env()
    return AppConfig(
        database=DatabaseConfig(
            host=env("DB_HOST"),
            port=env.int("DB_PORT"),
            database=env("DB_NAME"),
            user=env("DB_USER"),
            password=env("DB_PASSWORD"),
        )
    )