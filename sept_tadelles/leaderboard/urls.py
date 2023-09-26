from django.urls import path

from . import views

app_name = "leaderboard"
urlpatterns = [

	path("partie/create", views.partie_create, name="partie_create"),
	path("partie/list", views.partie_list, name="partie_list"),
	path("partie/detail", views.partie_detail, name="partie_detail"),
	path("partie/done", views.partie_terminer, name="partie_terminer"),
	path("partie/undo", views.partie_annuler, name="partie_annuler"),

	path('index', views.index, name="index"),
	path('reset-all-scores', views.reset_all_scores, name="reset_all_scores"),
]