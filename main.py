from datetime import date


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
)

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
