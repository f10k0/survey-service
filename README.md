# Сервис проведения опросов

Приложение для создания опросов и сбора ответов. Консольная версия
(ПР3) дополнена веб-интерфейсом на Django (ПР5), страницы которого
построены на шаблонах Django Template Language (ПР6).

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
* просматривать список ответов пользователей и конкретный ответ;
* создавать опросы и регистрировать пользователей (консоль);
* проходить опросы с проверкой возраста и защитой от повторного
  участия (консоль);
* искать, фильтровать и сортировать опросы (консоль);
* хранить данные между запусками в JSON-файлах.

## Используемые технологии

* Python 3;
* Django 5.2;
* Django Template Language (DTL) - шаблоны страниц;
* HTML5, CSS3, JavaScript;
* Bootstrap 5.3 (CDN) и собственный CSS проекта;
* JSON для хранения данных;
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
Python-классы; Django ORM и база данных пока не используются.

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
│   │   ├── survey_detail.html
│   │   └── survey_list.html
│   ├── views.py
│   └── urls.py
├── responses/
│   ├── templates/responses/
│   │   ├── response_detail.html
│   │   └── response_list.html
│   ├── views.py
│   └── urls.py
├── models/                     классы предметной области (ПР3)
│   ├── __init__.py
│   ├── questions.py
│   ├── surveys.py
│   ├── users.py
│   └── responses.py
├── data/                       JSON-файлы данных
│   ├── surveys.json
│   ├── users.json
│   └── responses.json
├── tests/
│   ├── test_surveys.py
│   ├── test_users.py
│   ├── test_responses.py
│   ├── test_web.py             страницы и 404 (ПР5)
│   └── test_templates.py       шаблоны, include, static, URL (ПР6)
├── legacy_pr2/                 старые модули ПР2 (не используются)
└── docs/
    ├── PR5_poyasneniya.md
    └── PR6_poyasneniya.md
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
* `surveys/views.py` - `surveys()` и `survey_detail()`;
* `responses/views.py` - `responses()` и `response_detail()`;
* `models/` - классы `Question`, `Survey`, `User`, `Response` и функции
  работы с коллекциями (в том числе `find_survey_by_id()`,
  `find_response_by_id()`, `get_survey_statistics()`);
* `storage.py` - загрузка JSON в объекты и сохранение объектов в JSON;
* `utils.py` - функции консольного ввода;
* `tests/` - автоматические тесты.

## Хранение данных

Данные хранятся в JSON-файлах каталога `data/` (`surveys.json`,
`users.json`, `responses.json`). Загрузку выполняют функции
`storage.py`: JSON превращается в объекты `Survey`, `User`, `Response`.
Если у ответа в JSON нет поля `id`, оно назначается по порядку записи.
Веб-интерфейс только читает данные. Django ORM и база данных в текущей
версии проекта не используются.

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

Тесты ПР3 проходят без изменений; `tests/test_web.py` и
`tests/test_templates.py` проверяют страницы, коды ответа, шаблоны,
`include`, статику, именованные URL и обработку пустых данных.

## Проверка качества кода

```text
flake8 . --extend-exclude=venv
```

Конфигурация - в `.flake8`. Замечаний быть не должно.

## Git

Каждый коммит ПР6 начинается с метки `PR6:`.

```text
git status
git add .
git commit -m "PR6: add Django templates and static files"
git push
```

## Зависимости

* `Django==5.2.*`;
* `pytest`;
* `flake8`.

## Текущее состояние проекта

Реализовано: предметные классы `Question`, `Survey`, `User`,
`Response`; консольный интерфейс; хранение данных в JSON; Django-проект
и приложения `homepage`, `surveys`, `responses`; веб-представления;
Django Template Language: базовый шаблон, наследование, блоки,
включаемые шаблоны, контекст, циклы и условия, фильтры; именованные
URL и пространства имён; статические CSS, JavaScript и изображение;
собственное оформление поверх Bootstrap; тесты предметной области и
веб-интерфейса.

Не реализовано: формы Django, модели Django ORM и работа с базой данных
(относятся к следующим практическим работам); создание, изменение и
удаление объектов через веб; регистрация и авторизация.

## Дальнейшее развитие

Переход от JSON-хранилища к базе данных и Django ORM; формы Django и
операции создания/изменения через веб (создание опроса, прохождение
опроса); регистрация и аутентификация; REST API; контейнеризация и
CI/CD.
