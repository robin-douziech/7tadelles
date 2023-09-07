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

    path("discord_verification/", views.discord_verification_info, name="discord_verification_info"),
    path("discord_verification_send_email/<str:discord_name>/<str:discord_id>/<str:user_name>/<str:bot_token>", views.discord_verification_send_email, name="discord_verification_send_email"),
    path("discord_verification_link/<str:user_id>/<str:token>", views.discord_verification_link, name="discord_verification_link"),

]