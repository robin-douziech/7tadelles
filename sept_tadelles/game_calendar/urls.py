from django.urls import path

from . import views

app_name = "game_calendar"
urlpatterns = [
	path("", views.index, name="game_calendar_index")
]