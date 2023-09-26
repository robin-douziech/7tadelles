from django import forms

from . import models
from wiki import models as wiki_models
from account import models as account_models

class PartieCreationForm(forms.Form) :
	filter_horizontal = ('joueurs',)

	jeu = forms.ModelChoiceField(
		label = "Jeu",
		queryset = wiki_models.Game.objects.filter(ranking=True)
	)

	joueurs = forms.ModelMultipleChoiceField(
		label = "Joueurs",
		queryset = account_models.User.objects.filter(discord_verified=True),
		required = False
	)



class PartieClassementForm(forms.Form) :

	def __init__(self, request, partie, *args, **kwargs) :
		super(PartieClassementForm, self).__init__(*args, **kwargs)
		
		for i,joueur in enumerate(partie.joueurs.all()) :

			if joueur in partie.classement.all() :
				initial = models.PositionJoueur.objects.get(partie=partie, joueur=joueur).position
			else :
				initial = 1

			self.fields[f"{partie.joueurs.all()[i]}"] = forms.IntegerField(
				label=f"{partie.joueurs.all()[i]}",
				initial = initial,
				min_value = 1,
				max_value = len(partie.joueurs.all())
			)

