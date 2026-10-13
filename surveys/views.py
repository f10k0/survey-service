"""Views приложения surveys: список опросов и страница опроса."""

from __future__ import annotations

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.utils.html import escape

from homepage.views import page
from models.responses import get_survey_statistics
from models.surveys import find_survey_by_id
from storage import load_responses, load_surveys, load_users


def surveys(request: HttpRequest) -> HttpResponse:
    """Страница /surveys/: список опросов из data/surveys.json."""
    surveys_list = load_surveys(settings.SURVEYS_FILE)

    items = ""
    for survey in surveys_list:
        text = escape(
            f"{survey.title} - тема: {survey.topic}, "
            f"вопросов: {survey.questions_count}"
        )
        items += (
            '<li class="list-group-item">'
            f'<a href="/surveys/{survey.id}/">{text}</a>'
            "</li>"
        )

    if not items:
        items = '<li class="list-group-item">Список опросов пуст.</li>'

    content = f"""
    <h1>Опросы</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("Сервис опросов - опросы", content))


def survey_detail(request: HttpRequest,
                  survey_id: int) -> HttpResponse:
    """Страница /surveys/<id>/: карточка одного опроса.

    Если опроса с таким id нет - ответ с кодом 404.
    """
    surveys_list = load_surveys(settings.SURVEYS_FILE)
    survey = find_survey_by_id(surveys_list, survey_id)

    if survey is None:
        content = """
        <h1 class="text-danger">Опрос не найден</h1>
        <a href="/surveys/" class="btn btn-outline-secondary">
            &larr; к списку опросов
        </a>
        """
        return HttpResponse(
            page("Опрос не найден", content),
            status=404,
        )

    users_list = load_users(settings.USERS_FILE)
    responses_list = load_responses(
        settings.RESPONSES_FILE,
        users_list,
        surveys_list,
    )
    stats = get_survey_statistics(responses_list, survey)

    status = "активен" if survey.is_active() else "закрыт"
    badge = "bg-success" if survey.is_active() else "bg-secondary"

    questions_html = ""
    for question in survey.questions:
        if question.is_open():
            kind = "открытый вопрос"
        else:
            kind = "варианты: " + ", ".join(question.options)
        questions_html += (
            '<li class="list-group-item">'
            f"{escape(question.text)} ({escape(kind)})"
            "</li>"
        )

    stats_html = ""
    for answer, count in stats.items():
        stats_html += (
            '<li class="list-group-item">'
            f"&laquo;{escape(answer)}&raquo;: {count}"
            "</li>"
        )
    if not stats_html:
        stats_html = (
            '<li class="list-group-item">Ответов пока нет.</li>'
        )

    content = f"""
    <div class="card">
      <div class="card-body">
        <h5 class="card-title">{escape(survey.title)}</h5>
        <p class="card-text"><strong>ID:</strong> {survey.id}</p>
        <p class="card-text">
            <strong>Тема:</strong> {escape(survey.topic)}
        </p>
        <p class="card-text">
            <strong>Дата создания:</strong> {survey.creation_date}
        </p>
        <p class="card-text">
            Статус:
            <span class="badge {badge}">{status}</span>
        </p>
        <h6 class="mt-3">Вопросы:</h6>
        <ul class="list-group">{questions_html}</ul>
        <h6 class="mt-3">Статистика ответов:</h6>
        <ul class="list-group">{stats_html}</ul>
        <a href="/surveys/" class="btn btn-outline-secondary mt-3">
            &larr; к списку опросов
        </a>
      </div>
    </div>
    """
    return HttpResponse(page(survey.title, content), status=200)
