"""Маршруты приложения surveys (префикс surveys/ задан в корне)."""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.surveys, name="surveys"),
    path(
        "<int:survey_id>/",
        views.survey_detail,
        name="survey_detail",
    ),
]
