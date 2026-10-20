-- =========================================
-- Сервис проведения опросов: SQL-запросы
-- Каждый запрос проверен в SQLite и используется в views (см. пометку).
-- Значения, которые в приложении приходят от пользователя, здесь
-- заданы для проверки; в views они передаются параметрами ?.
-- =========================================


-- ---------- Выборка списков (SELECT) ----------

-- 1. Список пользователей (выпадающий список на /surveys/available/)
SELECT id, name, email
FROM users
ORDER BY name;

-- 2. Список тем опросов без повторов (фильтр на /surveys/)
SELECT DISTINCT topic
FROM surveys
ORDER BY topic;

-- 3. Вопросы выбранного опроса (страница /surveys/<id>/)
SELECT id, text, options
FROM questions
WHERE survey_id = 1
ORDER BY id;


-- ---------- Фильтрация (WHERE) ----------

-- 4. Активные опросы (страница /surveys/active/)
SELECT id, title, topic, status, creation_date,
       (SELECT COUNT(*) FROM questions
        WHERE questions.survey_id = surveys.id) AS questions_count
FROM surveys
WHERE status = 'активен'
ORDER BY creation_date;

-- 5. Опросы выбранной темы (страница /surveys/?topic=...)
SELECT id, title, topic, status
FROM surveys
WHERE topic = 'IT и разработка'
ORDER BY title;

-- 6. Опрос по идентификатору (страница /surveys/<id>/)
SELECT id, title, topic, status, creation_date
FROM surveys
WHERE id = 1;

-- 7. Поиск по подстроке (LIKE). Внимание: в SQLite LIKE не различает
-- регистр только у латиницы, поэтому для кириллицы регистр важен.
SELECT id, title
FROM surveys
WHERE title LIKE '%Опрос%';

-- 8. Несколько условий: ответы пользователя на опрос (AND)
SELECT id, question, answer
FROM responses
WHERE user_id = 1
  AND survey_id = 1;

-- 9. Доступные для прохождения опросы: активные и ещё не пройденные
--    пользователем (подзапрос NOT IN; страница /surveys/available/)
SELECT surveys.id, surveys.title, surveys.topic
FROM surveys
WHERE surveys.status = 'активен'
  AND surveys.id NOT IN (
      SELECT responses.survey_id
      FROM responses
      WHERE responses.user_id = 1
  )
ORDER BY surveys.title;


-- ---------- Соединение таблиц (JOIN) ----------

-- 10. Полная информация об ответах: ответ + пользователь + опрос
--     (страница /responses/)
SELECT responses.id,
       responses.question,
       responses.answer,
       users.name AS user_name,
       users.email AS user_email,
       surveys.title AS survey_title
FROM responses
JOIN users ON responses.user_id = users.id
JOIN surveys ON responses.survey_id = surveys.id
ORDER BY responses.id;

-- 11. Один ответ с данными пользователя и опроса
--     (страница /responses/<id>/)
SELECT responses.id,
       responses.question,
       responses.answer,
       users.name AS user_name,
       users.email AS user_email,
       surveys.id AS survey_id,
       surveys.title AS survey_title
FROM responses
JOIN users ON responses.user_id = users.id
JOIN surveys ON responses.survey_id = surveys.id
WHERE responses.id = 1;

-- 12. Вопросы с названиями опросов
SELECT questions.id, surveys.title AS survey_title, questions.text
FROM questions
JOIN surveys ON questions.survey_id = surveys.id
ORDER BY surveys.title, questions.id;


-- ---------- Агрегатные функции ----------

-- 13. Количество активных опросов (COUNT; страница /responses/statistics/)
SELECT COUNT(*) AS active_surveys
FROM surveys
WHERE status = 'активен';

-- 14. Количество ответов и участников (COUNT, COUNT DISTINCT)
SELECT COUNT(*) AS total_responses,
       COUNT(DISTINCT user_id) AS respondents
FROM responses;

-- 15. Возраст пользователей (COUNT, MIN, MAX, AVG)
SELECT COUNT(*) AS users_count,
       MIN(age) AS min_age,
       MAX(age) AS max_age,
       ROUND(AVG(age), 1) AS avg_age
FROM users;


-- ---------- Группировка (GROUP BY) и HAVING ----------

-- 16. Опросы с количеством вопросов (LEFT JOIN + GROUP BY;
--     страница /surveys/). Опрос без вопросов получает 0.
SELECT surveys.id, surveys.title, surveys.topic, surveys.status,
       surveys.creation_date,
       COUNT(questions.id) AS questions_count
FROM surveys
LEFT JOIN questions ON questions.survey_id = surveys.id
GROUP BY surveys.id, surveys.title, surveys.topic, surveys.status,
         surveys.creation_date
ORDER BY surveys.title;

-- 17. Статистика ответов опроса: сколько раз выбран каждый ответ
--     (GROUP BY; страница /surveys/<id>/)
SELECT question, answer, COUNT(*) AS answers_count
FROM responses
WHERE survey_id = 1
GROUP BY question, answer
ORDER BY question, answers_count DESC;

-- 18. Количество ответов по каждому опросу (LEFT JOIN + GROUP BY;
--     страница /responses/statistics/). Опрос без ответов получает 0.
SELECT surveys.title, COUNT(responses.id) AS responses_count
FROM surveys
LEFT JOIN responses ON responses.survey_id = surveys.id
GROUP BY surveys.id, surveys.title
ORDER BY responses_count DESC, surveys.title;

-- 19. Популярные опросы: больше заданного числа ответов (HAVING;
--     порог в приложении берётся из параметра ?min=)
SELECT surveys.title, COUNT(responses.id) AS responses_count
FROM surveys
JOIN responses ON responses.survey_id = surveys.id
GROUP BY surveys.id, surveys.title
HAVING COUNT(responses.id) > 1
ORDER BY responses_count DESC;

-- 20. Активность пользователей: ответов на каждого (GROUP BY)
SELECT users.name, COUNT(responses.id) AS answers_count
FROM users
LEFT JOIN responses ON responses.user_id = users.id
GROUP BY users.id, users.name
ORDER BY answers_count DESC, users.name;


-- ---------- Сортировка и ограничение (LIMIT) ----------

-- 21. Последние 5 ответов (ORDER BY + LIMIT; /responses/statistics/)
SELECT responses.id, users.name AS user_name,
       surveys.title AS survey_title, responses.answer
FROM responses
JOIN users ON responses.user_id = users.id
JOIN surveys ON responses.survey_id = surveys.id
ORDER BY responses.id DESC
LIMIT 5;
