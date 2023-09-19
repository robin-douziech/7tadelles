from django import forms
from django.core.validators import MinValueValidator

import datetime as dt

from account import models as account_models

from . import models


class CreationForm_step_1(forms.Form) :

	type_soiree = forms.ChoiceField(
		label = "Type de soirée",
		choices = models.Soiree.TypeDeSoiree.choices,
		initial = models.Soiree.TypeDeSoiree.PRIV_INVIT_CONFIRM,
		widget = forms.RadioSelect()
	)

	def __init__(self, request, *args, **kwargs) :
		super(CreationForm_step_1, self).__init__(*args, **kwargs)

class CreationForm_step_2(forms.Form) :

	nb_joueurs = forms.IntegerField(
		label = "Nombre maximal de joueurs (hôte compris)",
		validators = [MinValueValidator(2)],
		initial = models.Soiree()._meta.get_field('nb_joueurs').default,
		min_value = 2
	)

	def __init__(self, request, *args, **kwargs) :
		super(CreationForm_step_2, self).__init__(*args, **kwargs)

class CreationForm_step_3(forms.Form) :

	lieu = forms.ModelChoiceField(
		label="Lieu",
		queryset=account_models.Lieu.objects.all()
	)

	def __init__(self, request, *args, **kwargs) :
		super(CreationForm_step_3, self).__init__(*args, **kwargs)
		self.fields['lieu'].queryset = request.user.lieus.all()
		self.fields['lieu'].initial = request.user.adresse

class CreationForm_step_4(forms.Form) :

	date = forms.DateTimeField(
		label="Date",
		initial = dt.datetime.now() + dt.timedelta(days=1),
		widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
	)

	def __init__(self, request, *args, **kwargs) :
		super(CreationForm_step_4, self).__init__(*args, **kwargs)

class InvitesForm(forms.Form) :
	filter_horizontal = ('invites_to_add',)

	invites_to_add = forms.ModelMultipleChoiceField(
		label="Joueur(s) à inviter",
		queryset=None,
		required=False
	)

	def __init__(self, request, soiree, *args, **kwargs) :
		super(InvitesForm, self).__init__(*args, **kwargs)
		invites_to_add_queryset = request.user.amis.all()
		for invite in soiree.invites.all() :
			invites_to_add_queryset = invites_to_add_queryset.exclude(pk=invite.id)

		self.fields['invites_to_add'].queryset = invites_to_add_queryset


class SoireeForm(forms.Form) :

	type_soiree = forms.ChoiceField(
		label = "Type de soirée",
		choices = models.Soiree.TypeDeSoiree.choices,
		widget = forms.RadioSelect()
	)

	nb_joueurs = forms.IntegerField(
		label = "Nombre maximal de joueurs (hôte compris)",
		validators = [MinValueValidator(2)],
		min_value = 2
	)

	lieu = forms.ModelChoiceField(
		label="Lieu",
		queryset=account_models.Lieu.objects.all()
	)

	date = forms.DateTimeField(
		label="Date",
		widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
	)

	def __init__(self, request, soiree, *args, **kwargs) :
		super(SoireeForm, self).__init__(*args, **kwargs)
		self.fields['type_soiree'].initial = soiree.type_soiree
		self.fields['nb_joueurs'].initial = soiree.nb_joueurs
		self.fields['lieu'].initial = soiree.lieu
		self.fields['date'].initial = soiree.date

		self.fields['lieu'].queryset = request.user.lieus.all()