from __future__ import annotations

from datetime import date


def add_survey(surveys: list, title: str, topic: str,
               questions: list[dict]) -> dict:
    next_id = max((s["id"] for s in surveys), default=0) + 1
    survey = {
        "id": next_id,
        "title": title,
        "topic": topic,
        "questions": questions,
        "status": "активен",
        "creation_date": date.today().isoformat(),
    }
    surveys.append(survey)
    return survey


def find_survey_by_id(surveys: list, survey_id: int) -> dict | None:
    for survey in surveys:
        if survey["id"] == survey_id:
            return survey
    return None


def find_surveys(surveys: list, query: str) -> list:
    query_lower = query.lower()
    return [
        survey for survey in surveys
        if query_lower in survey["title"].lower()
    ]


def filter_surveys_by_questions(surveys: list,
                                min_questions: int) -> list:
    return [
        survey for survey in surveys
        if len(survey["questions"]) >= min_questions
    ]


def sort_surveys(surveys: list) -> list:
    return sorted(
        surveys,
        key=lambda survey: len(survey["questions"]),
        reverse=True,
    )


def get_survey_status(survey: dict) -> str:
    if survey["status"] == "активен":
        return "Опрос доступен для прохождения"
    return "Опрос недоступен"
