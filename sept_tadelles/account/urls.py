from django.urls import path

from .views import lieu, user, account

app_name = "account"
urlpatterns = [

    path("login/", account.login_view, name="login"),
    path("logout/", account.logout_view, name="logout"),

    path("user/detail", user.detail, name="detail"),
    path("user/list", user.list, name="list"),
    path("user/add", user.add_friend, name="add_friend"),
    path("user/accept", user.accept_friend, name="accept_friend"),
    path("user/refuse", user.refuse_friend, name="refuse_friend"),
    path("user/message", user.message_friend, name="message_friend"),



    path("user/add", account.create, name="user_creation_form"),
    path("verify_email/<str:user_id>/<str:token>/", account.verify_email, name="verify_email"),

    path("password_reset_email/", account.password_reset_email_form, name="password_reset_email"),
    path("password_reset/<str:user_id>/<str:token>/", account.password_reset_form, name="password_reset"),

    path("profile-photo/update", account.update_profile_photo, name="update_profile_photo"),
    path("profile-photo/delete", account.delete_profile_photo, name="delete_profile_photo"),

    path("cover-photo/update", account.update_cover_photo, name="update_cover_photo"),
    path("cover-photo/delete", account.delete_cover_photo, name="delete_cover_photo"),

    path("discord_verification/", account.discord_verification_info, name="discord_verification_info"),
    path("discord_verification_send_email/<str:discord_name>/<str:discord_id>/<str:user_name>/<str:bot_token>", account.discord_verification_send_email, name="discord_verification_send_email"),
    path("discord_verification_link/<str:user_id>/<str:token>", account.discord_verification_link, name="discord_verification_link"),
    
    path("address/update", account.address_form, name="change_address"),
    path("adress/delete", account.address_delete, name="delete_address"),



    # ajouter jeu
    path("game/add", account.add_game, name="add_game"),

    # Lieu
    path("place/add", lieu.create_lieu, name="create_lieu"),
]