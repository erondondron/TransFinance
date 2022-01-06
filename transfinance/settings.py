from enum import Enum
from pathlib import Path
from typing import Dict, Any, TypeVar, Optional, Type

import yaml

CONFIG_PATH = Path("config.yaml")
FIELD_TYPE = TypeVar("FIELD_TYPE")


class ConfigFields(Enum):
    TINKOFF_MARKET_TOKEN = "Токен Тинькофф (биржа)"
    TINKOFF_SANDBOX_TOKEN = "Токен Тинькофф (песочница)"

    WORKING_DIRECTORY = "Рабочая директория"


def extract_config_field(
    configuration: Dict[str, Any],
    field: ConfigFields,
    dtype: Type[FIELD_TYPE] = str,
    default: Optional[FIELD_TYPE] = None,
) -> FIELD_TYPE:
    value = configuration.get(field.value)
    if value is None:
        if default is not None:
            value = default
        else:
            raise ValueError(
                f"Необходимо задать параметр {field} в конфигурационном файле"
            )
    if not isinstance(value, dtype):
        try:
            value = dtype(value)
        except Exception:
            raise TypeError(
                f"Неверный тип данных для пераметра {field} "
                f"в конфигурационном файле"
            )
    return value


with open(CONFIG_PATH, "r", encoding="utf-8") as file:
    config = yaml.safe_load(file)


class Settings:
    TINKOFF_MARKET_TOKEN: str = extract_config_field(
        config, ConfigFields.TINKOFF_MARKET_TOKEN
    )
    TINKOFF_SANDBOX_TOKEN: str = extract_config_field(
        config, ConfigFields.TINKOFF_SANDBOX_TOKEN
    )
    WORKING_DIRECTORY: Path = extract_config_field(
        config, ConfigFields.WORKING_DIRECTORY, Path, Path("userdata")
    )
    FIGI_FILE: Path = WORKING_DIRECTORY.joinpath("figi_file.txt")


Settings.WORKING_DIRECTORY.mkdir(parents=True, exist_ok=True)
