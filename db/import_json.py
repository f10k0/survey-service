"""Перенос данных из JSON-файлов в SQLite (ПР7).

Запуск из корня проекта: python -m db.import_json
"""

import json

from db.database import BASE_DIR, get_connection

USERS_FILE = BASE_DIR / "data" / "users.json"
SURVEYS_FILE = BASE_DIR / "data" / "surveys.json"
RESPONSES_FILE = BASE_DIR / "data" / "responses.json"


def load_json(filename):
    """Прочитать список из JSON-файла."""
    with open(filename, encoding="utf-8") as file:
        return json.load(file)


def clear_tables(conn):
    """Очистить таблицы: сначала зависимые, потом справочные."""
    conn.execute("DELETE FROM responses")
    conn.execute("DELETE FROM questions")
    conn.execute("DELETE FROM surveys")
    conn.execute("DELETE FROM users")


def import_users(conn):
    """Перенести пользователей. Возвращает {email: id}."""
    users = load_json(USERS_FILE)
    conn.executemany(
        """
        INSERT INTO users (id, name, email, age, is_registered)
        VALUES (?, ?, ?, ?, ?)
        """,
        [
            (
                user["id"],
                user["name"],
                user["email"],
                user["age"],
                int(user.get("is_registered", True)),
            )
            for user in users
        ],
    )
    return {user["email"]: user["id"] for user in users}


def import_surveys(conn):
    """Перенести опросы и их вопросы (две таблицы из одного файла)."""
    surveys = load_json(SURVEYS_FILE)
    conn.executemany(
        """
        INSERT INTO surveys (id, title, topic, status, creation_date)
        VALUES (?, ?, ?, ?, ?)
        """,
        [
            (
                survey["id"],
                survey["title"],
                survey["topic"],
                survey.get("status", "активен"),
                survey["creation_date"],
            )
            for survey in surveys
        ],
    )
    conn.executemany(
        """
        INSERT INTO questions (survey_id, text, options)
        VALUES (?, ?, ?)
        """,
        [
            (
                survey["id"],
                question["text"],
                None if question["options"] is None
                else json.dumps(question["options"], ensure_ascii=False),
            )
            for survey in surveys
            for question in survey["questions"]
        ],
    )


def import_responses(conn, email_to_id):
    """Перенести ответы: user_email заменяется на user_id.

    Если в JSON у ответа нет id (файл создан в ПР3), id назначается по
    порядку записи - так же, как это делает storage.load_responses().
    """
    responses = load_json(RESPONSES_FILE)
    conn.executemany(
        """
        INSERT INTO responses (id, user_id, survey_id, question, answer)
        VALUES (?, ?, ?, ?, ?)
        """,
        [
            (
                response.get("id", number),
                email_to_id[response["user_email"]],
                response["survey_id"],
                response["question"],
                response["answer"],
            )
            for number, response in enumerate(responses, start=1)
        ],
    )


def main():
    """Импортировать все данные одной транзакцией."""
    conn = get_connection()
    try:
        clear_tables(conn)
        email_to_id = import_users(conn)
        import_surveys(conn)
        import_responses(conn, email_to_id)
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
    print("Данные из JSON перенесены в SQLite.")


if __name__ == "__main__":
    main()
