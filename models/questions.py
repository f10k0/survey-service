"""Класс Question — вопрос опроса."""

from __future__ import annotations


class Question:
    """Вопрос опроса. Может быть открытым или с вариантами."""

    def __init__(self, text: str,
                 options: list[str] | None = None) -> None:
        """Создать вопрос.

        options=None — открытый вопрос (свободный ответ).
        options=[...] — закрытый вопрос (выбор из вариантов).
        """
        self.text = text
        self.options = options

    def is_open(self) -> bool:
        """Проверить, является ли вопрос открытым."""
        return self.options is None

    @staticmethod
    def validate_options(options: list[str] | None) -> bool:
        """Проверить корректность вариантов ответа."""
        if options is None:
            return True
        return isinstance(options, list) and len(options) >= 2

    @classmethod
    def from_data(cls, data: dict) -> "Question":
        """Создать вопрос из словаря."""
        return cls(text=data["text"], options=data.get("options"))

    def to_dict(self) -> dict:
        """Преобразовать вопрос в словарь для JSON."""
        return {"text": self.text, "options": self.options}

    def __str__(self) -> str:
        """Строковое представление вопроса."""
        if self.options is None:
            return f"{self.text} (открытый)"
        return f"{self.text} (варианты: {', '.join(self.options)})"