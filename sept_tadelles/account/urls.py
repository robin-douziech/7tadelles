from django.urls import path

from . import views

app_name = "account"
urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    path("", views.detail, name="detail"),
    path("update_pp/", views.update_profile_photo, name="update_profile_photo"),

    path("create/", views.create, name="user_creation_form"),
    path("verify_email/<str:user_id>/<str:token>/", views.verify_email, name="verify_email"),

    path("password_reset_email/", views.password_reset_email_form, name="password_reset_email"),
    path("password_reset/<str:user_id>/<str:token>/", views.password_reset_form, name="password_reset"),

    path("discord_verification_form/", views.discord_verification_form, name="discord_verification_form"),
    path("discord_verification/<str:user_id>/<str:token>", views.discord_verification, name="discord_verification"),
]