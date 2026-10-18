"""Views приложения surveys: готовят данные и вызывают render()."""

from __future__ import annotations

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from models.responses import get_survey_statistics
from models.surveys import find_survey_by_id
from storage import load_responses, load_surveys, load_users


def surveys(request: HttpRequest) -> HttpResponse:
    """Страница /surveys/: список опросов из data/surveys.json."""
    surveys_list = load_surveys(settings.SURVEYS_FILE)

    context = {
        "surveys": surveys_list,
    }

    return render(request, "surveys/survey_list.html", context)


def survey_detail(request: HttpRequest,
                  survey_id: int) -> HttpResponse:
    """Страница /surveys/<id>/: один опрос.

    Если опроса нет, в шаблон передаётся survey=None, а ответ
    получает код статуса 404.
    """
    surveys_list = load_surveys(settings.SURVEYS_FILE)
    survey = find_survey_by_id(surveys_list, survey_id)

    stats = {}
    if survey is not None:
        users_list = load_users(settings.USERS_FILE)
        responses_list = load_responses(
            settings.RESPONSES_FILE,
            users_list,
            surveys_list,
        )
        stats = get_survey_statistics(responses_list, survey)

    context = {
        "survey": survey,
        "stats": stats,
    }

    return render(
        request,
        "surveys/survey_detail.html",
        context,
        status=404 if survey is None else 200,
    )
