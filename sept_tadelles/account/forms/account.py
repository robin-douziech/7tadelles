from django import forms
from django.core.validators import RegexValidator

from account import models

class LoginForm(forms.Form) :
	username = forms.CharField(label="nom d'utilisateur", max_length=50)
	password = forms.CharField(label="mot de passe", max_length=50, widget=forms.PasswordInput())

class UserCreationForm(forms.Form) :
	username = forms.CharField(label="nom d'utilisateur", max_length=50)
	password1 = forms.CharField(label="mot de passe", max_length=50, widget=forms.PasswordInput())
	password2 = forms.CharField(label="confirmer le mot de passe", max_length=50, widget=forms.PasswordInput())
	email = forms.EmailField()

class PasswordResetEmailForm(forms.Form) :
	email = forms.EmailField()

class PasswordResetForm(forms.Form) :
	password1 = forms.CharField(max_length=50, widget=forms.PasswordInput())
	password2 = forms.CharField(max_length=50, widget=forms.PasswordInput())

class AddressForm(forms.Form) :
	adresse = forms.CharField(label="Adresse*", max_length=200)
	complement = forms.CharField(label="Complément d'adresse", max_length=200, required=False)
	code_postal = forms.CharField(label="Code postal*", max_length=5)
	ville = forms.CharField(label="Ville*", max_length=50)
	pays = forms.CharField(label="Pays*", max_length=50)
	image = forms.ImageField(label="Photo", required=False)

class UpdateProfilePhotoForm(forms.ModelForm) :

	profile_photo = forms.ImageField(
		label = "Photo de profil",
	)

class UpdateCoverPhotoForm(forms.ModelForm) :

	cover_photo = forms.ImageField(
		label = "Photo de couverture",
	)