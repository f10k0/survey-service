"""Корневая маршрутизация Django-проекта."""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("surveys/", include("surveys.urls")),
    path("responses/", include("responses.urls")),
]

# Обработчик 404 читается только из корневого urls.py и действует
# для всех приложений сразу (работает при DEBUG = False).
handler404 = "homepage.views.page_not_found"
