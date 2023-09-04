from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse
from django.core.mail import send_mail

from django.contrib.auth.models import User
from django.conf import settings

from django.contrib.auth import authenticate, logout, login


import random
from PIL import Image
import os

from . import forms
from . import models

def generate_token(length) :

	alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

	token = ""
	for i in range(length) :
		token += alphabet[random.randint(0, len(alphabet)-1)]

	return token

def find_user_by_email(email) :

	for user in models.User.objects.all() :
		if user.email == email :
			return user

	return None

def find_photo_by_caption(caption) :

	for photo in models.ProfilePhoto.objects.all() :
		if photo.caption == caption :
			return photo

	return None

def delete_media_file(path) :
	try :
		if os.path.isfile(path) :
			os.remove(path)
			return True
		else :
			return False
	except Exception as e :
		print(f"Erreur lors de la suppression d'un fichier media : {str(e)}")
		return False





### LOGIN/LOGOUT



def login_view(request) :

	form = forms.LoginForm()
	auth_error = False
	unverified_user = False

	if request.method == "POST" :

		form = forms.LoginForm(request.POST)

		if form.is_valid() :

			user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])

			if user is not None and user.verified :
				login(request, user)
				return redirect('/')
			elif user is not None :
				unverified_user = True
			else :
				auth_error = True

	return render(request, 'account/registration/login.html', {'form': form, 'auth_error': auth_error, 'unverified_user': unverified_user})


def logout_view(request) :
	logout(request)
	return render(request, 'account/registration/logout.html')



### DETAIL ###



def detail(request) :

	default_profile_photo = False
	profile_photo = request.user.profile_photo
	if not(profile_photo) :
		default_profile_photo = True
	print(type(profile_photo))
	print(profile_photo)

	actions = [
		('Modifier la photo de profil', 'account:update_profile_photo', ()),
		('Modifier le mot de passe', 'account:password_reset_email', ())
	]

	return render(request, "account/detail/detail.html", {'profile_photo': profile_photo, 'actions': actions, 'default_profile_photo': default_profile_photo})


def update_profile_photo(request) :

	form = forms.UpdateProfilePhotoForm()

	if request.method == "POST" :

		form = forms.UpdateProfilePhotoForm(request.POST, request.FILES)

		if form.is_valid() :

			old_profile_photo = request.user.profile_photo

			if old_profile_photo :

				if not(delete_media_file(f"{settings.MEDIA_ROOT}{old_profile_photo.url}")) :
					send_mail(
						subject="Fichier mal supprimé sur le serveur",
						message=f"""
Une erreur est survenue lors de la suppression d'un fichier sur le serveur.

chemin vers le fichier : {settings.BASE_DIR}{old_profile_photo.url}
						""",
						from_email="info@7tadelles.com",
						recipient_list=["robin.douziech27@gmail.com"],
						fail_silently=False
					)

			request.user.profile_photo = form.cleaned_data['profile_photo']
			request.user.save()



			return redirect('/')

	return render(request, 'account/detail/update_profile_photo.html', {'form': form})



### ACCOUNT CREATION ###



def create(request) :

	form = forms.UserCreationForm()
	errors = {
		'email_already_used': [False, "Un compte est déjà associé à cette adresse e-mail"],
		'username_already_used': [False, "Ce nom d'utilisateur est déjà utilisé"],
		'passwords_dont_match': [False, "Les mots de passe ne sont pas identiques"]
	}

	if request.method == "POST" :

		form = forms.UserCreationForm(request.POST)

		if form.is_valid() :

			# on vérifie qu'aucun compte n'existe avec cet e-mail ou ce nom d'utilisateur
			for user in models.User.objects.all() :
				if user.email == form.cleaned_data['email'] :
					errors['email_already_used'][0] = True
				if user.username == form.cleaned_data['username'] :
					errors['username_already_used'][0] = True

			# on vérifie que les mots de passe sont identiques
			errors['passwords_dont_match'][0] = (form.cleaned_data['password1'] != form.cleaned_data['password2'])

			print(f"errors : {errors}")

			for error in errors :
				if errors[error][0] :
					return render(request, 'account/creation/creation_form.html', {'form': form, 'errors': errors})

			# aucune erreur : on crée l'utilisateur
			user = models.User.objects.create_user(form.cleaned_data['username'], form.cleaned_data['email'], form.cleaned_data['password1'])
			user.verification_token = generate_token(64)
			user.save()

			if settings.ENV == "PROD" :
				verification_link = f"https://7tadelles.com/account/verify_email/{user.id}/{user.verification_token}"
			else :
				verification_link = f"http://localhost:8000/account/verify_email/{user.id}/{user.verification_token}"

			send_mail(
    			subject="Activation de votre compte",
    			message=f"""Bonjour !

Quelqu'un tente de créer un compte sur le site 7tadelles.com avec votre adresse e-mail.
S'il s'agit bien de vous, veuillez cliquer sur le lien ci-dessous, sinon, ignorez ce mail.

Lien d'activation : {verification_link}""",
    			from_email="info@7tadelles.com",
    			recipient_list=[form.cleaned_data['email']],
    			fail_silently=False
    		)

			return render(request, 'account/creation/activation_email_sent.html', {})


	return render(request, "account/creation/creation_form.html", {"form": form, 'errors': errors})


def verify_email(request, user_id, token):

	try :
		user = models.User.objects.get(pk=user_id)
	except :
		user = None

	if user is not None and user.verification_token == token:
		user.verified = True
		user.verification_token = ""
		user.save()
		return render(request, 'account/creation/activation_success.html', {})
	else:
		return render(request, 'account/creation/activation_error.html', {})



### PASSWORD RESET ###

def password_reset_email_form(request) :

	form = forms.PasswordResetEmailForm()
	errors = {
		'unknown_email': [False, "Aucun compte n'a été trouvé avec cette adresse e-mail."]
	}

	if request.method == "POST" :

		form = forms.PasswordResetEmailForm(request.POST)

		if form.is_valid() :

			user = find_user_by_email(form.cleaned_data['email'])
			if user is None :
				errors['unknown_email'][0] = True

			email = user.email

	elif request.user.is_authenticated :

		user = request.user
		email = user.email

	for error in errors :
		if errors[error][0] :
			return render(request, 'account/password_reset/password_reset_email_form.html', {'form': form, 'errors': errors})

	if (request.method == "POST" and form.is_valid()) or request.user.is_authenticated :

		user.password_reset_token = generate_token(64)
		user.save()

		if settings.ENV == "PROD" :
			verification_link = f"https://7tadelles.com/account/password_reset/{user.id}/{user.password_reset_token}/"
		else :
			verification_link = f"http://localhost:8000/account/password_reset/{user.id}/{user.password_reset_token}/"

		send_mail(
			subject="Réinitialisation de votre mot de passe",
			message=f"""
Bonjour !

Quelqu'un a demandé la réinitialisation du mot de passe du compte lié à votre adresse e-mail sur 7tadelles.com.
Si ce n'est pas vous, ignorez ce message. Sinon, cliquez sur le lien ci-dessous pour réinitialiser votre mot de passe.

{verification_link}
				""",
			from_email="info@7tadelles.com",
			recipient_list=[email],
			fail_silently=False
		)

		return render(request, 'account/password_reset/password_reset_email_sent.html', {})

	return render(request, 'account/password_reset/password_reset_email_form.html', {'form': form, 'errors': errors})





def password_reset_form(request, user_id, token) :

	passwords_dont_match = False

	try :
		user = models.User.objects.get(pk=user_id)
	except :
		user = None

	if user is not None and user.password_reset_token == token :

		form = forms.PasswordResetForm()

		if request.method == "POST" :

			form = forms.PasswordResetForm(request.POST)

			if form.is_valid() :

				if form.cleaned_data['password1'] == form.cleaned_data['password2'] :

					user.set_password(form.cleaned_data['password1'])
					user.password_reset_token = ""
					user.save()

					return render(request, 'account/password_reset/password_reset_complete.html', {})

				else :

					passwords_dont_match = True

		return render(request, 'account/password_reset/password_reset_confirm.html', {'form': form, 'passwords_dont_match': passwords_dont_match})

	else :

		return render(request, 'account/password_reset/password_reset_bad_link.html')








