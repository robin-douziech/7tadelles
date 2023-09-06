from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.files.images import get_image_dimensions

from . import models


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

class DiscordVerificationForm(forms.Form) :

	discord_username = forms.CharField(label="nom d'utilisateur discord", max_length=50)