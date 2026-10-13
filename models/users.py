from __future__ import annotations


class User:
    """Пользователь сервиса проведения опросов."""

    def __init__(self, user_id: int, name: str, email: str,
                 age: int, is_registered: bool = True) -> None:
        """Создать пользователя."""
        self.id = user_id
        self.name = name
        self.email = email
        self.age = age
        self.is_registered = is_registered

    def is_adult(self, min_age: int = 18,
                 max_age: int = 100) -> bool:
        """Проверить, подходит ли возраст пользователя."""
        return min_age <= self.age <= max_age

    @classmethod
    def from_data(cls, data: dict) -> "User":
        """Создать пользователя из словаря."""
        return cls(
            user_id=data["id"],
            name=data["name"],
            email=data["email"],
            age=data["age"],
            is_registered=data.get("is_registered", True),
        )

    def to_dict(self) -> dict:
        """Преобразовать пользователя в словарь для JSON."""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "age": self.age,
            "is_registered": self.is_registered,
        }

    def __str__(self) -> str:
        """Строковое представление пользователя."""
        status = "зарегистрирован" if self.is_registered else "нет"
        return (
            f"#{self.id} {self.name} ({self.email}), "
            f"{self.age} лет, {status}"
        )


# ---------- Функции обработки коллекции пользователей ----------

def add_user(users: list[User], name: str, email: str,
             age: int) -> User:
    """Создать пользователя, добавить в коллекцию и вернуть его."""
    next_id = max((u.id for u in users), default=0) + 1
    user = User(next_id, name, email, age)
    users.append(user)
    return user


def find_user_by_email(users: list[User], email: str) -> User | None:
    """Найти пользователя по email."""
    for user in users:
        if user.email == email:
            return user
    return None


def find_user_by_id(users: list[User], user_id: int) -> User | None:
    """Найти пользователя по идентификатору."""
    for user in users:
        if user.id == user_id:
            return user
    return None
