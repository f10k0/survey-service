"""Маршруты приложения surveys (префикс surveys/ задан в корне)."""

from django.urls import path

from . import views

app_name = "surveys"

urlpatterns = [
    path("", views.surveys, name="list"),
    path(
        "<int:survey_id>/",
        views.survey_detail,
        name="detail",
    ),
]
