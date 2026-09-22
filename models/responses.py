from __future__ import annotations

from .surveys import Survey
from .users import User


class Response:
    """Ответ пользователя на вопрос конкретного опроса."""

    def __init__(self, user: User, survey: Survey,
                 question: str, answer: str) -> None:
        """Создать ответ. Храним ссылки на объекты User и Survey."""
        self.user = user
        self.survey = survey
        self.question = question
        self.answer = answer

    @classmethod
    def from_data(cls, data: dict,
                  users: list[User],
                  surveys: list[Survey]) -> "Response | None":
        """Восстановить ответ из JSON, найдя связанные объекты."""
        user = next(
            (u for u in users if u.email == data["user_email"]),
            None,
        )
        survey = next(
            (s for s in surveys if s.id == data["survey_id"]),
            None,
        )
        if user is None or survey is None:
            return None
        return cls(user, survey, data["question"], data["answer"])

    def to_dict(self) -> dict:
        """Преобразовать ответ в словарь для JSON."""
        return {
            "user_email": self.user.email,
            "survey_id": self.survey.id,
            "question": self.question,
            "answer": self.answer,
        }

    def __str__(self) -> str:
        """Строковое представление ответа."""
        return (f"{self.user.name} → [{self.survey.id}] "
                f"{self.question}: «{self.answer}»")


# ---------- Функции обработки коллекции ответов ----------

def add_response(responses: list[Response], user: User,
                 survey: Survey, question: str,
                 answer: str) -> Response:
    """Добавить ответ в коллекцию."""
    response = Response(user, survey, question, answer)
    responses.append(response)
    return response


def is_user_participated(responses: list[Response], user: User,
                         survey: Survey) -> bool:
    """Проверить, участвовал ли пользователь в опросе."""
    return any(
        r.user.email == user.email and r.survey.id == survey.id
        for r in responses
    )


def get_survey_statistics(responses: list[Response],
                          survey: Survey) -> dict[str, int]:
    """Подсчитать количество ответов по вариантам."""
    stats: dict[str, int] = {}
    for response in responses:
        if response.survey.id == survey.id:
            answer = response.answer
            stats[answer] = stats.get(answer, 0) + 1
    return stats


def get_user_responses(responses: list[Response],
                       user: User) -> list[Response]:
    """Все ответы конкретного пользователя."""
    return [r for r in responses if r.user.email == user.email]
