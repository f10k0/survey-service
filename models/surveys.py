from __future__ import annotations

from datetime import date

from .questions import Question


class Survey:
    """Опрос — набор вопросов по определённой теме."""

    def __init__(self, survey_id: int, title: str, topic: str,
                 questions: list[Question],
                 status: str = "активен",
                 creation_date: str | None = None) -> None:
        """Создать объект опроса."""
        self.id = survey_id
        self.title = title
        self.topic = topic
        self.questions = questions
        self.status = status
        self.creation_date = creation_date or date.today().isoformat()

    @property
    def questions_count(self) -> int:
        """Количество вопросов в опросе."""
        return len(self.questions)

    def is_active(self) -> bool:
        """Проверить, активен ли опрос."""
        return self.status == "активен"

    def add_question(self, question: Question) -> None:
        """Добавить вопрос в опрос."""
        self.questions.append(question)

    @classmethod
    def from_data(cls, data: dict) -> "Survey":
        """Создать опрос из словаря."""
        questions = [
            Question.from_data(item) for item in data["questions"]
        ]
        return cls(
            survey_id=data["id"],
            title=data["title"],
            topic=data["topic"],
            questions=questions,
            status=data.get("status", "активен"),
            creation_date=data.get("creation_date"),
        )

    def to_dict(self) -> dict:
        """Преобразовать опрос в словарь для JSON."""
        return {
            "id": self.id,
            "title": self.title,
            "topic": self.topic,
            "questions": [q.to_dict() for q in self.questions],
            "status": self.status,
            "creation_date": self.creation_date,
        }

    def __str__(self) -> str:
        """Строковое представление опроса."""
        return (
            f"[{self.id}] {self.title} | "
            f"Тема: {self.topic} | "
            f"Вопросов: {self.questions_count} | "
            f"Статус: {self.status}"
        )


# ---------- Функции обработки коллекции опросов ----------

def add_survey(surveys: list[Survey], title: str, topic: str,
               questions: list[Question]) -> Survey:
    """Создать опрос, добавить в коллекцию и вернуть его."""
    next_id = max((s.id for s in surveys), default=0) + 1
    survey = Survey(next_id, title, topic, questions)
    surveys.append(survey)
    return survey


def find_survey_by_id(surveys: list[Survey],
                      survey_id: int) -> Survey | None:
    """Найти опрос по идентификатору."""
    for survey in surveys:
        if survey.id == survey_id:
            return survey
    return None


def find_surveys(surveys: list[Survey], query: str) -> list[Survey]:
    """Найти опросы по подстроке в названии."""
    query_lower = query.lower()
    return [s for s in surveys if query_lower in s.title.lower()]


def filter_surveys_by_questions(surveys: list[Survey],
                                min_questions: int) -> list[Survey]:
    """Отобрать опросы с числом вопросов >= min_questions."""
    return [s for s in surveys if s.questions_count >= min_questions]


def sort_surveys(surveys: list[Survey]) -> list[Survey]:
    """Отсортировать опросы по числу вопросов (по убыванию)."""
    return sorted(surveys, key=lambda s: s.questions_count, reverse=True)
