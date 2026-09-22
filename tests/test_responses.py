"""Тесты класса Response и функций модуля responses."""

from models import Question, Survey, User
from models.responses import (
    add_response,
    get_survey_statistics,
    is_user_participated,
)


def _make_data():
    user = User(1, "Руслан", "r@example.com", 20)
    survey = Survey(1, "IT-опрос", "Тема", [Question("Q1")])
    return user, survey


def test_response_creation():
    user, survey = _make_data()
    response = add_response([], user, survey, "Q1", "Python")
    assert response.user is user
    assert response.survey is survey
    assert response.answer == "Python"


def test_is_user_participated():
    user, survey = _make_data()
    responses = []
    add_response(responses, user, survey, "Q1", "Python")
    assert is_user_participated(responses, user, survey)


def test_statistics():
    user, survey = _make_data()
    user2 = User(2, "A", "a@b.ru", 25)
    responses = []
    add_response(responses, user, survey, "Q1", "Python")
    add_response(responses, user2, survey, "Q1", "Python")
    add_response(responses, user2, survey, "Q1", "Java")
    stats = get_survey_statistics(responses, survey)
    assert stats["Python"] == 2
    assert stats["Java"] == 1
