"""Views приложения homepage: главная страница и страница 404."""

from __future__ import annotations

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def index(request: HttpRequest) -> HttpResponse:
    """Главная страница: HTML формирует шаблон homepage/index.html."""
    return render(request, "homepage/index.html")


def page_not_found(request: HttpRequest,
                   exception: Exception) -> HttpResponse:
    """Собственная страница 404 (handler404): шаблон 404.html."""
    return render(request, "404.html", status=404)
