"""Тесты слоя базы данных (ПР7): схема, импорт, запросы, страницы."""

import json
import re
import sqlite3
from pathlib import Path

import pytest
from django.test import Client

import db.database
import db.import_json as import_json
from conftest import execute, make_database
from db.database import fetch_all, fetch_one, get_connection

client = Client()
ROOT = db.database.BASE_DIR


def tables(path):
    conn = sqlite3.connect(path)
    rows = conn.execute(
        "SELECT name FROM sqlite_master WHERE type = 'table'").fetchall()
    conn.close()
    return {row[0] for row in rows}


def count(path, table):
    conn = sqlite3.connect(path)
    result = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
    conn.close()
    return result


def write_json(path, name, data):
    (path / name).write_text(json.dumps(data), encoding="utf-8")


@pytest.fixture
def json_files(tmp_path, monkeypatch):
    """Подменить JSON-файлы, которые читает db/import_json.py."""
    write_json(tmp_path, "users.json", [
        {"id": 1, "name": "Анна", "email": "a@b.ru", "age": 20,
         "is_registered": True},
    ])
    write_json(tmp_path, "surveys.json", [
        {"id": 1, "title": "Опрос", "topic": "IT", "status": "активен",
         "creation_date": "2026-09-20",
         "questions": [{"text": "Q1", "options": ["A", "B"]},
                       {"text": "Q2", "options": None}]},
    ])
    write_json(tmp_path, "responses.json", [
        {"user_email": "a@b.ru", "survey_id": 1, "question": "Q1",
         "answer": "A"},
        {"user_email": "a@b.ru", "survey_id": 1, "question": "Q2",
         "answer": "text"},
    ])
    monkeypatch.setattr(import_json, "USERS_FILE", tmp_path / "users.json")
    monkeypatch.setattr(import_json, "SURVEYS_FILE",
                        tmp_path / "surveys.json")
    monkeypatch.setattr(import_json, "RESPONSES_FILE",
                        tmp_path / "responses.json")
    return tmp_path


# ---------- схема и ключи ----------

def test_schema_creates_tables(empty_db):
    assert tables(empty_db) == {"users", "surveys", "questions",
                                "responses"}


def test_schema_can_be_applied_twice(empty_db):
    """IF NOT EXISTS: повторный запуск схемы не даёт ошибки."""
    make_database(empty_db)
    assert len(tables(empty_db)) == 4


def test_foreign_keys_declared(empty_db):
    conn = get_connection()
    for table, parents in (("responses", {"users", "surveys"}),
                           ("questions", {"surveys"})):
        rows = conn.execute(f"PRAGMA foreign_key_list({table})").fetchall()
        assert {row["table"] for row in rows} == parents
    conn.close()


def test_foreign_keys_are_enforced(empty_db):
    conn = get_connection()
    with pytest.raises(sqlite3.IntegrityError):
        conn.execute(
            "INSERT INTO responses VALUES (1, 99, 99, 'Q', 'A')")
    conn.close()


def test_email_is_unique(sample_db):
    with pytest.raises(sqlite3.IntegrityError):
        execute(sample_db,
                "INSERT INTO users VALUES (9, 'X', 'a@b.ru', 20, 1)")


# ---------- подключение ----------

def test_get_connection_uses_row_factory(sample_db):
    row = fetch_one("SELECT id, title FROM surveys WHERE id = ?", [2])
    assert row["title"] == "Второй" and row["id"] == 2


def test_missing_database_has_clear_error(tmp_path, monkeypatch):
    monkeypatch.setattr(db.database, "DB_PATH", tmp_path / "none.sqlite")
    with pytest.raises(FileNotFoundError, match="README"):
        get_connection()
    assert not (tmp_path / "none.sqlite").exists()


def test_fetch_all_returns_list(sample_db):
    assert len(fetch_all("SELECT * FROM users")) == 3


# ---------- импорт ----------

def test_import_json_moves_all_data(empty_db, json_files):
    import_json.main()
    assert count(empty_db, "users") == 1
    assert count(empty_db, "surveys") == 1
    assert count(empty_db, "questions") == 2
    assert count(empty_db, "responses") == 2


def test_import_assigns_response_ids_by_position(empty_db, json_files):
    import_json.main()
    ids = [r["id"] for r in fetch_all("SELECT id FROM responses")]
    assert ids == [1, 2]


def test_import_converts_options_and_email(empty_db, json_files):
    import_json.main()
    questions = fetch_all("SELECT options FROM questions ORDER BY id")
    assert json.loads(questions[0]["options"]) == ["A", "B"]
    assert questions[1]["options"] is None
    assert fetch_one("SELECT user_id FROM responses")["user_id"] == 1


def test_import_is_repeatable(empty_db, json_files):
    import_json.main()
    import_json.main()
    assert count(empty_db, "responses") == 2
    assert count(empty_db, "questions") == 2


def test_failed_import_rolls_back(empty_db, json_files):
    import_json.main()
    write_json(json_files, "responses.json", [
        {"user_email": "nobody@b.ru", "survey_id": 1, "question": "Q",
         "answer": "A"},
    ])
    with pytest.raises(KeyError):
        import_json.main()
    assert count(empty_db, "responses") == 2


def test_real_json_files_are_imported(empty_db):
    import_json.main()
    for table, filename in (("users", "users.json"),
                            ("surveys", "surveys.json"),
                            ("responses", "responses.json")):
        data = json.loads(
            (ROOT / "data" / filename).read_text(encoding="utf-8"))
        assert count(empty_db, table) == len(data)


def test_delivered_database_matches_json():
    """Файл data/survey_service.sqlite соответствует JSON-файлам."""
    conn = sqlite3.connect(ROOT / "data" / "survey_service.sqlite")
    for table, filename in (("users", "users.json"),
                            ("surveys", "surveys.json"),
                            ("responses", "responses.json")):
        data = json.loads(
            (ROOT / "data" / filename).read_text(encoding="utf-8"))
        total = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        assert total == len(data)
    conn.close()


# ---------- файл queries.sql ----------

def read_queries():
    text = (ROOT / "sql" / "queries.sql").read_text(encoding="utf-8")
    parts = re.split(r";\s*\n", text)
    return [part.strip() for part in parts if "SELECT" in part]


def test_queries_file_has_required_volume_and_kinds():
    queries = read_queries()
    assert len(queries) >= 10
    for keyword in ("WHERE", "JOIN", "COUNT(", "GROUP BY"):
        assert sum(keyword in q for q in queries) >= 2, keyword
    assert any("HAVING" in q for q in queries)


def test_every_query_runs_on_sample_data(sample_db):
    conn = sqlite3.connect(sample_db)
    for query in read_queries():
        conn.execute(query).fetchall()
    conn.close()


# ---------- без f-строк в SQL ----------

@pytest.mark.parametrize("name", [
    "surveys/views.py", "responses/views.py", "db/database.py",
    "db/import_json.py",
])
def test_no_fstring_or_format_in_sql(name):
    source = (ROOT / name).read_text(encoding="utf-8")
    assert not re.search(
        r'\bf"""?\s*(SELECT|INSERT|UPDATE|DELETE)', source, re.I)
    assert ".format(" not in source


# ---------- страницы ----------

def test_surveys_list_shows_questions_count_from_join(sample_db):
    html = client.get("/surveys/").content.decode()
    assert "Вопросов: 2" in html
    assert "Вопросов: 0" in html


def test_topic_filter_uses_parameter(sample_db):
    html = client.get("/surveys/", {"topic": "Спорт"}).content.decode()
    assert "Всего опросов: 1" in html
    assert 'href="/surveys/2/"' in html
    assert 'href="/surveys/1/"' not in html


def test_topic_filter_is_not_vulnerable_to_injection(sample_db):
    response = client.get("/surveys/", {"topic": "' OR '1'='1"})
    assert "Всего опросов: 0" in response.content.decode()
    assert count(sample_db, "surveys") == 3


def test_active_page_shows_only_active_surveys(sample_db):
    html = client.get("/surveys/active/").content.decode()
    assert 'href="/surveys/1/"' in html and 'href="/surveys/3/"' in html
    assert 'href="/surveys/2/"' not in html


def test_available_page_without_user_shows_form_only(sample_db):
    html = client.get("/surveys/available/").content.decode()
    assert "<select" in html and "Анна" in html
    assert 'class="card survey-card"' not in html


def test_available_excludes_answered_and_closed(sample_db):
    html = client.get("/surveys/available/", {"user": 1}).content.decode()
    assert 'href="/surveys/3/"' in html
    assert 'href="/surveys/1/"' not in html
    assert 'href="/surveys/2/"' not in html


def test_available_for_user_without_answers(sample_db):
    html = client.get("/surveys/available/", {"user": 3}).content.decode()
    assert 'href="/surveys/1/"' in html and 'href="/surveys/3/"' in html


def test_available_empty_result_is_not_an_error(sample_db):
    execute(sample_db, "INSERT INTO responses VALUES "
            "(10, 2, 3, 'Любимый цвет?', 'Красный')")
    response = client.get("/surveys/available/", {"user": 2})
    assert response.status_code == 200
    assert "Доступных опросов нет" in response.content.decode()


@pytest.mark.parametrize("value", ["99", "abc", "1 OR 1=1", "-1"])
def test_available_rejects_bad_user(sample_db, value):
    response = client.get("/surveys/available/", {"user": value})
    assert response.status_code == 200
    assert "Пользователь не найден." in response.content.decode()


def test_response_pages_use_join(sample_db):
    html = client.get("/responses/").content.decode()
    assert "Анна" in html and "Борис" in html
    detail = client.get("/responses/3/").content.decode()
    assert "Борис (b@b.ru)" in detail and "Java" in detail
    assert 'href="/surveys/1/"' in detail


def test_statistics_page_aggregates(sample_db):
    html = client.get("/responses/statistics/").content.decode()
    assert '<div class="fs-3">2</div>' in html
    assert '<div class="fs-3">3</div>' in html
    assert "участников: 2" in html
    assert "мин. 20" in html and "макс. 30" in html


def test_statistics_includes_surveys_without_responses(sample_db):
    html = client.get("/responses/statistics/").content.decode()
    assert "Второй" in html
    assert '<span class="badge bg-primary">0</span>' in html


def test_statistics_having_threshold_is_a_parameter(sample_db):
    html = client.get("/responses/statistics/", {"min": 2}).content.decode()
    assert '<span class="badge bg-success">3</span>' in html
    html = client.get("/responses/statistics/", {"min": 3}).content.decode()
    assert "Нет опросов с числом ответов больше 3." in html


@pytest.mark.parametrize("value", ["abc", "-1", "1; DROP TABLE users"])
def test_statistics_bad_threshold_falls_back_to_default(sample_db, value):
    response = client.get("/responses/statistics/", {"min": value})
    assert response.status_code == 200
    assert count(sample_db, "users") == 3


def test_statistics_last_responses_limit(sample_db):
    for number in range(10, 18):
        execute(sample_db, "INSERT INTO responses VALUES "
                "(?, 1, 1, 'Язык?', 'x')", [number])
    html = client.get("/responses/statistics/").content.decode()
    assert html.count("Ответ №") == 5
    assert "Ответ №17" in html


def test_pages_work_with_empty_database(empty_db):
    for url in ("/surveys/", "/surveys/active/", "/surveys/available/",
                "/responses/", "/responses/statistics/"):
        assert client.get(url).status_code == 200, url


def test_survey_detail_404_for_missing_survey(sample_db):
    assert client.get("/surveys/999/").status_code == 404


def test_database_file_is_not_git_ignored():
    ignore = (Path(ROOT) / ".gitignore").read_text(encoding="utf-8")
    assert "!data/survey_service.sqlite" in ignore
