from __future__ import annotations

<<<<<<< HEAD
from responses import (
    add_response,
    get_survey_statistics,
    is_user_participated,
=======

# ФУНКЦИЯ 1: РЕГИСТРАЦИЯ ПОЛЬЗОВАТЕЛЯ
def register_user(name, email, age):
    is_registered = True
    print(f"\n👤 Пользователь {name} успешно зарегистрирован.")
    return name, email, age, is_registered


# ФУНКЦИЯ 2: СОЗДАНИЕ ОПРОСА
def create_survey(title, topic, questions_count):
    status = "активен"
    creation_date = date.today()
    print(f"\n📊 Опрос «{title}» создан. Статус: {status}.")
    return title, topic, questions_count, status, creation_date


# ФУНКЦИЯ 3: ПРОВЕРКА ДОСТУПА
def check_access(user_age, survey_status, is_registered):
    if survey_status == "ещё не начат":
        return False, "Опрос ещё не начался. Дата старта позже."
    if survey_status == "завершен":
        return False, "Опрос уже завершён. Результаты будут опубликованы позже."
    if not is_registered:
        return False, "Пользователь не зарегистрирован. Требуется регистрация."
    if user_age < 18:
        return False, f"Ваш возраст ({user_age} лет) не подходит. Опрос доступен только для 18+."
    if user_age > 100:
        return False, f"Возраст ({user_age} лет) не соответствует допустимому диапазону."
    return True, "Пользователь допущен к прохождению опроса"


# ФУНКЦИЯ 4: ПРОХОЖДЕНИЕ ОПРОСА
def take_survey(user_name, survey_title):
    question = "Какой язык программирования вы предпочитаете?"
    print(f"\n📝 {user_name}, вопрос из опроса «{survey_title}»:")
    print(f"   {question}")
    print("   Варианты: Python / Java / JavaScript")
    answer = input("   Ваш ответ: ")
    return question, answer


# НКЦИЯ 5: ПРОСМОТР СТАТИСТИКИ
def view_statistics(question, answer):
    votes = 1
    print("\n📈 СТАТИСТИКА ПО ОПРОСУ:")
    print(f"   Вопрос: {question}")
    print(f"   Вариант «{answer}»: {votes} голос")
    return votes

print("=" * 60)
print("СЕРВИС ПРОВЕДЕНИЯ ОПРОСОВ")
print("=" * 60)

# 1. Регистрация пользователя
user_name, user_email, user_age, is_registered = register_user(
    "Руслан Коршиков", "ruster.korshik@yandex.ru", 20
>>>>>>> 97513ab21554f1d2f4bc5bf3ac2708318dd14c80
)
from storage import load_data, save_data
from surveys import (
    add_survey,
    filter_surveys_by_questions,
    find_survey_by_id,
    find_surveys,
    get_survey_status,
    sort_surveys,
)
from users import check_user_age, find_user_by_email, register_user
from utils import input_int, input_str

<<<<<<< HEAD
SURVEYS_FILE = "data/surveys.json"
USERS_FILE = "data/users.json"
RESPONSES_FILE = "data/responses.json"


def show_surveys(surveys: list) -> None:
    if not surveys:
        print("Список опросов пуст.")
        return
    print("\n--- ОПРОСЫ ---")
    for survey in surveys:
        print(
            f"[{survey['id']}] {survey['title']} | "
            f"Тема: {survey['topic']} | "
            f"Вопросов: {len(survey['questions'])} | "
            f"Статус: {get_survey_status(survey)}"
        )


def show_statistics(responses: list, survey_id: int) -> None:
    stats = get_survey_statistics(responses, survey_id)
    if not stats:
        print("Пока нет ответов по этому опросу.")
        return
    print(f"\n--- СТАТИСТИКА ПО ОПРОСУ {survey_id} ---")
    for answer, count in stats.items():
        print(f"  «{answer}»: {count} голос(ов)")


def ask_question() -> dict:
    text = input_str("  Текст вопроса: ")
    print("  Тип вопроса: 1 — открытый, 2 — с вариантами ответа")
    kind = input_int("  Ваш выбор: ")

    if kind == 2:
        count = input_int("  Сколько вариантов ответа? ")
        options = []
        for i in range(1, count + 1):
            option = input_str(f"    Вариант {i}: ")
            options.append(option)
        return {"text": text, "options": options}

    return {"text": text, "options": None}


def menu_create_survey(surveys: list) -> None:
    title = input_str("Название опроса: ")
    topic = input_str("Тема: ")
    count = input_int("Сколько вопросов? ")

    questions = []
    for i in range(1, count + 1):
        print(f"\nВопрос {i}:")
        questions.append(ask_question())

    survey = add_survey(surveys, title, topic, questions)
    save_data(SURVEYS_FILE, surveys)
    print(f"\nОпрос создан. ID = {survey['id']}.")


def menu_register_user(users: list) -> None:
    name = input_str("Имя: ")
    email = input_str("Email: ")
    age = input_int("Возраст: ")
    if not 18 <= age <= 100:
        print("Возраст должен быть от 18 до 100 лет.")
        return
    user = register_user(users, name, email, age)
    save_data(USERS_FILE, users)
    print(f"Пользователь зарегистрирован. ID = {user['id']}.")


def menu_find_survey(surveys: list) -> None:
    query = input_str("Поисковый запрос: ")
    found = find_surveys(surveys, query)
    if found:
        show_surveys(found)
    else:
        print("Ничего не найдено.")


def menu_filter_surveys(surveys: list) -> None:
    min_q = input_int("Минимальное число вопросов: ")
    found = filter_surveys_by_questions(surveys, min_q)
    if found:
        show_surveys(found)
    else:
        print("Подходящих опросов нет.")


def menu_sort_surveys(surveys: list) -> None:
    if not surveys:
        print("Список опросов пуст.")
        return
    for survey in sort_surveys(surveys):
        print(
            f"[{survey['id']}] {survey['title']} — "
            f"{len(survey['questions'])} вопросов"
        )


def ask_answer(question: dict) -> str:
    if question["options"]:
        for i, option in enumerate(question["options"], start=1):
            print(f"    {i}. {option}")
        while True:
            number = input_int("    Ваш выбор (номер): ")
            if 1 <= number <= len(question["options"]):
                return question["options"][number - 1]
            print("    Неверный номер, попробуйте снова.")
    return input_str("    Ваш ответ: ")


def menu_take_survey(surveys: list, users: list,
                     responses: list) -> None:
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
    if not check_user_age(user):
        print("Возраст не подходит для прохождения опроса.")
        return
    if is_user_participated(responses, email, survey_id):
        print("Вы уже участвовали в этом опросе.")
        return

    print(f"\n--- Опрос: {survey['title']} ---")
    for i, question in enumerate(survey["questions"], start=1):
        print(f"\nВопрос {i}: {question['text']}")
        answer = ask_answer(question)
        add_response(responses, email, survey_id,
                     question["text"], answer)

    save_data(RESPONSES_FILE, responses)
    print("\nСпасибо! Ваши ответы сохранены.")


def menu_show_statistics(responses: list) -> None:
    survey_id = input_int("Введите ID опроса: ")
    show_statistics(responses, survey_id)


def main() -> None:
    surveys = load_data(SURVEYS_FILE)
    users = load_data(USERS_FILE)
    responses = load_data(RESPONSES_FILE)

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
            menu_show_statistics(responses)
        elif choice == "8":
            show_surveys(surveys)
        else:
            print("Неверный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()
=======
# 2. Создание опроса
survey_title, survey_topic, questions_count, survey_status, survey_date = create_survey(
    "Опрос о предпочтениях в IT-сфере", "Технологии и карьера", 15
)

# Вывод информации
print("\n📋 ИНФОРМАЦИЯ О ПОЛЬЗОВАТЕЛЕ:")
print(f"   Имя: {user_name}")
print(f"   Email: {user_email}")
print(f"   Возраст: {user_age} лет")
print(f"   Статус: {'Зарегистрирован' if is_registered else 'Не зарегистрирован'}")

print("\n📊 ИНФОРМАЦИЯ ОБ ОПРОСЕ:")
print(f"   Название: {survey_title}")
print(f"   Тема: {survey_topic}")
print(f"   Статус: {survey_status}")
print(f"   Вопросов: {questions_count}")
print(f"   Дата: {survey_date}")

# 3. Проверка доступа
print("\n" + "=" * 60)
print("ПРОВЕРКА ДОСТУПА")
print("=" * 60)

is_available, message = check_access(user_age, survey_status, is_registered)

if is_available:
    print(f"\n✅ ДОСТУП РАЗРЕШЁН: {message}")

    # 4. Прохождение опроса
    question, answer = take_survey(user_name, survey_title)

    # 5. Просмотр статистики
    votes = view_statistics(question, answer)
else:
    print(f"\n❌ ДОСТУП ЗАПРЕЩЁН: {message}")

print("\n" + "=" * 60)
print("Конец работы программы")
print("=" * 60)

print("\n📚 ИНФОРМАЦИЯ О МОДУЛЯХ:")
print(f"   Модуль datetime использован для даты: {date.today()}")
>>>>>>> 97513ab21554f1d2f4bc5bf3ac2708318dd14c80
