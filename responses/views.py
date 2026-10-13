"""Views приложения responses: список ответов и страница ответа."""

from __future__ import annotations

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.utils.html import escape

from homepage.views import page
from models.responses import find_response_by_id
from storage import load_responses, load_surveys, load_users


def _load_responses_list():
    """Загрузить ответы вместе со связанными опросами и людьми."""
    surveys_list = load_surveys(settings.SURVEYS_FILE)
    users_list = load_users(settings.USERS_FILE)
    return load_responses(
        settings.RESPONSES_FILE,
        users_list,
        surveys_list,
    )


def responses(request: HttpRequest) -> HttpResponse:
    """Страница /responses/: список ответов из data/responses.json."""
    items = ""
    for resp in _load_responses_list():
        text = escape(
            f"{resp.user.name} - [{resp.survey.id}] "
            f"{resp.survey.title}: {resp.question}"
        )
        items += (
            '<li class="list-group-item">'
            f'<a href="/responses/{resp.id}/">{text}</a>'
            "</li>"
        )

    if not items:
        items = '<li class="list-group-item">Список ответов пуст.</li>'

    content = f"""
    <h1>Ответы</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("Сервис опросов - ответы", content))


def response_detail(request: HttpRequest,
                    response_id: int) -> HttpResponse:
    """Страница /responses/<id>/: карточка одного ответа.

    Если ответа с таким id нет - ответ с кодом 404.
    """
    response = find_response_by_id(_load_responses_list(), response_id)

    if response is None:
        content = """
        <h1 class="text-danger">Ответ не найден</h1>
        <a href="/responses/" class="btn btn-outline-secondary">
            &larr; к списку ответов
        </a>
        """
        return HttpResponse(
            page("Ответ не найден", content),
            status=404,
        )

    content = f"""
    <div class="card">
      <div class="card-body">
        <h5 class="card-title">Ответ №{response.id}</h5>
        <p class="card-text">
            <strong>Пользователь:</strong>
            {escape(response.user.name)}
            ({escape(response.user.email)})
        </p>
        <p class="card-text">
            <strong>Опрос:</strong>
            <a href="/surveys/{response.survey.id}/">
                {escape(response.survey.title)}
            </a>
        </p>
        <p class="card-text">
            <strong>Вопрос:</strong> {escape(response.question)}
        </p>
        <p class="card-text">
            <strong>Ответ:</strong> {escape(response.answer)}
        </p>
        <a href="/responses/" class="btn btn-outline-secondary">
            &larr; к списку ответов
        </a>
      </div>
    </div>
    """
    return HttpResponse(
        page(f"Ответ №{response.id}", content),
        status=200,
    )
