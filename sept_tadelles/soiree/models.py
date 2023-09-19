from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _

from account import models as account_models

# Create your models here.


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
        account_models.Lieu,
        verbose_name="Lieu",
        on_delete=models.CASCADE
    )

    date = models.DateTimeField(
        verbose_name="Date",
        null=True,
        blank=True
    )

    hote = models.ForeignKey(
        account_models.User,
        on_delete=models.CASCADE,
        related_name='soirees_hote'
    )

    invites = models.ManyToManyField(
        account_models.User,
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
        account_models.User,
        verbose_name="Notification send to",
        blank=True,
        related_name="invitations_received"
    )

    inscriptions = models.ManyToManyField(
        account_models.User,
        verbose_name="Inscriptions",
        blank=True,
        related_name="user_inscriptions"
    )

    def __str__(self) :
        return f"Soirée de {self.hote} du {self.date.day}/{self.date.month}/{self.date.year}"

	