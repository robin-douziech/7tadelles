from django.urls import path

from .views import lieu, user, account, parameters, bot

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

    path("user/create", account.create, name="user_creation_form"),
    path("verify-email/<str:user_id>/<str:token>/", account.verify_email, name="verify_email"),

    path("password-reset-email/", account.password_reset_email_form, name="password_reset_email"),
    path("password-reset/<str:user_id>/<str:token>/", account.password_reset_form, name="password_reset"),

    path("discord-verification-send-email/<str:discord_name>/<str:discord_id>/<str:user_name>/<str:bot_token>", account.discord_verification_send_email, name="discord_verification_send_email"),
    path("discord-verification-link/<str:user_id>/<str:token>", account.discord_verification_link, name="discord_verification_link"),

    path("parameters", parameters.base, name="parameters_base"),
    path("parameters/profile", parameters.profile, name="parameters_profile"),
    path("parameters/address", parameters.address, name="parameters_address"),
    path("parameters/address/delete", parameters.delete_address, name="parameters_delete_address"),
    path("parameters/type-soiree", parameters.type_soiree, name="parameters_type_soiree"),
    path("parameters/notif-mail", parameters.notif_mail, name="parameters_notif_mail"),
    path("parameters/delete-profile-photo", parameters.delete_profile_photo, name="delete_profile_photo"),
    path("parameters/delete-cover-photo", parameters.delete_cover_photo, name="delete_cover_photo"),



    path("bot/get-ranking-games/<str:bot_token>", bot.get_ranking_games, name="get_ranking_games"),
    path("bot/get-classement/<str:bot_token>", bot.get_classement, name="get_classement"),
    path("bot/get-score/<str:bot_token>", bot.get_score, name="get_score"),
    path("bot/month-end-validation/<str:bot_token>", bot.month_end_validation, name="month_end_validation"),



    # ajouter jeu
    path("game/add", account.add_game, name="add_game"),

    # Lieu
    path("place/add", lieu.create_lieu, name="create_lieu"),

    path("clean-session", account.clean_session, name="clean_session"),
    path("retour1", account.retour1, name="retour1"),
    path("retour2", account.retour2, name="retour2"),
]