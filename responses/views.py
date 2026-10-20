"""Views приложения responses: SQL-запросы к SQLite и render() (ПР7)."""

from __future__ import annotations

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from db.database import fetch_all, fetch_one

ACTIVE_STATUS = "активен"

# Запрос 10: ответы вместе с пользователем и опросом (JOIN трёх таблиц).
RESPONSES_SQL = """
    SELECT responses.id,
           responses.question,
           responses.answer,
           users.name AS user_name,
           users.email AS user_email,
           surveys.title AS survey_title
    FROM responses
    JOIN users ON responses.user_id = users.id
    JOIN surveys ON responses.survey_id = surveys.id
    ORDER BY responses.id;
"""

# Запрос 11: один ответ по идентификатору.
RESPONSE_SQL = """
    SELECT responses.id,
           responses.question,
           responses.answer,
           users.name AS user_name,
           users.email AS user_email,
           surveys.id AS survey_id,
           surveys.title AS survey_title
    FROM responses
    JOIN users ON responses.user_id = users.id
    JOIN surveys ON responses.survey_id = surveys.id
    WHERE responses.id = ?;
"""

# Запросы 13-15, 18, 19 и 21: страница статистики.
ACTIVE_COUNT_SQL = """
    SELECT COUNT(*) AS active_surveys
    FROM surveys
    WHERE status = ?;
"""

RESPONSES_TOTAL_SQL = """
    SELECT COUNT(*) AS total_responses,
           COUNT(DISTINCT user_id) AS respondents
    FROM responses;
"""

USERS_AGE_SQL = """
    SELECT COUNT(*) AS users_count,
           MIN(age) AS min_age,
           MAX(age) AS max_age,
           ROUND(AVG(age), 1) AS avg_age
    FROM users;
"""

PER_SURVEY_SQL = """
    SELECT surveys.title, COUNT(responses.id) AS responses_count
    FROM surveys
    LEFT JOIN responses ON responses.survey_id = surveys.id
    GROUP BY surveys.id, surveys.title
    ORDER BY responses_count DESC, surveys.title;
"""

POPULAR_SQL = """
    SELECT surveys.title, COUNT(responses.id) AS responses_count
    FROM surveys
    JOIN responses ON responses.survey_id = surveys.id
    GROUP BY surveys.id, surveys.title
    HAVING COUNT(responses.id) > ?
    ORDER BY responses_count DESC, surveys.title;
"""

LAST_RESPONSES_SQL = """
    SELECT responses.id, users.name AS user_name,
           surveys.title AS survey_title, responses.answer
    FROM responses
    JOIN users ON responses.user_id = users.id
    JOIN surveys ON responses.survey_id = surveys.id
    ORDER BY responses.id DESC
    LIMIT 5;
"""


def responses(request: HttpRequest) -> HttpResponse:
    """Страница /responses/: список ответов из БД (JOIN)."""
    context = {
        "responses": fetch_all(RESPONSES_SQL),
    }

    return render(request, "responses/response_list.html", context)


def response_detail(request: HttpRequest,
                    response_id: int) -> HttpResponse:
    """Страница /responses/<id>/: один ответ.

    Если ответа нет, в шаблон передаётся response=None, а ответ
    получает код статуса 404.
    """
    response = fetch_one(RESPONSE_SQL, [response_id])

    context = {
        "response": response,
    }

    return render(
        request,
        "responses/response_detail.html",
        context,
        status=404 if response is None else 200,
    )


def statistics(request: HttpRequest) -> HttpResponse:
    """Страница /responses/statistics/: агрегатные запросы.

    Порог для блока «популярные опросы» берётся из параметра ?min=
    (по умолчанию 1) и передаётся в HAVING через ?.
    """
    min_raw = request.GET.get("min", "1").strip()
    min_responses = int(min_raw) if min_raw.isdecimal() else 1

    context = {
        "active_surveys": fetch_one(ACTIVE_COUNT_SQL, [ACTIVE_STATUS]),
        "totals": fetch_one(RESPONSES_TOTAL_SQL),
        "users_age": fetch_one(USERS_AGE_SQL),
        "per_survey": fetch_all(PER_SURVEY_SQL),
        "min_responses": min_responses,
        "popular": fetch_all(POPULAR_SQL, [min_responses]),
        "last_responses": fetch_all(LAST_RESPONSES_SQL),
    }

    return render(request, "responses/statistics.html", context)
