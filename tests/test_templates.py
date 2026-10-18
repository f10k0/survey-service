"""Тесты шаблонов Django (ПР6): наследование, include, static, URL."""

import json

import pytest
from django.contrib.staticfiles import finders
from django.template.loader import get_template
from django.test import Client, override_settings
from django.urls import reverse

import homepage.views

client = Client()


@pytest.fixture
def data_files(tmp_path):
    """Подменить JSON-файлы данных временными."""
    surveys = [
        {"id": 1, "title": "Первый", "topic": "IT",
         "questions": [{"text": "Q1", "options": ["A", "B"]},
                       {"text": "Q2", "options": None}],
         "status": "активен", "creation_date": "2026-09-20"},
        {"id": 2, "title": "Второй", "topic": "Спорт",
         "questions": [], "status": "завершён",
         "creation_date": "2026-09-21"},
    ]
    users = [{"id": 1, "name": "Анна", "email": "a@b.ru", "age": 20,
              "is_registered": True}]
    responses = [{"user_email": "a@b.ru", "survey_id": 1,
                  "question": "Q1", "answer": "A"}]
    paths = {}
    for name, data in (("surveys", surveys), ("users", users),
                       ("responses", responses)):
        path = tmp_path / f"{name}.json"
        path.write_text(json.dumps(data), encoding="utf-8")
        paths[name] = path
    with override_settings(SURVEYS_FILE=paths["surveys"],
                           USERS_FILE=paths["users"],
                           RESPONSES_FILE=paths["responses"]):
        yield tmp_path


def test_page_function_removed():
    """page() из ПР5 больше не существует."""
    assert not hasattr(homepage.views, "page")


@pytest.mark.parametrize("name", [
    "base.html", "includes/navigation.html", "404.html",
    "homepage/index.html", "surveys/survey_list.html",
    "surveys/survey_detail.html", "surveys/includes/survey_card.html",
    "surveys/includes/survey_status.html",
    "responses/response_list.html", "responses/response_detail.html",
])
def test_templates_are_found(name):
    assert get_template(name) is not None


@pytest.mark.parametrize("path", [
    "homepage/css/style.css",
    "homepage/js/main.js",
    "homepage/img/logo.png",
])
def test_static_files_exist(path):
    assert finders.find(path)


def test_named_urls_and_namespaces():
    assert reverse("homepage:index") == "/"
    assert reverse("surveys:list") == "/surveys/"
    assert reverse("surveys:detail", args=[3]) == "/surveys/3/"
    assert reverse("responses:list") == "/responses/"
    assert reverse("responses:detail", args=[2]) == "/responses/2/"


def test_base_template_inheritance_and_static():
    html = client.get("/").content.decode()
    assert "<title>" in html and "Главная - Сервис опросов" in html
    assert "/static/homepage/css/style.css" in html
    assert "/static/homepage/js/main.js" in html
    assert "/static/homepage/img/logo.png" in html
    assert 'id="current-year"' in html
    assert 'href="/surveys/"' in html and 'href="/responses/"' in html


def test_list_uses_card_include_filters_and_loop(data_files):
    html = client.get("/surveys/").content.decode()
    assert "Всего опросов: 2" in html
    assert html.count('class="card survey-card"') == 2
    assert 'href="/surveys/1/"' in html
    assert "survey-status-active" in html
    assert "survey-status-closed" in html


def test_empty_collections(data_files):
    (data_files / "surveys.json").write_text("[]", encoding="utf-8")
    (data_files / "responses.json").write_text("[]", encoding="utf-8")
    html = client.get("/surveys/").content.decode()
    assert "Всего опросов: 0" in html and "Опросов пока нет." in html
    html = client.get("/responses/").content.decode()
    assert "Ответов пока нет." in html


def test_default_filter_for_empty_title(data_files):
    (data_files / "surveys.json").write_text(json.dumps([
        {"id": 5, "title": "", "topic": "T", "questions": []},
    ]), encoding="utf-8")
    assert "Без названия" in client.get("/surveys/").content.decode()


def test_detail_condition_branches(data_files):
    html = client.get("/surveys/1/").content.decode()
    assert "открытый вопрос" in html
    assert "варианты: A, B" in html
    assert "&laquo;A&raquo;: 1" in html
    closed = client.get("/surveys/2/").content.decode()
    assert "Вопросов нет." in closed
    assert "Ответов пока нет." in closed


def test_not_found_pages_use_template_and_status(data_files):
    for url, text in (("/surveys/999/", "Опрос не найден"),
                      ("/responses/999/", "Ответ не найден")):
        response = client.get(url)
        assert response.status_code == 404
        assert text in response.content.decode()
        assert 'href="/surveys/"' in response.content.decode()


def test_context_name_mismatch_gives_empty_output(data_files):
    """Переменной нет в контексте - Django выводит пустую строку."""
    template = get_template("surveys/survey_list.html")
    html = template.render({"items": []})
    assert "Всего опросов: 0" in html


def test_autoescape_in_templates(data_files):
    (data_files / "surveys.json").write_text(json.dumps([
        {"id": 1, "title": "<b>x</b>", "topic": "T", "questions": []},
    ]), encoding="utf-8")
    html = client.get("/surveys/").content.decode()
    assert "<b>x</b>" not in html and "&lt;b&gt;x&lt;/b&gt;" in html
