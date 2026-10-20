"""Views приложения surveys: SQL-запросы к SQLite и render() (ПР7)."""

from __future__ import annotations

import json

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from db.database import fetch_all, fetch_one

ACTIVE_STATUS = "активен"

# Запросы 16 и 5 из sql/queries.sql: все опросы / опросы одной темы.
SURVEYS_SQL = """
    SELECT surveys.id, surveys.title, surveys.topic, surveys.status,
           surveys.creation_date,
           COUNT(questions.id) AS questions_count
    FROM surveys
    LEFT JOIN questions ON questions.survey_id = surveys.id
    GROUP BY surveys.id, surveys.title, surveys.topic, surveys.status,
             surveys.creation_date
    ORDER BY surveys.title;
"""

SURVEYS_BY_TOPIC_SQL = """
    SELECT surveys.id, surveys.title, surveys.topic, surveys.status,
           surveys.creation_date,
           COUNT(questions.id) AS questions_count
    FROM surveys
    LEFT JOIN questions ON questions.survey_id = surveys.id
    WHERE surveys.topic = ?
    GROUP BY surveys.id, surveys.title, surveys.topic, surveys.status,
             surveys.creation_date
    ORDER BY surveys.title;
"""

TOPICS_SQL = """
    SELECT DISTINCT topic
    FROM surveys
    ORDER BY topic;
"""

# Запрос 4: активные опросы.
ACTIVE_SURVEYS_SQL = """
    SELECT id, title, topic, status, creation_date,
           (SELECT COUNT(*) FROM questions
            WHERE questions.survey_id = surveys.id) AS questions_count
    FROM surveys
    WHERE status = ?
    ORDER BY creation_date;
"""

# Запросы 6, 3 и 17: страница одного опроса.
SURVEY_SQL = """
    SELECT id, title, topic, status, creation_date
    FROM surveys
    WHERE id = ?;
"""

QUESTIONS_SQL = """
    SELECT id, text, options
    FROM questions
    WHERE survey_id = ?
    ORDER BY id;
"""

ANSWER_STATS_SQL = """
    SELECT question, answer, COUNT(*) AS answers_count
    FROM responses
    WHERE survey_id = ?
    GROUP BY question, answer
    ORDER BY question, answers_count DESC;
"""

# Запросы 1 и 9: поиск доступных пользователю опросов.
USERS_SQL = """
    SELECT id, name, email
    FROM users
    ORDER BY name;
"""

USER_SQL = """
    SELECT id, name, email
    FROM users
    WHERE id = ?;
"""

AVAILABLE_SURVEYS_SQL = """
    SELECT surveys.id, surveys.title, surveys.topic, surveys.status,
           surveys.creation_date,
           (SELECT COUNT(*) FROM questions
            WHERE questions.survey_id = surveys.id) AS questions_count
    FROM surveys
    WHERE surveys.status = ?
      AND surveys.id NOT IN (
          SELECT responses.survey_id
          FROM responses
          WHERE responses.user_id = ?
      )
    ORDER BY surveys.title;
"""


def surveys(request: HttpRequest) -> HttpResponse:
    """Страница /surveys/: опросы из БД, фильтр по теме (?topic=)."""
    topic = request.GET.get("topic", "").strip()
    if topic:
        surveys_list = fetch_all(SURVEYS_BY_TOPIC_SQL, [topic])
    else:
        surveys_list = fetch_all(SURVEYS_SQL)

    context = {
        "surveys": surveys_list,
        "topics": fetch_all(TOPICS_SQL),
        "selected_topic": topic,
    }

    return render(request, "surveys/survey_list.html", context)


def active_surveys(request: HttpRequest) -> HttpResponse:
    """Страница /surveys/active/: только активные опросы."""
    context = {
        "surveys": fetch_all(ACTIVE_SURVEYS_SQL, [ACTIVE_STATUS]),
    }

    return render(request, "surveys/active_list.html", context)


def survey_detail(request: HttpRequest,
                  survey_id: int) -> HttpResponse:
    """Страница /surveys/<id>/: один опрос, вопросы и статистика.

    Если опроса нет, в шаблон передаётся survey=None, а ответ
    получает код статуса 404.
    """
    survey = fetch_one(SURVEY_SQL, [survey_id])

    questions = []
    stats = []
    if survey is not None:
        for row in fetch_all(QUESTIONS_SQL, [survey_id]):
            options = (None if row["options"] is None
                       else json.loads(row["options"]))
            questions.append({
                "text": row["text"],
                "options": options,
                "is_open": options is None,
            })
        stats = fetch_all(ANSWER_STATS_SQL, [survey_id])

    context = {
        "survey": survey,
        "questions": questions,
        "stats": stats,
    }

    return render(
        request,
        "surveys/survey_detail.html",
        context,
        status=404 if survey is None else 200,
    )


def available_surveys(request: HttpRequest) -> HttpResponse:
    """Страница /surveys/available/?user=<id>.

    Показывает активные опросы, которые выбранный пользователь ещё
    не проходил. Идентификатор пользователя приходит от клиента, поэтому
    в SQL он передаётся только параметром ?.
    """
    user_raw = request.GET.get("user", "").strip()

    selected_user = None
    available = []
    error = None
    if user_raw:
        if user_raw.isdecimal():
            selected_user = fetch_one(USER_SQL, [int(user_raw)])
        if selected_user is None:
            error = "Пользователь не найден."
        else:
            available = fetch_all(
                AVAILABLE_SURVEYS_SQL,
                [ACTIVE_STATUS, selected_user["id"]],
            )

    context = {
        "users": fetch_all(USERS_SQL),
        "selected_user": selected_user,
        "surveys": available,
        "error": error,
    }

    return render(request, "surveys/available.html", context)
