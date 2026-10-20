# Сервис проведения опросов

Приложение для создания опросов и сбора ответов. Консольная версия
(ПР3) дополнена веб-интерфейсом на Django (ПР5), страницы которого
построены на шаблонах Django Template Language (ПР6). Данные хранятся
в реляционной базе SQLite и читаются SQL-запросами (ПР7).

## Назначение

Проект учебный: хранит опросы, вопросы, пользователей и ответы,
выполняет основные операции с этими объектами и предоставляет доступ к
информации через веб-интерфейс Django. Проект развивается поэтапно:
консольная версия дополнена веб-интерфейсом и постепенно переводится на
возможности Django.

Приложение позволяет:

* просматривать список опросов в браузере;
* просматривать информацию о конкретном опросе (вопросы, статус,
  статистика ответов);
* фильтровать опросы по теме, смотреть активные опросы;
* находить опросы, которые пользователь ещё не проходил;
* смотреть статистику: ответы по опросам, популярные опросы,
  последние ответы;
* просматривать список ответов пользователей и конкретный ответ;
* создавать опросы и регистрировать пользователей (консоль);
* проходить опросы с проверкой возраста и защитой от повторного
  участия (консоль);
* искать, фильтровать и сортировать опросы (консоль);
* хранить данные между запусками (SQLite для веб-версии, JSON для
  консольной).

## Используемые технологии

* Python 3;
* Django 5.2;
* Django Template Language (DTL) - шаблоны страниц;
* HTML5, CSS3, JavaScript;
* Bootstrap 5.3 (CDN) и собственный CSS проекта;
* SQLite и SQL, стандартная библиотека `sqlite3` (ПР7);
* JSON для хранения данных консольной версии и исходных данных;
* Git;
* pytest - автоматизированные тесты;
* flake8 - проверка качества кода.

## Целевая аудитория

Организаторы опросов, преподаватели, HR-специалисты, маркетологи -
все, кому нужно быстро собрать и обработать мнения аудитории.

## Предметная область

Опрос - набор вопросов по определённой теме, на которые пользователь
даёт ответы. Основные сущности (пакет `models/`, ПР3):

* `Question` - вопрос: `text`, `options` (список вариантов или `None`
  для открытого вопроса); методы `is_open()`, `from_data()`,
  `to_dict()`;
* `Survey` - опрос: `id`, `title`, `topic`, `questions`, `status`,
  `creation_date`; `questions_count`, `is_active()`, `add_question()`;
* `User` - пользователь: `id`, `name`, `email`, `age`,
  `is_registered`; `is_adult()`;
* `Response` - ответ: `id`, `user` (объект `User`), `survey` (объект
  `Survey`), `question`, `answer`.

Связи между объектами сохраняются: `response.user.name`,
`response.survey.title`. Для предметной области реализованы собственные
Python-классы (консольная версия). Веб-интерфейс получает данные
из SQLite средствами `sqlite3` и SQL; Django ORM пока не используется.

## Веб-интерфейс

Веб-часть реализована на Django. Страницы формируются шаблонами
Django; функция `page()` из ПР5 удалена, HTML в Python-коде
веб-представлений не формируется. Представления подготавливают данные,
передают их в шаблон через контекст и вызывают `render()`.

| Страница        | URL                    | View-функция                     | Шаблон                                 | Имя маршрута       |
|-----------------|------------------------|----------------------------------|----------------------------------------|--------------------|
| Главная         | `/`                    | `homepage.views.index`           | `homepage/index.html`                  | `homepage:index`   |
| Список опросов  | `/surveys/`            | `surveys.views.surveys`          | `surveys/survey_list.html`             | `surveys:list`     |
| Страница опроса | `/surveys/<int:id>/`   | `surveys.views.survey_detail`    | `surveys/survey_detail.html`           | `surveys:detail`   |
| Список ответов  | `/responses/`          | `responses.views.responses`      | `responses/response_list.html`         | `responses:list`   |
| Страница ответа | `/responses/<int:id>/` | `responses.views.response_detail`| `responses/response_detail.html`       | `responses:detail` |
| Активные опросы | `/surveys/active/`     | `surveys.views.active_surveys`   | `surveys/active_list.html`             | `surveys:active`   |
| Доступные опросы| `/surveys/available/?user=<id>` | `surveys.views.available_surveys` | `surveys/available.html`   | `surveys:available`|
| Статистика      | `/responses/statistics/` | `responses.views.statistics`   | `responses/statistics.html`            | `responses:statistics` |
| Ошибка 404      | любой неизвестный URL  | `homepage.views.page_not_found`  | `404.html`                             | -                  |

Если опрос или ответ с указанным идентификатором не найден, view
передаёт в шаблон `None`, шаблон показывает сообщение («Опрос не
найден» / «Ответ не найден»), а ответ получает код статуса 404.

## Django Template Language

### Базовый шаблон и наследование

`templates/base.html` содержит общую структуру страницы: объявление
документа, кодировку, заголовок, подключение Bootstrap и собственного
CSS, логотип, навигацию, контейнер, подвал и JavaScript. Блоки:

```text
{% block title %}...{% endblock %}
{% block content %}...{% endblock %}
```

Дочерние шаблоны наследуют структуру: `{% extends "base.html" %}` и
переопределяют блоки `title` и `content`.

### Включаемые шаблоны (`include`)

* `templates/includes/navigation.html` - навигация (подключается в
  `base.html`);
* `surveys/includes/survey_card.html` - карточка опроса в списке;
* `surveys/includes/survey_status.html` - статус опроса; используется
  и в карточке, и на странице опроса.

Включаемые шаблоны получают переменные внешнего шаблона (например,
`survey` из цикла).

### Контекст, циклы и условия

Данные передаются словарём контекста:

```python
context = {"surveys": surveys_list}
return render(request, "surveys/survey_list.html", context)
```

В шаблонах используются `{{ ... }}`, циклы `{% for %}` с `{% empty %}`
для пустых коллекций и условия `{% if %}`/`{% else %}` (статус опроса,
отсутствие объекта, открытый или закрытый вопрос).

### Именованные URL и пространства имён

В `urls.py` каждого приложения задан `app_name` и имена маршрутов.
Ссылки строятся тегом `{% url %}`, адреса в HTML не прописываются:

```text
{% url 'homepage:index' %}
{% url 'surveys:list' %}      {% url 'surveys:detail' survey.id %}
{% url 'responses:list' %}    {% url 'responses:detail' response.id %}
```

### Фильтры шаблонов

* `{{ surveys|length }}` - количество опросов и вопросов;
* `{{ survey.title|default:"Без названия" }}` - значение по умолчанию;
* `{{ question.options|join:", " }}` - список вариантов через запятую.

Фильтры используются только для представления данных, бизнес-логика
остаётся в Python. Дата создания хранится как строка (ISO) и выводится
без преобразования шаблоном. Автоэкранирование Django защищает от
внедрения HTML.

### Статические файлы

Статика приложения `homepage` лежит в `homepage/static/homepage/`:

| Файл                 | Назначение                         | Где используется                          |
|----------------------|------------------------------------|-------------------------------------------|
| `css/style.css`      | собственные стили проекта          | `base.html`, карточка и статус опроса     |
| `js/main.js`         | текущий год в подвале              | `base.html`                               |
| `img/logo.png`       | логотип                            | `base.html`                               |

Подключение: `{% load static %}` и `{% static 'homepage/css/style.css' %}`.
Bootstrap 5.3 подключён через CDN и дополняется собственным CSS.

## База данных SQLite (ПР7)

Данные веб-интерфейса хранятся в файле `data/survey_service.sqlite`.
Схема - `sql/schema.sql`, перенос данных из JSON - `db/import_json.py`,
подключение - `db/database.py`, проверенные запросы - `sql/queries.sql`.
Путь данных: `SQLite -> SQL -> sqlite3 -> view -> context -> шаблон`.

### Структура базы данных

Сущности: пользователь, опрос, вопрос опроса, ответ.

**users** - пользователи

| Поле            | Тип     | Назначение                              |
|-----------------|---------|-----------------------------------------|
| `id`            | INTEGER | первичный ключ                          |
| `name`          | TEXT    | имя, NOT NULL                           |
| `email`         | TEXT    | почта, NOT NULL, UNIQUE                 |
| `age`           | INTEGER | возраст, NOT NULL                       |
| `is_registered` | INTEGER | 1 - зарегистрирован, 0 - нет (DEFAULT 1)|

**surveys** - опросы

| Поле            | Тип     | Назначение                                   |
|-----------------|---------|----------------------------------------------|
| `id`            | INTEGER | первичный ключ                               |
| `title`         | TEXT    | название, NOT NULL                           |
| `topic`         | TEXT    | тема, NOT NULL                               |
| `status`        | TEXT    | статус (`активен` и др.), DEFAULT `активен`  |
| `creation_date` | TEXT    | дата создания, формат YYYY-MM-DD             |

**questions** - вопросы опросов

| Поле        | Тип     | Назначение                                        |
|-------------|---------|---------------------------------------------------|
| `id`        | INTEGER | первичный ключ                                    |
| `survey_id` | INTEGER | внешний ключ -> `surveys.id`                      |
| `text`      | TEXT    | текст вопроса, NOT NULL                           |
| `options`   | TEXT    | JSON-список вариантов; NULL - открытый вопрос     |

**responses** - ответы

| Поле        | Тип     | Назначение                       |
|-------------|---------|----------------------------------|
| `id`        | INTEGER | первичный ключ                   |
| `user_id`   | INTEGER | внешний ключ -> `users.id`       |
| `survey_id` | INTEGER | внешний ключ -> `surveys.id`     |
| `question`  | TEXT    | текст вопроса                    |
| `answer`    | TEXT    | ответ                            |

Связи: один опрос - много вопросов и много ответов; один пользователь
- много ответов; каждый ответ относится к одному пользователю и одному
опросу. В JSON ответ ссылался на пользователя по `user_email`, в базе -
по `user_id`; импорт заменяет почту на идентификатор.

### Создание базы и импорт данных

Команды выполняются в PowerShell из корня проекта. Готовый файл базы
уже лежит в `data/`; команды нужны, чтобы создать базу заново.

```powershell
Remove-Item .\data\survey_service.sqlite
python -c "import sqlite3; sqlite3.connect('data/survey_service.sqlite').close()"
python -c "import sqlite3; conn=sqlite3.connect('data/survey_service.sqlite'); sql=open('sql/schema.sql', encoding='utf-8').read(); conn.executescript(sql); conn.commit(); conn.close()"
python -m db.import_json
```

Схема использует `CREATE TABLE IF NOT EXISTS`, поэтому её можно
выполнять повторно. Импорт очищает таблицы и заполняет их заново, в
одной транзакции: при ошибке выполняется `rollback()`. Порядок импорта:
пользователи, опросы с вопросами, ответы (сначала то, на что ссылаются
внешние ключи).

### Работа с базой из Python

* `db/database.py` - `get_connection()` (включает
  `PRAGMA foreign_keys = ON` и `row_factory = sqlite3.Row`),
  `fetch_all()`, `fetch_one()`;
* значения в SQL передаются только параметрами `?`:
  `conn.execute(sql, [topic])`; f-строки и конкатенация для подстановки
  значений не используются;
* поля результата доступны по именам: `row["title"]`,
  `{{ survey.title }}`.

### SQL-запросы (`sql/queries.sql`)

21 запрос, проверенный в SQLite; по комментариям видно, где каждый
используется.

| Вид                  | Запросы (номера в файле) | Где используются                       |
|----------------------|--------------------------|----------------------------------------|
| SELECT, списки       | 1, 2, 3                  | список пользователей, темы, вопросы    |
| WHERE                | 4-9                      | активные опросы, фильтр по теме, поиск доступных опросов (`NOT IN`) |
| JOIN                 | 10-12                    | ответы с пользователем и опросом       |
| Агрегатные функции   | 13-15                    | карточки на странице статистики        |
| GROUP BY, HAVING     | 16-20                    | опросы с числом вопросов, статистика, популярные опросы |
| ORDER BY, LIMIT      | 21                       | последние ответы                       |

Параметризованные запросы в приложении: тема (`?topic=`), пользователь
(`?user=`), порог `HAVING` (`?min=`), идентификаторы на страницах
`/surveys/<id>/` и `/responses/<id>/`.

### Страницы, получающие данные из SQLite

* `/surveys/` - опросы с числом вопросов (LEFT JOIN + GROUP BY), фильтр
  по теме;
* `/surveys/active/` - активные опросы (WHERE);
* `/surveys/available/` - поиск опросов, не пройденных выбранным
  пользователем (подзапрос NOT IN, параметр `?user=`);
* `/surveys/<id>/` - опрос, вопросы, статистика ответов (GROUP BY);
* `/responses/` и `/responses/<id>/` - ответы (JOIN трёх таблиц);
* `/responses/statistics/` - агрегатные функции, ответы по опросам,
  популярные опросы (HAVING), последние ответы (LIMIT).

Навигация: Главная | Опросы | Активные опросы | Ответы | Статистика;
поиск доступных опросов открывается со страницы «Опросы».

## Структура проекта

```text
survey-service/
├── README.md
├── requirements.txt
├── .flake8
├── manage.py
├── main.py                     консольная версия (ПР3)
├── storage.py                  загрузка и сохранение JSON
├── utils.py                    безопасный ввод (консоль)
├── survey_service/             пакет настроек Django-проекта
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── templates/                  шаблоны уровня проекта
│   ├── base.html
│   ├── 404.html
│   └── includes/
│       └── navigation.html
├── homepage/
│   ├── static/homepage/        css/style.css, js/main.js, img/logo.png
│   ├── templates/homepage/
│   │   └── index.html
│   ├── views.py
│   └── urls.py
├── surveys/
│   ├── templates/surveys/
│   │   ├── includes/
│   │   │   ├── survey_card.html
│   │   │   └── survey_status.html
│   │   ├── active_list.html
│   │   ├── available.html
│   │   ├── survey_detail.html
│   │   └── survey_list.html
│   ├── views.py
│   └── urls.py
├── responses/
│   ├── templates/responses/
│   │   ├── response_detail.html
│   │   ├── response_list.html
│   │   └── statistics.html
│   ├── views.py
│   └── urls.py
├── models/                     классы предметной области (ПР3)
│   ├── __init__.py
│   ├── questions.py
│   ├── surveys.py
│   ├── users.py
│   └── responses.py
├── db/                         работа с SQLite (ПР7)
│   ├── __init__.py
│   ├── database.py             подключение, fetch_all(), fetch_one()
│   └── import_json.py          перенос данных из JSON в SQLite
├── sql/
│   ├── schema.sql              создание таблиц
│   └── queries.sql             проверенные SQL-запросы
├── data/
│   ├── survey_service.sqlite   база данных SQLite
│   ├── surveys.json            исходные данные (JSON)
│   ├── users.json
│   └── responses.json
├── tests/
│   ├── test_surveys.py
│   ├── test_users.py
│   ├── test_responses.py
│   ├── test_web.py             страницы и 404 (ПР5)
│   ├── test_templates.py       шаблоны, include, static, URL (ПР6)
│   └── test_db.py              схема, импорт, запросы, страницы (ПР7)
├── legacy_pr2/                 старые модули ПР2 (не используются)
└── docs/
    ├── PR5_poyasneniya.md
    ├── PR6_poyasneniya.md
    └── PR7_poyasneniya.md
```

В каждом Django-приложении есть также `admin.py`, `apps.py`,
`models.py` (пока пустой), `tests.py`, `migrations/`. Пакет `models/` в
корне содержит классы предметной области, не Django-модели.

## Назначение модулей

* `main.py` - консольная версия приложения (сохранена с ПР3);
* `manage.py` - запуск команд управления Django;
* `survey_service/settings.py` - настройки проекта (в том числе
  `TEMPLATES` с `DIRS`, пути к JSON-файлам);
* `survey_service/urls.py` - маршруты верхнего уровня и `handler404`;
* `homepage/views.py` - `index()` и `page_not_found()`;
* `surveys/views.py` - `surveys()`, `active_surveys()`,
  `survey_detail()`, `available_surveys()` (SQL-запросы к SQLite);
* `responses/views.py` - `responses()`, `response_detail()`,
  `statistics()` (SQL-запросы к SQLite);
* `db/database.py`, `db/import_json.py` - подключение к SQLite и
  импорт данных из JSON;
* `models/` - классы `Question`, `Survey`, `User`, `Response` и функции
  работы с коллекциями (в том числе `find_survey_by_id()`,
  `find_response_by_id()`, `get_survey_statistics()`);
* `storage.py` - загрузка JSON в объекты и сохранение объектов в JSON;
* `utils.py` - функции консольного ввода;
* `tests/` - автоматические тесты.

## Хранение данных

Веб-интерфейс (ПР7) читает данные из SQLite (`data/survey_service.sqlite`),
см. раздел «База данных SQLite». JSON-файлы каталога `data/` остались
в проекте как исходные данные: из них база заполняется скриптом
`db/import_json.py`, ими же пользуется консольная версия (`main.py`,
`storage.py`). Веб-интерфейс только читает данные. Django ORM в
текущей версии проекта не используется.

## Установка и запуск

Windows (PowerShell), из корня проекта:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py check
python manage.py runserver
```

Файл базы данных `data/survey_service.sqlite` входит в проект. Если его
нужно создать заново, выполните команды из раздела «Создание базы и
импорт данных».

Веб-интерфейс: <http://127.0.0.1:8000/>

Проверка статики: `python manage.py findstatic homepage/img/logo.png`.
Консольная версия: `python main.py`.

### Проверка собственной страницы 404

При `DEBUG = True` Django показывает техническую страницу отладки.
Для проверки `handler404` в `survey_service/settings.py` временно
задайте `DEBUG = False`, перезапустите сервер и откройте
<http://127.0.0.1:8000/nonexistent/>. После проверки верните
`DEBUG = True`.

## Тестирование

```text
pytest -v
```

Тесты ПР3 проходят без изменений. `tests/test_web.py` и
`tests/test_templates.py` проверяют страницы, коды ответа, шаблоны,
`include`, статику, именованные URL и обработку пустых данных;
`tests/test_db.py` - схему и ключи, импорт из JSON (в том числе откат
при ошибке), все запросы из `sql/queries.sql`, параметризованные
запросы (защита от SQL-инъекций), страницы поиска и статистики. Тесты
работают с временной базой данных и не меняют `data/`.

## Проверка качества кода

```text
flake8 . --extend-exclude=venv
```

Конфигурация - в `.flake8`. Замечаний быть не должно.

## Git

Каждый коммит ПР7 начинается с метки `PR7:`.

```text
git status
git add .
git commit -m "PR7: add SQLite database and SQL queries"
git push
```

## Зависимости

* `Django==5.2.*`;
* `pytest`;
* `flake8`.

## Текущее состояние проекта

Реализовано: предметные классы `Question`, `Survey`, `User`,
`Response`; консольный интерфейс; Django-проект и приложения
`homepage`, `surveys`, `responses`; шаблоны Django Template Language;
статические файлы; **слой реляционного хранения (ПР7)**: база SQLite,
схема `sql/schema.sql`, импорт из JSON `db/import_json.py`, 21 SQL-запрос
в `sql/queries.sql`, получение данных в представлениях через `sqlite3`,
страницы списка и активных опросов, поиска доступных опросов,
ответов и статистики, навигация; тесты предметной области и
веб-интерфейса.

На ПР7 данные перенесены из JSON в базу данных SQLite:

* создана база `data/survey_service.sqlite`;
* таблицы созданы с помощью `sql/schema.sql`;
* данные перенесены скриптом `db/import_json.py`;
* SQL-запросы сохранены в `sql/queries.sql`;
* Django-представления получают данные из SQLite;
* страницы опросов, ответов, поиска доступных опросов и статистики
  работают с базой данных.

Не реализовано: формы Django, модели Django ORM и миграции для
предметной области (следующие практические работы); создание, изменение
и удаление объектов через веб; регистрация и авторизация.

## Дальнейшее развитие

Подключение базы данных к Django с использованием Django ORM; формы
Django и операции создания/изменения через веб (создание опроса,
прохождение опроса); регистрация и аутентификация; REST API;
контейнеризация и CI/CD.
