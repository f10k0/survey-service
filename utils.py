"""Вспомогательные функции безопасного ввода."""

from __future__ import annotations

from datetime import date, datetime


def input_int(prompt: str) -> int:
    """Запросить целое число с повторением при ошибке."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Ошибка: введите целое число.")


def input_str(prompt: str) -> str:
    """Запросить непустую строку."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Ошибка: строка не может быть пустой.")


def input_date(prompt: str) -> date:
    """Запросить дату в формате ДД.ММ.ГГГГ."""
    while True:
        try:
            return datetime.strptime(input(prompt), "%d.%m.%Y").date()
        except ValueError:
            print("Ошибка: используйте формат ДД.ММ.ГГГГ.")
