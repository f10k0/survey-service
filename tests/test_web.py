"""Тесты веб-интерфейса (ПР5): страницы, динамические URL, 404."""

from django.test import Client, override_settings

from models import Question, Survey, User
from models.responses import add_response, find_response_by_id

client = Client()


def test_index_page():
    response = client.get("/")
    assert response.status_code == 200
    assert "Сервис проведения опросов" in response.content.decode()
    assert "bootstrap" in response.content.decode()


def test_surveys_list(sample_db):
    response = client.get("/surveys/")
    assert response.status_code == 200
    assert 'href="/surveys/1/"' in response.content.decode()


def test_survey_detail(sample_db):
    response = client.get("/surveys/1/")
    html = response.content.decode()
    assert response.status_code == 200
    assert "Python" in html
    assert "активен" in html


def test_survey_not_found(sample_db):
    response = client.get("/surveys/999/")
    assert response.status_code == 404
    assert "Опрос не найден" in response.content.decode()


def test_responses_list_and_detail(sample_db):
    assert client.get("/responses/").status_code == 200
    response = client.get("/responses/1/")
    assert response.status_code == 200
    assert "Анна" in response.content.decode()


def test_response_not_found(sample_db):
    response = client.get("/responses/999/")
    assert response.status_code == 404
    assert "Ответ не найден" in response.content.decode()


def test_html_is_escaped(sample_db):
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


def test_real_sample_db_load():
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
