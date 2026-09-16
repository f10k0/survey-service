from surveys import (
    add_survey,
    filter_surveys_by_questions,
    find_surveys,
    get_survey_status,
    sort_surveys,
)


def _q(text: str, options=None) -> dict:
    return {"text": text, "options": options}


def test_add_survey():
    surveys = []
    add_survey(surveys, "Опрос 1", "Тема 1", [
        _q("Q1"),
        _q("Q2", ["A", "B"]),
        _q("Q3"),
    ])
    assert len(surveys) == 1
    assert surveys[0]["title"] == "Опрос 1"
    assert len(surveys[0]["questions"]) == 3
    assert surveys[0]["questions"][1]["options"] == ["A", "B"]


def test_find_surveys():
    surveys = []
    add_survey(surveys, "IT-опрос", "Технологии", [_q("Q1")])
    add_survey(surveys, "Опрос о еде", "Еда", [_q("Q1")])
    assert len(find_surveys(surveys, "опрос")) == 2
    assert len(find_surveys(surveys, "IT")) == 1


def test_filter_surveys_by_questions():
    surveys = []
    add_survey(surveys, "A", "T", [_q(f"Q{i}") for i in range(10)])
    add_survey(surveys, "B", "T", [_q(f"Q{i}") for i in range(5)])
    result = filter_surveys_by_questions(surveys, 7)
    assert len(result) == 1
    assert result[0]["title"] == "A"


def test_sort_surveys():
    surveys = []
    add_survey(surveys, "A", "T", [_q(f"Q{i}") for i in range(5)])
    add_survey(surveys, "B", "T", [_q(f"Q{i}") for i in range(15)])
    sorted_surveys = sort_surveys(surveys)
    assert len(sorted_surveys[0]["questions"]) == 15


def test_get_survey_status():
    survey = {"status": "активен"}
    assert "доступен" in get_survey_status(survey)
