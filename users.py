from __future__ import annotations


def register_user(users: list, name: str, email: str, age: int) -> dict:
    next_id = max((u["id"] for u in users), default=0) + 1
    user = {
        "id": next_id,
        "name": name,
        "email": email,
        "age": age,
        "is_registered": True,
    }
    users.append(user)
    return user


def find_user_by_email(users: list, email: str) -> dict | None:
    for user in users:
        if user["email"] == email:
            return user
    return None


def check_user_age(user: dict, min_age: int = 18,
                   max_age: int = 100) -> bool:
    return min_age <= user["age"] <= max_age
