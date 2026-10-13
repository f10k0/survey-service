"""Views главной страницы и общий HTML-каркас всех страниц."""

from __future__ import annotations

from django.http import HttpRequest, HttpResponse
from django.utils.html import escape


def page(title: str, content: str) -> str:
    """Собрать HTML-документ с общим каркасом.

    title - заголовок вкладки (обычный текст, экранируется);
    content - готовый HTML-фрагмент страницы.
    """
    bootstrap = (
        "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3"
        "/dist/css/bootstrap.min.css"
    )
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, initial-scale=1">
    <title>{escape(title)}</title>
    <link rel="stylesheet" href="{bootstrap}">
</head>
<body>
    <nav class="nav container mt-3 mb-3">
        <a class="nav-link" href="/">Главная</a>
        <a class="nav-link" href="/surveys/">Опросы</a>
        <a class="nav-link" href="/responses/">Ответы</a>
    </nav>
    <main class="container">{content}</main>
</body>
</html>"""


def index(request: HttpRequest) -> HttpResponse:
    """Главная страница: описание сервиса и навигация."""
    content = """
    <h1 class="display-4">Сервис проведения опросов</h1>
    <p class="lead">
        Приложение для создания опросов и сбора ответов.
    </p>
    <p>Основные разделы:</p>
    <a href="/surveys/" class="btn btn-primary me-2">Опросы</a>
    <a href="/responses/" class="btn btn-secondary">Ответы</a>
    """
    return HttpResponse(page("Сервис опросов", content))


def page_not_found(request: HttpRequest,
                   exception: Exception) -> HttpResponse:
    """Собственная страница 404 (handler404)."""
    content = """
    <h1 class="text-danger">404 - страница не найдена</h1>
    <p>Проверьте адрес или вернитесь на главную.</p>
    <a href="/" class="btn btn-primary">На главную</a>
    """
    return HttpResponse(
        page("404 - страница не найдена", content),
        status=404,
    )
