from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.utils.translation import gettext_lazy as _




def profile_photo_name(instance, filename) :
    return f"account/users/{instance.id}/profile_photo.png"

def cover_photo_name(instance, filename) :
    return f"account/users/{instance.id}/cover_photo.png"

def default_parameters() :
    default_parameters = {
        'type_soiree_view': 15,
        'type_soiree_notif': 15,
        'notif_mail': True,
    }
    return default_parameters






class Lieu(models.Model) :

    name = models.CharField(verbose_name="Nom du lieu", max_length=50, null=True, blank=True)

    adresse = models.CharField(verbose_name="Adresse", max_length=200, null=True, blank=True)
    complement = models.CharField(verbose_name="Complément d'adresse", max_length=50, null=True, blank=True)
    code_postal = models.CharField(verbose_name="Code postal", max_length=5, validators=[RegexValidator('^[0-9]{5}$')], null=True, blank=True)
    ville = models.CharField(verbose_name="Ville", max_length=50, null=True, blank=True)
    pays = models.CharField(verbose_name="Pays", max_length=50, null=True, blank=True)

    has_image = models.BooleanField(default=False)
    image = models.ImageField(verbose_name="Image", upload_to="photos/lieu/", null=True, blank=True)

    def __str__(self) :
        return self.name

class User(AbstractUser):

    has_cover_photo = models.BooleanField(default=False)
    cover_photo = models.ImageField(upload_to=cover_photo_name, null=True, blank=True)
    
    has_profile_photo = models.BooleanField(default=False)
    profile_photo = models.ImageField(upload_to=profile_photo_name, null=True, blank=True)

    verified = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=64, null=True, blank=True)
    password_reset_token = models.CharField(max_length=64, null=True, blank=True)

    discord_verified = models.BooleanField(default=False)
    discord_username = models.CharField(max_length=50, null=True, blank=True)
    discord_verification_token = models.CharField(max_length=64, null=True, blank=True)

    adresse = models.ForeignKey(Lieu, on_delete=models.SET_NULL, null=True, blank=True)

    lieus = models.ManyToManyField(
        Lieu,
        verbose_name="Lieux",
        blank=True,
        related_name="owners"
    )

    amis = models.ManyToManyField('self', blank=True)
    demandes_envoyees = models.ManyToManyField('self', symmetrical=False, blank=True, related_name="demandes_recues")

    parameters = models.JSONField(verbose_name = "Paramètres", default = default_parameters)

    def __str__(self) :
        return self.username







class Notification(models.Model) :

    users = models.ManyToManyField(
        User,
        verbose_name="Utilisateur ayant reçu la notification",
        blank=True,
        related_name='user_notifications'
    )

    title = models.CharField(
        verbose_name="Titre de la notification",
        max_length=50,
        null=True,
        blank=True
    )

    text = models.TextField(
        verbose_name="Texte de la notification",
        max_length=500,
        null=True,
        blank=True
    )

    link = models.CharField(
        verbose_name="vue pointée par la notification",
        max_length=50,
        null=True,
        blank=True
    )

    get_args = models.CharField(
        verbose_name="arguments GET de la vue pointée par la notification",
        max_length=50,
        null=True,
        blank=True
    )

    post_args = models.CharField(
        verbose_name="arguments POST de la vue pointée par la notification",
        max_length=50,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        verbose_name="Created at",
        null=True,
        blank=True
    )