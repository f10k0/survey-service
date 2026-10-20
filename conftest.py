"""Настройка pytest: подключает Django и тестовую базу SQLite."""

import json
import os
import sqlite3

import django
import pytest
from django.test.utils import setup_test_environment

import db.database

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "survey_service.settings")
django.setup()
setup_test_environment()


def make_database(path):
    """Создать файл БД со схемой из sql/schema.sql."""
    schema = (db.database.BASE_DIR / "sql" / "schema.sql").read_text(
        encoding="utf-8")
    conn = sqlite3.connect(path)
    conn.executescript(schema)
    conn.commit()
    conn.close()


@pytest.fixture
def empty_db(tmp_path, monkeypatch):
    """Пустая БД со схемой; views и db.database работают с ней."""
    path = tmp_path / "test.sqlite"
    make_database(path)
    monkeypatch.setattr(db.database, "DB_PATH", path)
    return path


@pytest.fixture
def sample_db(empty_db):
    """БД с тестовыми данными (с «опасным» текстом для автоэкранирования).

    Опросы: 1 - активный, 2 - завершённый (без вопросов), 3 - активный.
    Анна ответила на опрос 1 дважды, Борис - один раз, Вера - ни разу.
    """
    conn = sqlite3.connect(empty_db)
    conn.executemany(
        "INSERT INTO users VALUES (?, ?, ?, ?, ?)",
        [(1, "Анна", "a@b.ru", 20, 1),
         (2, "Борис", "b@b.ru", 30, 1),
         (3, "Вера", "v@b.ru", 25, 1)],
    )
    conn.executemany(
        "INSERT INTO surveys VALUES (?, ?, ?, ?, ?)",
        [(1, "Опрос <b>1</b>", "IT", "активен", "2026-09-20"),
         (2, "Второй", "Спорт", "завершён", "2026-09-21"),
         (3, "Третий", "IT", "активен", "2026-09-22")],
    )
    conn.executemany(
        "INSERT INTO questions (survey_id, text, options) VALUES (?, ?, ?)",
        [(1, "Язык?", json.dumps(["Python", "Java"], ensure_ascii=False)),
         (1, "Комментарий", None),
         (3, "Любимый цвет?", json.dumps(["Красный"], ensure_ascii=False))],
    )
    conn.executemany(
        "INSERT INTO responses VALUES (?, ?, ?, ?, ?)",
        [(1, 1, 1, "Язык?", "Python"),
         (2, 1, 1, "Комментарий", "<script>x</script>"),
         (3, 2, 1, "Язык?", "Java")],
    )
    conn.commit()
    conn.close()
    return empty_db


def execute(path, sql, params=()):
    """Выполнить изменяющий запрос в тестовой БД."""
    conn = sqlite3.connect(path)
    conn.execute(sql, params)
    conn.commit()
    conn.close()
