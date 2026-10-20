-- =========================================
-- Сервис проведения опросов: структура БД
-- =========================================

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    age INTEGER NOT NULL,
    is_registered INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS surveys (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    topic TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'активен',
    creation_date TEXT NOT NULL
);

-- options хранит JSON-список вариантов; NULL - открытый вопрос
CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY,
    survey_id INTEGER NOT NULL,
    text TEXT NOT NULL,
    options TEXT,
    FOREIGN KEY (survey_id) REFERENCES surveys(id)
);

CREATE TABLE IF NOT EXISTS responses (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    survey_id INTEGER NOT NULL,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (survey_id) REFERENCES surveys(id)
);
