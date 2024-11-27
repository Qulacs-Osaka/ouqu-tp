from os import getenv
from typing import Any


def get_config(key: str, default_value: Any) -> Any:
    return getenv(key, default_value)


# ログ


def get_config_LOG_FORMAT(default_value: str) -> str:
    return str(get_config("LOG_FORMAT", default_value))


def get_config_LOG_LEVEL(default_value: int) -> int:
    return int(get_config("LOG_LEVEL", default_value))


def get_config_LOG_PATH(default_value: str) -> str:
    return str(get_config("LOG_PATH", default_value))


# PORT


def get_config_PORT(default_value: int) -> int:
    return int(get_config("PORT", default_value))


# 一時ファイルの削除フラグ: Trueの場合、削除する


def get_config_DELETE_TMP_FLG() -> bool:
    return str(get_config("DELETE_TMP_FLG", "FALSE")).upper() == "TRUE"
