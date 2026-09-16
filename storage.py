from __future__ import annotations

import json
import os


def load_data(filename: str) -> list:
    if not os.path.exists(filename):
        return []
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError) as exc:
        print(f"Ошибка загрузки {filename}: {exc}")
        return []


def save_data(filename: str, data: list) -> None:
    directory = os.path.dirname(filename)
    if directory:
        os.makedirs(directory, exist_ok=True)
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
    except OSError as exc:
        print(f"Ошибка сохранения {filename}: {exc}")
