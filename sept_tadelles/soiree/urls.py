from django.urls import path

from . import views

app_name = "soiree"
urlpatterns = [
    path("list", views.list, name="list"),
    path("detail", views.detail, name="detail"),
    path("creation-1", views.creation_step_1, name="creation_step_1"),
    path("creation-2", views.creation_step_2, name="creation_step_2"),
    path("creation-3", views.creation_step_3, name="creation_step_3"),
    path("creation-4", views.creation_step_4, name="creation_step_4"),
    path("invites", views.change_invites, name="change_invites"),
    path("inscription", views.inscription, name="inscription"),
    path("desinscription", views.desinscription, name="desinscription"),
    path("delete", views.delete_soiree, name="delete_soiree"),
]