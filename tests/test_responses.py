from responses import (
    add_response,
    get_survey_statistics,
    is_user_participated,
)


def test_add_response():
    responses = []
    add_response(responses, "a@b.ru", 1, "Вопрос?", "Ответ")
    assert len(responses) == 1


def test_is_user_participated():
    responses = []
    add_response(responses, "a@b.ru", 1, "Q", "A")
    assert is_user_participated(responses, "a@b.ru", 1)
    assert not is_user_participated(responses, "c@d.ru", 1)


def test_get_survey_statistics():
    responses = []
    add_response(responses, "a@b.ru", 1, "Q1", "Python")
    add_response(responses, "c@d.ru", 1, "Q1", "Python")
    add_response(responses, "e@f.ru", 1, "Q1", "Java")
    stats = get_survey_statistics(responses, 1)
    assert stats["Python"] == 2
    assert stats["Java"] == 1
