from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.files.images import get_image_dimensions

from . import models


class LoginForm(forms.Form) :

	username = forms.CharField(max_length=50)
	password = forms.CharField(max_length=50, widget=forms.PasswordInput())



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

	def clean_email(self) :
		email = self.cleaned_data['email']

		for user in models.User.objects.all() :
			if user.email == email :
				raise ValidationError(_('Invalid email : An account already exists with this email'))

		return email

	def clean_username(self) :
		username = self.cleaned_data['username']

		for user in models.User.objects.all() :
			if user.username == username :
				raise ValidationError(_('Invalid username : Someone already has this username'))

		return username

	def clean_password2(self) :
		password1 = self.cleaned_data['password1']
		password2 = self.cleaned_data['password2']

		if password2 != password1 :
			raise ValidationError(_('Invalid password : passwords don\'t match'))

		return password2


class UpdateProfilePhotoForm(forms.ModelForm) :

	class Meta :
		model = models.User
		fields = ['profile_photo']

	def clean_profile_photo(self) :

		profile_photo = self.cleaned_data['profile_photo']
		width, height = get_image_dimensions(profile_photo)

		if height > 1024 or width > 1024 :
			raise ValidationError(_('Invalid dimensions'))

		return profile_photo
