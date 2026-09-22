"""Тесты классов и функций модуля surveys."""

from models import Question, Survey
from models.surveys import (
    add_survey,
    filter_surveys_by_questions,
    find_surveys,
    sort_surveys,
)


def _q(text: str, options=None) -> Question:
    return Question(text, options)


def test_survey_creation():
    survey = Survey(1, "Опрос", "Тема", [_q("Q1"), _q("Q2")])
    assert survey.id == 1
    assert survey.title == "Опрос"
    assert survey.questions_count == 2
    assert survey.is_active()


def test_survey_add_question():
    survey = Survey(1, "Опрос", "Тема", [])
    survey.add_question(_q("Новый"))
    assert survey.questions_count == 1


def test_survey_str():
    survey = Survey(1, "IT-опрос", "Технологии", [_q("Q1")])
    text = str(survey)
    assert "IT-опрос" in text
    assert "Вопросов: 1" in text


def test_add_survey():
    surveys = []
    add_survey(surveys, "A", "T", [_q("Q1")])
    add_survey(surveys, "B", "T", [_q("Q1"), _q("Q2")])
    assert len(surveys) == 2
    assert surveys[0].id == 1
    assert surveys[1].id == 2


def test_find_surveys():
    surveys = []
    add_survey(surveys, "IT-опрос", "T", [_q("Q1")])
    add_survey(surveys, "Опрос о еде", "T", [_q("Q1")])
    assert len(find_surveys(surveys, "опрос")) == 2
    assert len(find_surveys(surveys, "IT")) == 1


def test_filter_surveys():
    surveys = []
    add_survey(surveys, "A", "T", [_q(f"Q{i}") for i in range(10)])
    add_survey(surveys, "B", "T", [_q(f"Q{i}") for i in range(3)])
    result = filter_surveys_by_questions(surveys, 5)
    assert len(result) == 1
    assert result[0].title == "A"


def test_sort_surveys():
    surveys = []
    add_survey(surveys, "A", "T", [_q("Q1")])
    add_survey(surveys, "B", "T", [_q(f"Q{i}") for i in range(5)])
    sorted_surveys = sort_surveys(surveys)
    assert sorted_surveys[0].title == "B"
