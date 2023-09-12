from django.urls import path

from .views import soiree, lieu, user

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
    path("delete-adsress/", user.address_delete, name="delete_address"),

    # Lieu
    path("create-place/", lieu.create_lieu, name="create_lieu"),

    # Soiree
    path("create-event/step-1/", soiree.create_soiree_step_1, name="create_soiree_step_1"),
    path("create-event/step-2/<int:soiree_id>", soiree.create_soiree_step_2, name="create_soiree_step_2"),
    path("create-event/step-3/<int:soiree_id>", soiree.create_soiree_step_3, name="create_soiree_step_3"),
    path("create-event/step-4/<int:soiree_id>", soiree.create_soiree_step_4, name="create_soiree_step_4"),
    path("my-events/", soiree.my_events, name="my_events"),
    path("event/<int:soiree_id>/", soiree.event_detail, name="event_detail"),
    path("change-guests/<int:soiree_id>/", soiree.change_invites, name="change_invites"),
]