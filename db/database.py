"""Подключение к базе данных SQLite (ПР7)."""

from __future__ import annotations

import sqlite3
from contextlib import closing
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "survey_service.sqlite"


def get_connection() -> sqlite3.Connection:
    """Создать соединение с БД.

    Включает проверку внешних ключей и доступ к полям строк по именам
    (sqlite3.Row). Если файла базы нет, сообщает, как его создать:
    sqlite3.connect() молча создал бы пустой файл без таблиц.
    """
    if not Path(DB_PATH).exists():
        raise FileNotFoundError(
            f"Файл базы данных не найден: {DB_PATH}. "
            "Создайте его командами из README.md (раздел ПР7)."
        )
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def fetch_all(sql: str, params=()) -> list[sqlite3.Row]:
    """Выполнить SELECT и вернуть все строки.

    Значения передаются отдельным списком params и подставляются в
    места ? самой библиотекой sqlite3, а не склеиваются со строкой.
    """
    with closing(get_connection()) as conn:
        return conn.execute(sql, params).fetchall()


def fetch_one(sql: str, params=()) -> sqlite3.Row | None:
    """Выполнить SELECT и вернуть первую строку или None."""
    with closing(get_connection()) as conn:
        return conn.execute(sql, params).fetchone()
