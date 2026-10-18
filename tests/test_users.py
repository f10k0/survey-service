"""Тесты класса User и функций модуля users."""

from models import User
from models.users import add_user, find_user_by_email, find_user_by_id


def test_user_creation():
    user = User(1, "Руслан", "r@example.com", 20)
    assert user.id == 1
    assert user.name == "Руслан"
    assert user.email == "r@example.com"
    assert user.age == 20
    assert user.is_registered


def test_user_is_adult():
    assert User(1, "A", "a@b.ru", 20).is_adult()
    assert not User(2, "B", "b@b.ru", 10).is_adult()
    assert not User(3, "C", "c@b.ru", 120).is_adult()


def test_user_str():
    user = User(1, "Руслан", "r@example.com", 20)
    text = str(user)
    assert "Руслан" in text
    assert "r@example.com" in text


def test_add_user():
    users = []
    add_user(users, "A", "a@b.ru", 20)
    add_user(users, "B", "b@b.ru", 25)
    assert len(users) == 2
    assert users[0].id == 1
    assert users[1].id == 2


def test_find_user_by_email():
    users = []
    add_user(users, "A", "a@b.ru", 20)
    assert find_user_by_email(users, "a@b.ru") is not None
    assert find_user_by_email(users, "x@y.ru") is None


def test_find_user_by_id():
    users = []
    add_user(users, "A", "a@b.ru", 20)
    assert find_user_by_id(users, 1) is not None
    assert find_user_by_id(users, 99) is None
