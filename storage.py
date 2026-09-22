"""Загрузка и сохранение объектов в JSON."""

from __future__ import annotations

import json
import os

from models import Response, Survey, User


def _load_json(filename: str) -> list:
    """Прочитать список из JSON-файла (низкоуровневая функция)."""
    if not os.path.exists(filename):
        return []
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError) as exc:
        print(f"Ошибка загрузки {filename}: {exc}")
        return []


def _save_json(filename: str, data: list) -> None:
    """Записать список в JSON-файл (низкоуровневая функция)."""
    directory = os.path.dirname(filename)
    if directory:
        os.makedirs(directory, exist_ok=True)
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
    except OSError as exc:
        print(f"Ошибка сохранения {filename}: {exc}")


def load_surveys(filename: str) -> list[Survey]:
    """Загрузить список опросов как объекты Survey."""
    return [Survey.from_data(item) for item in _load_json(filename)]


def save_surveys(filename: str, surveys: list[Survey]) -> None:
    """Сохранить опросы в JSON."""
    _save_json(filename, [s.to_dict() for s in surveys])


def load_users(filename: str) -> list[User]:
    """Загрузить список пользователей как объекты User."""
    return [User.from_data(item) for item in _load_json(filename)]


def save_users(filename: str, users: list[User]) -> None:
    """Сохранить пользователей в JSON."""
    _save_json(filename, [u.to_dict() for u in users])


def load_responses(filename: str, users: list[User],
                   surveys: list[Survey]) -> list[Response]:
    """Загрузить ответы как объекты Response."""
    result = []
    for item in _load_json(filename):
        response = Response.from_data(item, users, surveys)
        if response is not None:
            result.append(response)
    return result


def save_responses(filename: str, responses: list[Response]) -> None:
    """Сохранить ответы в JSON."""
    _save_json(filename, [r.to_dict() for r in responses])
