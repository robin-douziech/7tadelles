from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.files.images import get_image_dimensions
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator


from . import models


"""
class LoginForm(forms.Form) :

	username = forms.CharField(label="nom d'utilisateur", max_length=50)
	password = forms.CharField(label="mot de passe", max_length=50, widget=forms.PasswordInput())


class PasswordResetEmailForm(forms.Form) :

	email = forms.EmailField()


class PasswordResetForm(forms.Form) :

	password1 = forms.CharField(max_length=50, widget=forms.PasswordInput())
	password2 = forms.CharField(max_length=50, widget=forms.PasswordInput())


class UserCreationForm(forms.Form) :

	username = forms.CharField(label="nom d'utilisateur", max_length=50)
	password1 = forms.CharField(label="mot de passe", max_length=50, widget=forms.PasswordInput())
	password2 = forms.CharField(label="confirmer le mot de passe", max_length=50, widget=forms.PasswordInput())
	email = forms.EmailField()


class UpdateProfilePhotoForm(forms.ModelForm) :

	class Meta :
		model = models.User
		fields = ['profile_photo']


class AddressForm(forms.Form) :

	adresse = forms.CharField(label="Adresse*", max_length=200)
	complement = forms.CharField(label="Complément d'adresse", max_length=200, required=False)
	code_postal = forms.CharField(label="Code postal*", max_length=5, validators=[RegexValidator('^[0-9]{5}$')])
	ville = forms.CharField(label="Ville*", max_length=50)
	pays = forms.CharField(label="Pays*", max_length=50)
	image = forms.ImageField(label="Photo", required=False)
"""




"""
class SoireeCreationForm_step_1(forms.Form) :

	type_soiree = forms.ChoiceField(
		label = "Type de soirée",
		choices = models.Soiree.TypeDeSoiree.choices,
		widget = forms.RadioSelect()
	)

class SoireeCreationForm_step_2(forms.Form) :

	nb_joueurs = forms.IntegerField(
		label = "Nombre maximal de joueurs (hôte compris)",
		validators = [MinValueValidator(2)],
		min_value = 2
	)

class SoireeCreationForm_step_3(forms.Form) :

	lieu = forms.ModelChoiceField(label="Lieu", queryset=models.Lieu.objects.all())

class SoireeCreationForm_step_4(forms.Form) :

	date = forms.DateTimeField(label="Date", widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
"""


"""
class LieuCreationForm(forms.Form) :

	name = forms.CharField(label="Nom du lieu*", max_length=50)

	adresse = forms.CharField(label="Adresse*", max_length=200)
	complement = forms.CharField(label="Complément d'adresse", max_length=200, required=False)
	code_postal = forms.CharField(label="Code postal*", max_length=5, validators=[RegexValidator('^[0-9]{5}$')])
	ville = forms.CharField(label="Ville*", max_length=50)
	pays = forms.CharField(label="Pays*", max_length=50)
	image = forms.ImageField(label="Photo", required=False)
"""

"""
class InvitesForm(forms.Form) :
	filter_horizontal = ('invites_to_add',)

	invites_to_add = forms.ModelMultipleChoiceField(
		label="Joueur(s) à inviter",
		queryset=None,
		required=False
	)
	
	invites_to_del = forms.ModelMultipleChoiceField(
		label="Invité(s) à supprimer",
		queryset=None,
		required=False
	)

	def __init__(self, request, soiree, *args, **kwargs) :
		super().__init__(*args, **kwargs)
		invites_to_add_queryset = models.User.objects.all()
		invites_to_add_queryset = invites_to_add_queryset.exclude(pk=request.user.id)
		invites_to_del_queryset = soiree.invites.all()
		for invite in soiree.invites.all() :
			invites_to_add_queryset = invites_to_add_queryset.exclude(pk=invite.id)

		self.fields['invites_to_add'].queryset = invites_to_add_queryset
		self.fields['invites_to_del'].queryset = invites_to_del_queryset
"""