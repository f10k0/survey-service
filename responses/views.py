"""Views приложения responses: готовят данные и вызывают render()."""

from __future__ import annotations

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

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
    context = {
        "responses": _load_responses_list(),
    }

    return render(request, "responses/response_list.html", context)


def response_detail(request: HttpRequest,
                    response_id: int) -> HttpResponse:
    """Страница /responses/<id>/: один ответ.

    Если ответа нет, в шаблон передаётся response=None, а ответ
    получает код статуса 404.
    """
    response = find_response_by_id(_load_responses_list(), response_id)

    context = {
        "response": response,
    }

    return render(
        request,
        "responses/response_detail.html",
        context,
        status=404 if response is None else 200,
    )
