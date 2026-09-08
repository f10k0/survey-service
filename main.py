from datetime import date

def can_participate_in_survey(user_age, survey_status, is_registered):
    """
    Функция проверяет, может ли пользователь пройти опрос.
    
    Параметры:
    user_age - возраст пользователя (лет)
    survey_status - статус опроса ("активен", "завершен", "ещё не начат")
    is_registered - зарегистрирован ли пользователь в системе (True/False)
    
    Возвращает:
    (available, reason) - кортеж с результатом и причиной
    """
    
    # Проверка статуса опроса
    if survey_status == "активен":
        survey_active = True
    elif survey_status == "ещё не начат":
        return False, "Опрос ещё не начался. Дата старта позже."
    else:  # "завершен"
        return False, "Опрос уже завершен. Результаты будут опубликованы позже."
    
    # Проверка регистрации пользователя
    if not is_registered:
        return False, "Пользователь не зарегистрирован. Требуется регистрация для прохождения опроса."
    
    # Проверка возрастного ограничения
    if user_age < 18:
        return False, f"Ваш возраст ({user_age} лет) не подходит. Опрос доступен только для 18+."
    elif user_age > 100:
        return False, f"Возраст ({user_age} лет) не соответствует допустимому диапазону."
    
    # Если все проверки пройдены
    return True, "Пользователь допущен к прохождению опроса"

# Данные об опросе
survey_title = "Опрос о предпочтениях в IT-сфере"
survey_topic = "Технологии и карьера"
survey_status = "активен"
survey_date = date.today()
survey_questions_count = 15

# Данные о пользователе
user_name = "Руслан Коршиков"
user_email = "ruster.korshik@yandex.ru"
user_age = 20
is_registered = True

# Дополнительные параметры
estimated_time = "5 минут"

print("=" * 60)
print("СЕРВИС ПРОВЕДЕНИЯ ОПРОСОВ")
print("Проверка доступа пользователя к опросу")
print("=" * 60)

print("\n📋 ИНФОРМАЦИЯ О ПОЛЬЗОВАТЕЛЕ:")
print(f"  Имя: {user_name}")
print(f"  Email: {user_email}")
print(f"  Возраст: {user_age} лет")
print(f"  Статус регистрации: {'Зарегистрирован' if is_registered else 'Не зарегистрирован'}")

print("\n📊 ИНФОРМАЦИЯ ОБ ОПРОСЕ:")
print(f"  Название: {survey_title}")
print(f"  Тема: {survey_topic}")
print(f"  Статус: {survey_status}")
print(f"  Количество вопросов: {survey_questions_count}")
print(f"  Дата проведения: {survey_date}")
print(f"  Примерное время прохождения: {estimated_time}")

print("\n" + "=" * 60)
print("РЕЗУЛЬТАТ ПРОВЕРКИ (с использованием функции)")
print("=" * 60)

# Вызываем функцию и получаем результат
is_available, message = can_participate_in_survey(
    user_age,
    survey_status,
    is_registered
)

# Выводим результат на основе возвращенных данных
if is_available:
    print("\n✅ ДОСТУП К ОПРОСУ РАЗРЕШЁН")
    print(f"   Пользователь: {user_name}")
    print(f"   Опрос: {survey_title}")
    print(f"   Статус опроса: {survey_status}")
    print(f"   Возраст пользователя: {user_age} лет (ограничение пройдено)")
    print(f"   Регистрация: подтверждена")
    print(f"   Инструкция: ответьте на {survey_questions_count} вопросов за {estimated_time}")
else:
    print("\n❌ ДОСТУП К ОПРОСУ ЗАПРЕЩЁН")
    print(f"   Причина: {message}")

print("\n" + "=" * 60)
print("Конец проверки")
print("=" * 60)

print("\n📚 ИНФОРМАЦИЯ О МОДУЛЯХ:")
print(f"  Модуль datetime использован для даты: {date.today()}")