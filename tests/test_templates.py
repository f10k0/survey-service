"""Тесты шаблонов Django (ПР6): наследование, include, static, URL."""

import pytest
from django.contrib.staticfiles import finders
from django.template.loader import get_template
from django.test import Client
from django.urls import reverse

import homepage.views
from conftest import execute

client = Client()


def test_page_function_removed():
    """page() из ПР5 больше не существует."""
    assert not hasattr(homepage.views, "page")


@pytest.mark.parametrize("name", [
    "base.html", "includes/navigation.html", "404.html",
    "homepage/index.html", "surveys/survey_list.html",
    "surveys/survey_detail.html", "surveys/includes/survey_card.html",
    "surveys/active_list.html", "surveys/available.html",
    "responses/statistics.html",
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
    assert reverse("surveys:active") == "/surveys/active/"
    assert reverse("surveys:available") == "/surveys/available/"
    assert reverse("responses:statistics") == "/responses/statistics/"


def test_base_template_inheritance_and_static():
    html = client.get("/").content.decode()
    assert "<title>" in html and "Главная - Сервис опросов" in html
    assert "/static/homepage/css/style.css" in html
    assert "/static/homepage/js/main.js" in html
    assert "/static/homepage/img/logo.png" in html
    assert 'id="current-year"' in html
    for url in ("/surveys/", "/surveys/active/", "/responses/",
                "/responses/statistics/"):
        assert f'href="{url}"' in html


def test_list_uses_card_include_filters_and_loop(sample_db):
    html = client.get("/surveys/").content.decode()
    assert "Всего опросов: 3" in html
    assert html.count('class="card survey-card"') == 3
    assert "Вопросов: 2" in html
    assert 'href="/surveys/1/"' in html
    assert "survey-status-active" in html
    assert "survey-status-closed" in html


def test_empty_collections(sample_db):
    execute(sample_db, "DELETE FROM responses")
    execute(sample_db, "DELETE FROM questions")
    execute(sample_db, "DELETE FROM surveys")
    html = client.get("/surveys/").content.decode()
    assert "Всего опросов: 0" in html and "Опросов пока нет." in html
    html = client.get("/responses/").content.decode()
    assert "Ответов пока нет." in html


def test_default_filter_for_empty_title(sample_db):
    execute(sample_db, "UPDATE surveys SET title = '' WHERE id = 3")
    assert "Без названия" in client.get("/surveys/").content.decode()


def test_detail_condition_branches(sample_db):
    html = client.get("/surveys/1/").content.decode()
    assert "открытый вопрос" in html
    assert "варианты: Python, Java" in html
    assert "Язык?:" in html and "&laquo;Python&raquo; &mdash;" in html
    closed = client.get("/surveys/2/").content.decode()
    assert "Вопросов нет." in closed
    assert "Ответов пока нет." in closed


def test_not_found_pages_use_template_and_status(sample_db):
    for url, text in (("/surveys/999/", "Опрос не найден"),
                      ("/responses/999/", "Ответ не найден")):
        response = client.get(url)
        assert response.status_code == 404
        assert text in response.content.decode()
        assert 'href="/surveys/"' in response.content.decode()


def test_context_name_mismatch_gives_empty_output(sample_db):
    """Переменной нет в контексте - Django выводит пустую строку."""
    template = get_template("surveys/survey_list.html")
    html = template.render({"items": []})
    assert "Всего опросов: 0" in html


def test_autoescape_in_templates(sample_db):
    execute(sample_db, "UPDATE surveys SET title = '<b>x</b>' WHERE id = 3")
    html = client.get("/surveys/").content.decode()
    assert "<b>x</b>" not in html and "&lt;b&gt;x&lt;/b&gt;" in html
