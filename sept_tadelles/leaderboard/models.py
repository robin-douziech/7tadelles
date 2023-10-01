from django.db import models

from wiki import models as wiki_models

from account import models as account_models



class Partie(models.Model) :

	creator = models.ForeignKey(
		account_models.User,
		related_name = "parties_owned",
		on_delete = models.SET_NULL,
		null=True,
		blank = True
	)

	jeu = models.ForeignKey(
		wiki_models.Game,
		verbose_name = "Jeu",
		on_delete = models.CASCADE
	)

	joueurs = models.ManyToManyField(
		account_models.User,
		related_name = "parties",
		blank = True
	)

	classement = models.ManyToManyField(
		account_models.User,
		through = 'PositionJoueur',
		blank = True
	)

	finie = models.BooleanField(default=False)

	current_month = models.BooleanField(default=True)

	created_at = models.DateTimeField(
        verbose_name="Created at",
        null=True,
        blank=True
    )




class PositionJoueur(models.Model) :

	positionjoueur_id = models.BigAutoField(primary_key=True)

	joueur = models.ForeignKey(
		account_models.User,
		on_delete = models.CASCADE,
		related_name = 'position'
	)

	partie = models.ForeignKey(
		Partie,
		on_delete = models.CASCADE
	)

	position = models.PositiveIntegerField()
