from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.utils.translation import gettext_lazy as _













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
    
    has_profile_photo = models.BooleanField(default=False)
    profile_photo = models.ImageField(upload_to='photos/user/', null=True, blank=True)

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

    def __str__(self) :
        return self.username

'''
class Soiree(models.Model) :

    class TypeDeSoiree(models.TextChoices) :
        PRIV_INVIT_CONFIRM = "PRIV_I_C", _("Privée avec liste d'invités"),
        PRIV_LIST_INSC     = "PRIV_L_I", _("Privée sur inscription")
        PUB_INSC           = "PUB_I",    _("Publique sur inscription")
        PUB                = "PUB",      _("Publique")

    TYPES_SOIREE_DESC = {
        "PRIV_I_C": """
        Les soirées privées avec liste d'invités sont des soirées avec liste exhaustive d'invités.\
        Tous les invités peuvent y participer s'ils le souhaitent, il y a autant de places que d'invités.""",
        "PRIV_L_I" : """
        Les soirées privées sur inscription sont des soirées avec moins de places que d'invités.\
        Elles possèdent une liste d'invités. Les invités peuvent s'inscrire à la soirée pour y participer tant qu'il reste des places.""",
        "PUB_I" : """
        Les soirées publiques sur inscription sont des soirées sans liste d'invités (donc accessibles à tout le monde)\
        mais avec un nombre limité de places. Tout le monde peut s'y inscrire tant qu'il reste des places.""",
        "PUB" : """
        Les soirées publiques sont des soirées sans liste d'invité et sans nombre maximum de participants.\
        Tout le monde peut s'y inscrire sans limite de place."""
    }

    type_soiree = models.CharField(
        verbose_name = "Type de soirée",
        max_length = 8,
        choices = TypeDeSoiree.choices,
        default = TypeDeSoiree.PRIV_INVIT_CONFIRM
    )

    nb_joueurs = models.IntegerField(
        verbose_name = "Nombre maximal de joueurs (hôte compris)",
        validators = [MinValueValidator(2)],
        default = 2
    )

    lieu = models.ForeignKey(
        Lieu,
        verbose_name="Lieu",
        on_delete=models.CASCADE
    )

    date = models.DateTimeField(
        verbose_name="Date",
        null=True,
        blank=True
    )

    hote = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='soirees_hote'
    )

    invites = models.ManyToManyField(
        User,
        blank=True,
        related_name='invitations'
    )

    has_image = models.BooleanField(default=False)
    image = models.ImageField(
        verbose_name="Image",
        upload_to="photos/soiree/",
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        verbose_name="Created at",
        null=True,
        blank=True
    )

    notification_send_to = models.ManyToManyField(
        User,
        verbose_name="Notification send to",
        blank=True,
        related_name="invitations_received"
    )

    inscriptions = models.ManyToManyField(
        User,
        verbose_name="Inscriptions",
        blank=True,
        related_name="user_inscriptions"
    )

    def __str__(self) :
        return f"Soirée de {self.hote} du {self.date.day}/{self.date.month}/{self.date.year}"
'''






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

    args = models.CharField(
        verbose_name="arguments de la vue pointée par la notification",
        max_length=50,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        verbose_name="Created at",
        null=True,
        blank=True
    )