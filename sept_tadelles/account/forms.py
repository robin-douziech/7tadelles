from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.files.images import get_image_dimensions

from . import models


class LoginForm(forms.Form) :

	username = forms.CharField(label="Nom d'utilisateur", max_length=50)
	password = forms.CharField(label="Mot de passe", max_length=50, widget=forms.PasswordInput())



class PasswordResetEmailForm(forms.Form) :

	email = forms.EmailField()


class PasswordResetForm(forms.Form) :

	password1 = forms.CharField(max_length=50, widget=forms.PasswordInput())
	password2 = forms.CharField(max_length=50, widget=forms.PasswordInput())



class UserCreationForm(forms.Form) :

	username = forms.CharField(label="username", max_length=50)
	password1 = forms.CharField(label="password", max_length=50, widget=forms.PasswordInput())
	password2 = forms.CharField(label="confirm password", max_length=50, widget=forms.PasswordInput())
	email = forms.EmailField()


class UpdateProfilePhotoForm(forms.ModelForm) :

	class Meta :
		model = models.User
		fields = ['profile_photo']
