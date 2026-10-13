# Сервис проведения опросов

Приложение для создания опросов и сбора ответов. Консольная версия
(ПР3) дополнена веб-интерфейсом на Django (ПР5).

## Назначение

Приложение позволяет:

* просматривать список опросов в браузере;
* просматривать информацию о конкретном опросе (вопросы, статус,
  статистика ответов);
* просматривать список ответов пользователей в браузере;
* просматривать информацию о конкретном ответе;
* создавать опросы и регистрировать пользователей (консоль);
* проходить опросы с проверкой возраста и защитой от повторного
  участия (консоль);
* искать, фильтровать и сортировать опросы (консоль);
* хранить данные между запусками в JSON-файлах.

## Используемые технологии

* Python 3;
* Django 5.2 - веб-фреймворк;
* HTML - разметка веб-страниц;
* CSS и Bootstrap 5.3 (подключение через CDN) - оформление страниц;
* pytest - автоматизированные тесты;
* flake8 - проверка качества кода.

## Целевая аудитория

Организаторы опросов, преподаватели, HR-специалисты, маркетологи -
все, кому нужно быстро собрать и обработать мнения аудитории.

## Предметная область

Опрос - набор вопросов по определённой теме, на которые пользователь
даёт ответы. Сервис хранит опросы, вопросы, пользователей и ответы,
проверяет допуск пользователей и формирует статистику.

Основные объекты предметной области: опрос, вопрос, пользователь,
ответ. Опрос содержит вопросы; ответ ссылается на опрос и пользователя.

## Основные сущности (пакет `models/`, ПР3)

### `Question` - вопрос опроса

Атрибуты: `text` - текст; `options` - список вариантов или `None`
(открытый вопрос).
Методы: `is_open()`, `validate_options()`, `from_data()`, `to_dict()`,
`__str__()`.

### `Survey` - опрос

Атрибуты: `id`, `title`, `topic`, `questions` (список `Question`),
`status`, `creation_date`.
Методы: `questions_count` (`@property`), `is_active()`,
`add_question()`, `from_data()`, `to_dict()`, `__str__()`.

### `User` - пользователь

Атрибуты: `id`, `name`, `email`, `age`, `is_registered`.
Методы: `is_adult()`, `from_data()`, `to_dict()`, `__str__()`.

### `Response` - ответ пользователя

Атрибуты: `id` (добавлен в ПР5 для адреса страницы ответа), `user`
(объект `User`), `survey` (объект `Survey`), `question`, `answer`.
Методы: `from_data()`, `to_dict()`, `__str__()`.

Связи между объектами сохраняются: `response.user.name`,
`response.survey.title`.

## Страницы веб-интерфейса

| Страница        | URL                     | View-функция                       |
|-----------------|-------------------------|------------------------------------|
| Главная         | `/`                     | `homepage.views.index`             |
| Список опросов  | `/surveys/`             | `surveys.views.surveys`            |
| Страница опроса | `/surveys/<int:id>/`    | `surveys.views.survey_detail`      |
| Список ответов  | `/responses/`           | `responses.views.responses`        |
| Страница ответа | `/responses/<int:id>/`  | `responses.views.response_detail`  |
| Ошибка 404      | любой несуществующий    | `homepage.views.page_not_found`    |

Если опрос или ответ с указанным идентификатором не найден, страница
возвращает код статуса 404 («Опрос не найден» / «Ответ не найден»).
Собственная страница 404 для несуществующих адресов подключена через
`handler404` (виден при `DEBUG = False`).

## Назначение основных view-функций

* `page(title, content)` (`homepage/views.py`) - единый HTML-каркас:
  кодировка, заголовок вкладки, Bootstrap 5.3, навигация, контейнер;
* `index()` - главная страница с описанием и кнопками-ссылками;
* `page_not_found()` - обработчик ошибки 404;
* `surveys()` - список опросов из `data/surveys.json`;
* `survey_detail()` - карточка опроса: вопросы, статус-бейдж,
  статистика (`find_survey_by_id()`, `get_survey_statistics()`);
* `responses()` - список ответов из `data/responses.json`;
* `response_detail()` - карточка ответа (`find_response_by_id()`).

HTML пока формируется прямо во view-функциях. Текст из данных
экранируется (`django.utils.html.escape`). В следующих работах каркас
будет перенесён в шаблоны Django (`templates/`).

## Хранение данных

Данные хранятся в JSON-файлах каталога `data/`:

* `surveys.json` - опросы с вопросами;
* `users.json` - пользователи;
* `responses.json` - ответы (связь через `user_email` и `survey_id`).

При загрузке JSON преобразуется в объекты `Survey`, `User`, `Response`,
при сохранении объекты преобразуются обратно в словари. Если у ответа в
JSON нет поля `id`, оно назначается по порядку записи (1, 2, 3, ...).
Веб-интерфейс только читает данные; переход на базу данных Django ORM
будет выполнен в следующих работах.

## Структура проекта

```text
survey-service/
├── README.md
├── requirements.txt
├── .flake8
├── manage.py
├── main.py                 консольная версия (ПР3)
├── storage.py              загрузка и сохранение JSON
├── utils.py                безопасный ввод (консоль)
├── survey_service/         пакет настроек Django-проекта
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── homepage/               приложение: главная, page(), 404
│   ├── views.py
│   └── urls.py
├── surveys/                приложение: опросы
│   ├── views.py
│   └── urls.py
├── responses/              приложение: ответы
│   ├── views.py
│   └── urls.py
├── models/                 классы предметной области (ПР3)
│   ├── __init__.py
│   ├── questions.py
│   ├── surveys.py
│   ├── users.py
│   └── responses.py
├── data/                   JSON-файлы данных
│   ├── surveys.json
│   ├── users.json
│   └── responses.json
├── tests/                  автотесты pytest
│   ├── test_surveys.py
│   ├── test_users.py
│   ├── test_responses.py
│   └── test_web.py         тесты веб-интерфейса (ПР5)
├── legacy_pr2/             старые модули ПР2 (не используются)
└── docs/
    └── PR5_poyasneniya.md  пояснения к защите ПР5
```

В каждом Django-приложении есть также `admin.py`, `apps.py`,
`models.py`, `tests.py`, `migrations/`; `models.py` приложений пока
пуст - Django-модели появятся в следующих работах. Не путать с пакетом
`models/` в корне: он содержит классы предметной области.

Старые модули ПР2 (`users.py`, `surveys.py`, `responses.py`) перенесены
в `legacy_pr2/`: их имена совпадают с именами Django-приложений
`surveys` и `responses`, и Django не позволил бы создать приложения.

## Назначение модулей

* `main.py` - консольная версия приложения (сохранена с ПР3);
* `manage.py` - запуск команд управления Django;
* `survey_service/settings.py` - настройки (INSTALLED_APPS, язык,
  часовой пояс, пути к JSON-файлам, DEBUG, ALLOWED_HOSTS);
* `survey_service/urls.py` - маршрутизация верхнего уровня, `handler404`;
* `homepage/`, `surveys/`, `responses/` - Django-приложения с
  view-функциями и собственными `urls.py`;
* `models/` - классы `Question`, `Survey`, `User`, `Response` и функции
  работы с коллекциями;
* `storage.py` - JSON <-> объекты Python;
* `tests/` - автоматические тесты.

## Функции проекта

Функции ПР3 (консоль): `add_survey`, `find_surveys`,
`filter_surveys_by_questions`, `sort_surveys`, `add_user`,
`find_user_by_email`, `add_response`, `is_user_participated`,
`get_survey_statistics`, `get_user_responses`.

Используются в веб-интерфейсе (ПР5): `load_surveys`, `load_users`,
`load_responses`, `find_survey_by_id`, `find_response_by_id`
(новая в ПР5), `get_survey_statistics`, `Survey.is_active()`.

Отложены до появления форм и POST-запросов: создание опроса,
регистрация пользователя, прохождение опроса, поиск, фильтрация и
сортировка опросов.

## Установка и запуск

Windows (PowerShell), из корня проекта:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m django --version
python manage.py migrate
python manage.py check
python manage.py runserver
```

Открыть в браузере: <http://127.0.0.1:8000/>

Проверяемые адреса: `/`, `/surveys/`, `/surveys/1/`, `/responses/`,
`/responses/1/`, а также несуществующие `/surveys/999/` и
`/responses/999/` (код 404).

Консольная версия: `python main.py`.

### Проверка собственной страницы 404

При `DEBUG = True` Django показывает техническую страницу отладки. Для
проверки `handler404` в `survey_service/settings.py` временно задайте
`DEBUG = False` (при этом `ALLOWED_HOSTS` уже содержит `localhost` и
`127.0.0.1`), перезапустите сервер и откройте
<http://127.0.0.1:8000/nonexistent/>. После проверки верните
`DEBUG = True`.

## Тестирование

```text
pytest -v
```

Тесты ПР3 проходят без изменений; добавлены тесты веб-страниц
(`tests/test_web.py`): коды ответа, динамические URL, 404, экранирование.

## Проверка качества кода

```text
flake8 .
```

Конфигурация - в `.flake8` (каталоги `.venv`, `venv`, `migrations`
исключены). Замечаний быть не должно.

## Git

Каждый коммит ПР5 начинается с метки `PR5:`.

```text
git status
git add .
git commit -m "PR5: add Django project and web pages"
git push
```

## Зависимости

* `Django==5.2.*` - веб-фреймворк;
* `pytest` - тесты;
* `flake8` - проверка кода.

## Текущее состояние и план развития

Реализовано (ПР5): Django-проект и три приложения (`homepage`,
`surveys`, `responses`); маршрутизация URL двух уровней; динамические
URL; view-функции; страницы списков и карточек; обработка 404;
навигация между страницами; оформление Bootstrap 5.3; консольная
версия, классы ПР3, JSON-хранилище и тесты сохранены.

Планируется: шаблоны Django и отказ от `page()`; перенос `Survey`,
`User`, `Response` в Django ORM и подключение базы данных; формы
создания и прохождения опросов; регистрация и авторизация; REST API;
контейнеризация и CI/CD.
