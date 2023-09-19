from django.urls import path

from .views import lieu, user

app_name = "account"
urlpatterns = [

    # User
    path("login/", user.login_view, name="login"),
    path("logout/", user.logout_view, name="logout"),
    path("", user.detail, name="detail"),
    path("update_pp/", user.update_profile_photo, name="update_profile_photo"),
    path("delete_pp/", user.delete_profile_photo, name="delete_profile_photo"),
    path("create/", user.create, name="user_creation_form"),
    path("verify_email/<str:user_id>/<str:token>/", user.verify_email, name="verify_email"),
    path("password_reset_email/", user.password_reset_email_form, name="password_reset_email"),
    path("password_reset/<str:user_id>/<str:token>/", user.password_reset_form, name="password_reset"),
    path("discord_verification/", user.discord_verification_info, name="discord_verification_info"),
    path("discord_verification_send_email/<str:discord_name>/<str:discord_id>/<str:user_name>/<str:bot_token>", user.discord_verification_send_email, name="discord_verification_send_email"),
    path("discord_verification_link/<str:user_id>/<str:token>", user.discord_verification_link, name="discord_verification_link"),
    path("change-address/", user.address_form, name="change_address"),
    path("delete-adress/", user.address_delete, name="delete_address"),
    path("clear-session/", user.clear_session, name="clear_session"),
    path("retour/", user.retour, name="retour"),

    # recherche d'utilisateur
    path("user/list", user.search_user_form, name="search_user_form"),
    path("user/detail", user.user_detail, name="user_detail"),
    path("user/demande", user.demande_ami, name="demande_ami"),
    path("user/accepter", user.accepter_ami, name="accepter_ami"),
    path("user/refuser", user.refuser_ami, name="refuser_ami"),

    # ajouter jeu
    path("game/add", user.add_game, name="add_game"),

    # Lieu
    path("place/add", lieu.create_lieu, name="create_lieu"),
]