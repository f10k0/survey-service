"""Тесты веб-интерфейса (ПР5): страницы, динамические URL, 404."""

import json

import pytest
from django.test import Client, override_settings

from models import Question, Survey, User
from models.responses import add_response, find_response_by_id

client = Client()


@pytest.fixture
def data_files(tmp_path):
    """Подменить JSON-файлы данных временными (с «опасным» текстом)."""
    surveys = [{
        "id": 1,
        "title": "Опрос <b>1</b>",
        "topic": "IT",
        "questions": [
            {"text": "Язык?", "options": ["Python", "Java"]},
            {"text": "Комментарий", "options": None},
        ],
        "status": "активен",
        "creation_date": "2026-09-20",
    }]
    users = [{"id": 1, "name": "Анна", "email": "a@b.ru", "age": 20,
              "is_registered": True}]
    responses = [
        {"user_email": "a@b.ru", "survey_id": 1,
         "question": "Язык?", "answer": "Python"},
        {"user_email": "a@b.ru", "survey_id": 1,
         "question": "Комментарий", "answer": "<script>x</script>"},
    ]
    paths = {}
    for name, data in (("surveys", surveys), ("users", users),
                       ("responses", responses)):
        path = tmp_path / f"{name}.json"
        path.write_text(json.dumps(data), encoding="utf-8")
        paths[name] = path
    with override_settings(SURVEYS_FILE=paths["surveys"],
                           USERS_FILE=paths["users"],
                           RESPONSES_FILE=paths["responses"]):
        yield


def test_index_page():
    response = client.get("/")
    assert response.status_code == 200
    assert "Сервис проведения опросов" in response.content.decode()
    assert "bootstrap" in response.content.decode()


def test_surveys_list(data_files):
    response = client.get("/surveys/")
    assert response.status_code == 200
    assert 'href="/surveys/1/"' in response.content.decode()


def test_survey_detail(data_files):
    response = client.get("/surveys/1/")
    html = response.content.decode()
    assert response.status_code == 200
    assert "Python" in html
    assert "активен" in html


def test_survey_not_found(data_files):
    response = client.get("/surveys/999/")
    assert response.status_code == 404
    assert "Опрос не найден" in response.content.decode()


def test_responses_list_and_detail(data_files):
    assert client.get("/responses/").status_code == 200
    response = client.get("/responses/1/")
    assert response.status_code == 200
    assert "Анна" in response.content.decode()


def test_response_not_found(data_files):
    response = client.get("/responses/999/")
    assert response.status_code == 404
    assert "Ответ не найден" in response.content.decode()


def test_html_is_escaped(data_files):
    assert "<b>1</b>" not in client.get("/surveys/").content.decode()
    html = client.get("/responses/2/").content.decode()
    assert "<script>x</script>" not in html
    assert "&lt;script&gt;" in html


def test_non_int_id_is_404():
    """Конвертер <int:...> не пропускает /surveys/abc/."""
    assert client.get("/surveys/abc/").status_code == 404


@override_settings(DEBUG=False)
def test_custom_404_page():
    response = client.get("/nonexistent/")
    assert response.status_code == 404
    html = response.content.decode()
    assert "404 - страница не найдена" in html
    assert 'href="/"' in html


def test_real_data_files_load():
    """Проекты ПР3: реальные JSON-файлы открываются без ошибок."""
    assert client.get("/surveys/").status_code == 200
    assert client.get("/responses/").status_code == 200


def test_find_response_by_id():
    user = User(1, "Анна", "a@b.ru", 20)
    survey = Survey(1, "Опрос", "Тема", [Question("Q")])
    responses = []
    first = add_response(responses, user, survey, "Q", "A")
    second = add_response(responses, user, survey, "Q", "B")
    assert (first.id, second.id) == (1, 2)
    assert find_response_by_id(responses, 2) is second
    assert find_response_by_id(responses, 99) is None
