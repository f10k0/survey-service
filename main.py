"""Точка запуска сервиса проведения опросов."""

from __future__ import annotations

from models import Question, Response, Survey, User
from models.responses import (
    add_response,
    get_survey_statistics,
    is_user_participated,
)
from models.surveys import (
    add_survey,
    filter_surveys_by_questions,
    find_survey_by_id,
    find_surveys,
    sort_surveys,
)
from models.users import add_user, find_user_by_email
from storage import (
    load_responses,
    load_surveys,
    load_users,
    save_responses,
    save_surveys,
    save_users,
)
from utils import input_int, input_str

SURVEYS_FILE = "data/surveys.json"
USERS_FILE = "data/users.json"
RESPONSES_FILE = "data/responses.json"


def show_surveys(surveys: list[Survey]) -> None:
    """Вывести список опросов."""
    if not surveys:
        print("Список опросов пуст.")
        return
    print("\n--- ОПРОСЫ ---")
    for survey in surveys:
        print(survey)


def show_statistics(responses: list[Response],
                    survey: Survey) -> None:
    """Вывести статистику по опросу."""
    stats = get_survey_statistics(responses, survey)
    if not stats:
        print("Пока нет ответов по этому опросу.")
        return
    print(f"\n--- СТАТИСТИКА ПО ОПРОСУ «{survey.title}» ---")
    for answer, count in stats.items():
        print(f"  «{answer}»: {count} голос(ов)")


def ask_question() -> Question:
    """Запросить у автора опроса один вопрос."""
    text = input_str("  Текст вопроса: ")
    print("  Тип вопроса: 1 — открытый, 2 — с вариантами ответа")
    kind = input_int("  Ваш выбор: ")

    if kind == 2:
        count = input_int("  Сколько вариантов ответа? ")
        options = []
        for i in range(1, count + 1):
            options.append(input_str(f"    Вариант {i}: "))
        return Question(text, options)

    return Question(text, None)


def menu_create_survey(surveys: list[Survey]) -> None:
    """Создать новый опрос."""
    title = input_str("Название опроса: ")
    topic = input_str("Тема: ")
    count = input_int("Сколько вопросов? ")

    questions = []
    for i in range(1, count + 1):
        print(f"\nВопрос {i}:")
        questions.append(ask_question())

    survey = add_survey(surveys, title, topic, questions)
    save_surveys(SURVEYS_FILE, surveys)
    print(f"\nОпрос создан. ID = {survey.id}.")


def menu_register_user(users: list[User]) -> None:
    """Зарегистрировать пользователя."""
    name = input_str("Имя: ")
    email = input_str("Email: ")
    age = input_int("Возраст: ")

    user = User(0, name, email, age)
    if not user.is_adult():
        print("Возраст должен быть от 18 до 100 лет.")
        return

    user = add_user(users, name, email, age)
    save_users(USERS_FILE, users)
    print(f"Пользователь зарегистрирован. ID = {user.id}.")


def menu_find_survey(surveys: list[Survey]) -> None:
    """Найти опрос по названию."""
    query = input_str("Поисковый запрос: ")
    found = find_surveys(surveys, query)
    show_surveys(found) if found else print("Ничего не найдено.")


def menu_filter_surveys(surveys: list[Survey]) -> None:
    """Отобрать опросы по числу вопросов."""
    min_q = input_int("Минимальное число вопросов: ")
    found = filter_surveys_by_questions(surveys, min_q)
    show_surveys(found) if found else print("Подходящих опросов нет.")


def menu_sort_surveys(surveys: list[Survey]) -> None:
    """Сортировать опросы по числу вопросов."""
    if not surveys:
        print("Список опросов пуст.")
        return
    for survey in sort_surveys(surveys):
        print(f"[{survey.id}] {survey.title} — "
              f"{survey.questions_count} вопросов")


def ask_answer(question: Question) -> str:
    """Получить ответ пользователя на один вопрос."""
    if question.options is not None:
        for i, option in enumerate(question.options, start=1):
            print(f"    {i}. {option}")
        while True:
            number = input_int("    Ваш выбор (номер): ")
            if 1 <= number <= len(question.options):
                return question.options[number - 1]
            print("    Неверный номер.")
    return input_str("    Ваш ответ: ")


def menu_take_survey(surveys: list[Survey], users: list[User],
                     responses: list[Response]) -> None:
    """Пройти опрос."""
    show_surveys(surveys)
    if not surveys:
        return

    survey_id = input_int("Введите ID опроса: ")
    survey = find_survey_by_id(surveys, survey_id)
    if survey is None:
        print("Опрос не найден.")
        return

    email = input_str("Ваш email: ")
    user = find_user_by_email(users, email)
    if user is None:
        print("Пользователь не найден. Сначала зарегистрируйтесь.")
        return
    if not user.is_adult():
        print("Возраст не подходит для прохождения опроса.")
        return
    if is_user_participated(responses, user, survey):
        print("Вы уже участвовали в этом опросе.")
        return

    print(f"\n--- Опрос: {survey.title} ---")
    for i, question in enumerate(survey.questions, start=1):
        print(f"\nВопрос {i}: {question.text}")
        answer = ask_answer(question)
        add_response(responses, user, survey, question.text, answer)

    save_responses(RESPONSES_FILE, responses)
    print("\nСпасибо! Ваши ответы сохранены.")


def menu_show_statistics(surveys: list[Survey],
                         responses: list[Response]) -> None:
    """Показать статистику по опросу."""
    survey_id = input_int("Введите ID опроса: ")
    survey = find_survey_by_id(surveys, survey_id)
    if survey is None:
        print("Опрос не найден.")
        return
    show_statistics(responses, survey)


def main() -> None:
    """Точка запуска приложения."""
    surveys = load_surveys(SURVEYS_FILE)
    users = load_users(USERS_FILE)
    responses = load_responses(RESPONSES_FILE, users, surveys)

    while True:
        print("\n" + "=" * 50)
        print("СЕРВИС ПРОВЕДЕНИЯ ОПРОСОВ")
        print("=" * 50)
        print("  1. Создать опрос")
        print("  2. Зарегистрировать пользователя")
        print("  3. Найти опрос")
        print("  4. Отобрать опросы по числу вопросов")
        print("  5. Сортировать опросы")
        print("  6. Пройти опрос")
        print("  7. Статистика опроса")
        print("  8. Показать все опросы")
        print("  0. Выход")

        choice = input("Выберите действие: ").strip()

        if choice == "0":
            print("До свидания!")
            break
        elif choice == "1":
            menu_create_survey(surveys)
        elif choice == "2":
            menu_register_user(users)
        elif choice == "3":
            menu_find_survey(surveys)
        elif choice == "4":
            menu_filter_surveys(surveys)
        elif choice == "5":
            menu_sort_surveys(surveys)
        elif choice == "6":
            menu_take_survey(surveys, users, responses)
        elif choice == "7":
            menu_show_statistics(surveys, responses)
        elif choice == "8":
            show_surveys(surveys)
        else:
            print("Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()