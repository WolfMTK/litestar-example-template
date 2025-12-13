import os
import tomllib
from dataclasses import dataclass
from typing import Any

from app.exceptions import ConfigParseError


@dataclass
class DatabaseConfig:
    url: str


@dataclass
class ApplicationConfig:
    debug: bool
    db: DatabaseConfig


def _get_path_config() -> str:
    if not (value := os.getenv("BASE_CONFIG")):
        raise ConfigParseError("Not found path to config.toml")
    return value


def _get_data(path: str) -> dict[str, Any]:
    with open(path, mode="rb") as file:
        return tomllib.load(file)


def load_config() -> ApplicationConfig:
    path_config = _get_path_config()
    data = _get_data(path_config)
    return ApplicationConfig(
        **data.get("application"),
        db=DatabaseConfig(**data.get("database"))
    )
