from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.mail import send_mail
from django.core.files.images import get_image_dimensions
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout, login
from django.conf import settings
from django.urls import reverse

import re

from wiki import forms as wiki_forms
from wiki import models as wiki_models

from account import models
from account.forms import account as forms
from . import helpers


def login_view(request) :

	current_view = ['account:login', []]
	real_view = False

	form = forms.LoginForm()
	errors = {
		'errors_count': 0,
		'auth_error': [False, "Ce nom d'utilisateur et ce mot de passe ne correspondent pas, veuillez réessayer."],
		'unverified_user': [False, "Veuillez activer votre compte avant de vous connecter."],
	}

	if request.method == "POST" :

		form = forms.LoginForm(request.POST)

		if form.is_valid() :

			user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])

			if user is not None and user.verified :
				login(request, user)
				helpers.clean_user(user)
				helpers.register_view(request, current_view, real_view)
				return redirect('welcome:index')
			elif user is not None :
				errors['unverified_user'][0] = True
			else :
				errors['auth_error'][0] = True

	errors.pop('errors_count')
	helpers.register_view(request, current_view, real_view)
	return render(request, 'account/registration/login.html', {'form': form, 'errors': errors})

def logout_view(request) :
	current_view = ['account:logout', []]
	real_view = False
	logout(request)
	helpers.register_view(request, current_view, real_view)
	return render(request, 'account/registration/logout.html')

@login_required
def update_profile_photo(request) :

	current_view = ['account:update_profile_photo', []]
	real_view = False

	form = forms.UpdateProfilePhotoForm()
	if request.method == "POST" :
		form = forms.UpdateProfilePhotoForm(request.POST, request.FILES)
		if form.is_valid() :
			if request.user.has_profile_photo :
				if not(helpers.delete_media_file(f"{settings.MEDIA_ROOT}{request.user.profile_photo.url[1:].split('/',1)[1]}")) :
					send_mail(
						subject="Fichier mal supprimé sur le serveur",
						message=f"Une erreur est survenue lors de la suppression d'un fichier sur le serveur.\n\nChemin vers le fichier : {settings.MEDIA_ROOT}{request.user.profile_photo.url[1:].split('/',1)[1]}",
						from_email="info@7tadelles.com",
						recipient_list=["robin.douziech27@gmail.com"],
						fail_silently=False
					)		
			request.user.profile_photo = form.cleaned_data['profile_photo']
			request.user.has_profile_photo = True
			request.user.save()
			return redirect(f"{reverse('account:detail')}?id={request.user.id}")

	helpers.register_view(request, current_view, real_view)
	return render(request, 'account/account/profile_photo.html', {'form': form})

@login_required
def delete_profile_photo(request) :

	current_view = ['account:delete_profile_photo', []]
	real_view = False

	if request.user.has_profile_photo :

		if not(helpers.delete_media_file(f"{settings.MEDIA_ROOT}{request.user.profile_photo.url[1:].split('/',1)[1]}")) :
			send_mail(
				subject="Fichier mal supprimé sur le serveur",
				message=f"Une erreur est survenue lors de la suppression d'un fichier sur le serveur.\n\nChemin vers le fichier : {settings.MEDIA_ROOT}{request.user.profile_photo.url[1:].split('/',1)[1]}",
				from_email="info@7tadelles.com",
				recipient_list=["robin.douziech27@gmail.com"],
				fail_silently=False
			)

		request.user.has_profile_photo = False
		request.user.profile_photo = None
		request.user.save()

	return redirect(f"{reverse('account:detail')}?id={request.user.id}")

@login_required
def update_cover_photo(request) :

	current_view = ['account:update_cover_photo', []]
	real_view = False

	form = forms.UpdateCoverPhotoForm()
	if request.method == "POST" :
		form = forms.UpdateCoverPhotoForm(request.POST, request.FILES)
		if form.is_valid() :
			if request.user.has_cover_photo :
				if not(helpers.delete_media_file(f"{settings.MEDIA_ROOT}{request.user.cover_photo.url[1:].split('/',1)[1]}")) :
					send_mail(
						subject="Fichier mal supprimé sur le serveur",
						message=f"Une erreur est survenue lors de la suppression d'un fichier sur le serveur.\n\nChemin vers le fichier : {settings.MEDIA_ROOT}{request.user.cover_photo.url[1:].split('/',1)[1]}",
						from_email="info@7tadelles.com",
						recipient_list=["robin.douziech27@gmail.com"],
						fail_silently=False
					)
			request.user.cover_photo = form.cleaned_data['cover_photo']
			request.user.has_cover_photo = True
			request.user.save()
			return redirect(f"{reverse('account:detail')}?id={request.user.id}")

	helpers.register_view(request, current_view, real_view)
	return render(request, 'account/account/cover_photo.html', {'form': form})

@login_required
def delete_cover_photo(request) :

	current_view = ['account:delete_cover_photo', []]
	real_view = False

	if request.user.has_cover_photo :

		if not(helpers.delete_media_file(f"{settings.MEDIA_ROOT}{request.user.cover_photo.url[1:].split('/',1)[1]}")) :
			send_mail(
				subject="Fichier mal supprimé sur le serveur",
				message=f"Une erreur est survenue lors de la suppression d'un fichier sur le serveur.\n\nChemin vers le fichier : {settings.MEDIA_ROOT}{request.user.cover_photo.url[1:].split('/',1)[1]}",
				from_email="info@7tadelles.com",
				recipient_list=["robin.douziech27@gmail.com"],
				fail_silently=False
			)

		request.user.has_cover_photo = False
		request.user.cover_photo = None
		request.user.save()

	return redirect(f"{reverse('account:detail')}?id={request.user.id}")

def create(request) :

	current_view = ['account:user_creation_form', []]
	real_view = False

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
					helpers.register_view(request, current_view, real_view)
					return render(request, 'account/creation/creation_form.html', {'form': form, 'errors': errors})

			# aucune erreur : on crée l'utilisateur
			user = models.User.objects.create_user(form.cleaned_data['username'], form.cleaned_data['email'], form.cleaned_data['password1'])
			user.verification_token = helpers.generate_token(64)
			user.save()

			if settings.ENV == "PROD" :
				verification_link = f"https://7tadelles.com/account/verify_email/{user.id}/{user.verification_token}"
			else :
				verification_link = f"http://localhost:8000/account/verify_email/{user.id}/{user.verification_token}"
				print(verification_link)

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

			helpers.register_view(request, current_view, real_view)
			return render(request, 'account/creation/activation_email_sent.html', {})

	helpers.register_view(request, current_view, real_view)
	return render(request, "account/creation/creation_form.html", {"form": form, 'errors': errors})

def verify_email(request, user_id, token):

	current_view = ['account:verify_email', [user_id, token]]
	real_view = False

	try :
		user = models.User.objects.get(pk=user_id)
	except :
		user = None

	if user is not None and user.verification_token == token:
		user.verified = True
		user.verification_token = ""
		user.save()
		helpers.register_view(request, current_view, real_view)
		return render(request, 'account/creation/activation_success.html', {})
	else:
		helpers.register_view(request, current_view, real_view)
		return render(request, 'account/creation/activation_error.html', {})

def password_reset_email_form(request) :

	current_view = ['account:password_reset_email', []]
	real_view = False

	form = forms.PasswordResetEmailForm()
	errors = {
		'unknown_email': [False, "Aucun compte n'a été trouvé avec cette adresse e-mail."]
	}

	if request.method == "POST" :

		form = forms.PasswordResetEmailForm(request.POST)

		if form.is_valid() :

			user = helpers.find_user_by_email(form.cleaned_data['email'])
			if user is None :
				errors['unknown_email'][0] = True

			email = user.email

	elif request.user.is_authenticated :

		user = request.user
		email = user.email

	for error in errors :
		if errors[error][0] :
			helpers.register_view(request, current_view, real_view)
			return render(request, 'account/password_reset/password_reset_email_form.html', {'form': form, 'errors': errors})

	if (request.method == "POST" and form.is_valid()) or request.user.is_authenticated :

		user.password_reset_token = helpers.generate_token(64)
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

		helpers.register_view(request, current_view, real_view)
		return render(request, 'account/password_reset/password_reset_email_sent.html', {})

	helpers.register_view(request, current_view, real_view)
	return render(request, 'account/password_reset/password_reset_email_form.html', {'form': form, 'errors': errors})

def password_reset_form(request, user_id, token) :

	current_view = ['account:password_reset', [user_id, token]]
	real_view = False

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

					helpers.register_view(request, current_view, real_view)
					return render(request, 'account/password_reset/password_reset_complete.html', {})

				else :

					passwords_dont_match = True

		helpers.register_view(request, current_view, real_view)
		return render(request, 'account/password_reset/password_reset_confirm.html', {'form': form, 'passwords_dont_match': passwords_dont_match})

	else :

		helpers.register_view(request, current_view, real_view)
		return render(request, 'account/password_reset/password_reset_bad_link.html')

@login_required
def discord_verification_info(request) :

	current_view = ['account:discord_verification_info', []]
	real_view = False

	if request.user.discord_verified :
		helpers.register_view(request, current_view, real_view)
		return redirect(f"{reverse('account:detail')}?id={request.user.id}")
	else :
		helpers.register_view(request, current_view, real_view)
		return render(request, 'account/discord_verification/info.html', {})

def discord_verification_send_email(request, discord_name, discord_id, user_name, bot_token) :

	current_view = ['account:discord_verification_send_email', [discord_name, discord_id, user_name, bot_token]]
	real_view = False

	if bot_token != settings.BOT_TOKEN :
		helpers.register_view(request, current_view, real_view)
		return redirect('welcome:index')
	else :

		try :
			user = models.User.objects.get(username=user_name)
		except :
			user = None

		if user is not None and not(user.discord_verified) :

			token = helpers.generate_token(64)
			user.discord_verification_token = token
			user.discord_username = f"{discord_name}#{discord_id}"
			user.save()

			if settings.ENV == "PROD" :
				verification_link = f"https://7tadelles.com/account/discord_verification_link/{user.id}/{token}"
			else :
				verification_link = f"http://localhost:8000/account/discord_verification_link/{user.id}/{token}"

			send_mail(
				subject="Lien avec votre compte discord",
				message=f"""
Bonjour,

Quelqu'un tente de lier un compte discord ({user.discord_username}) à votre compte sur 7tadelles.com.
Si ce n'est pas vous, veuillez ignorer ce message. Sinon, veuillez cliquer sur le lien ci-dessous pour lier votre compte discord.

{verification_link}
				""",
				from_email = "info@7tadelles.com",
				recipient_list = [user.email],
				fail_silently = False
			)

			helpers.register_view(request, current_view, real_view)
			return JsonResponse({'result': 'success'})

		else :

			helpers.register_view(request, current_view, real_view)
			return JsonResponse({'result': 'failure'})


def discord_verification_link(request, user_id, token) :

	current_view = ['account:discord_verification_link', [user_id, token]]
	real_view = False

	try :
		user = models.User.objects.get(pk=user_id)
	except :
		user = None

	if user is not None and user.discord_verification_token == token :

		user.discord_verified = True
		user.discord_verification_token = ""
		user.save()

		send_mail(
			subject="Quelqu'un a lié son compte discord",
			message=f"Le compte {user.username} a été lié au compte discord {user.discord_username}.",
			from_email="info@7tadelles.com",
			recipient_list=["robin.douziech27@gmail.com"],
			fail_silently=False
		)

		helpers.register_view(request, current_view, real_view)
		return render(request, 'account/discord_verification/success.html', {})

	else :

		helpers.register_view(request, current_view, real_view)
		return render(request, 'account/discord_verification/bad_link.html', {})

@login_required
def address_form(request) :

	current_view = ['account:change_address', []]
	real_view = False

	form = forms.AddressForm()
	errors = {
		'errors_count': 0,
		'code_postal_error': [False, "Le code postal doit être composé de 5 chiffres"]
	}

	if request.method == "POST" :

		form = forms.AddressForm(request.POST, request.FILES)

		if form.is_valid() :

			if not(re.match(r"[0-9]{5}", form.cleaned_data['code_postal'])) :
				errors['code_postal_error'][0] = True
				errors['errors_count'] += 1

			if errors['errors_count'] == 0 :

				# on supprime l'ancienne adresse si elle existe
				if request.user.adresse is not None :
					request.user.adresse.delete()
					request.user.adresse = None
					request.user.save()

				# on crée la nouvelle adresse
				adresse = models.Lieu(
					name=f"Chez {request.user.username}",
					adresse=form.cleaned_data['adresse'],
					complement=form.cleaned_data['complement'],
					code_postal=form.cleaned_data['code_postal'],
					ville=form.cleaned_data['ville'],
					pays=form.cleaned_data['pays'],
					image=form.cleaned_data['image']
				)
				adresse.save()

				request.user.adresse = adresse
				request.user.lieus.add(adresse)
				request.user.save()

				helpers.register_view(request, current_view, real_view)
				return render(request, 'account/adresse/success.html', {})

	errors.pop('errors_count')
	helpers.register_view(request, current_view, real_view)
	return render(request, 'account/adresse/form.html', {'form':form, 'errors': errors})

@login_required
def address_delete(request) :
	current_view = ['account:delete_address', []]
	real_view = False
	request.user.lieus.remove(request.user.adresse)
	request.user.adresse.delete()
	request.user.adresse = None
	request.user.save()
	helpers.register_view(request, current_view, real_view)
	return redirect(f"{reverse('account:detail')}?id={request.user.id}")

@login_required
def add_game(request) :
	
	current_view = ['account:add_game', []]
	real_view = False

	form = wiki_forms.GameForm()
	errors = {
		'errors_count': 0,
		'name_already_exists': [False, "Un jeu possédant le même nom est déjà présent dans la base de données."],
		'invalid_bg_color': [False, "La couleur de fond, si elle est renseignée, doit l'être au format hexadécimal (#XXXXXX)"],
		'invalid_player_min_max': [False, "Le nombre minimal de joueurs ne peut pas être supérieur au nombre maximal de joueurs"],
		'invalid_duration': [False, "La durée du jeu doit respecter le bon format."]
	}

	if request.method == "POST" :

		form = wiki_forms.GameForm(request.POST, request.FILES)

		if form.is_valid() :

			# name
			for game in wiki_models.Game.objects.all() :
				if game.name == form.cleaned_data['name'] :
					errors['name_already_exists'][0] = True
					errors['errors_count'] += 1

			if form.cleaned_data['image'] is not None :
				has_image = True
			else :
				has_image = False

			if form.cleaned_data['bg_image'] is not None :
				has_bg_image = True
			else :
				has_bg_image = False

			# bg_color
			if form.cleaned_data['bg_color'] != "" :
				bg_color = form.cleaned_data['bg_color']
				if not(re.match(r"#[0-9a-fA-F]{6}", bg_color)) :
					errors['invalid_bg_color'][0] = True
					errors['errors_count'] += 1
			else :
				bg_color = "#000000"

			# player_min_max
			if form.cleaned_data['players_min'] > form.cleaned_data['players_max'] :
				errors['invalid_player_min_max'][0] = True
				errors['errors_count'] += 1

			# duration
			regs = [
				r"< [1-9]\d{0,1}min",
				r"< [1-9]\d{0,1}h\d{2}|[1-9]\d{0,1}h",
				r"[1-9]\d{0,1}min",
				r"[1-9]\d{0,1}h\d{2}|[1-9]\d{0,1}h",
				r"[1-9]\d{0,1}min - [1-9]\d{0,1}min",
				r"[1-9]\d{0,1}h\d{2}|[1-9]\d{0,1}h - [1-9]\d{0,1}h\d{2}|[1-9]\d{0,1}h",
			]
			ok = False
			index = 0
			while not(ok) and index < len(regs) :
				if re.match(regs[index], form.cleaned_data['duration']) :
					ok = True
				index += 1
			if ok == False :
				errors['invalid_duration'][0] = True
				errors['errors_count'] += 1

			if form.cleaned_data['rules_pdf'] is not None :
				has_rules_pdf = True
			else :
				has_rules_pdf = False

			if errors['errors_count'] == 0 :

				game = wiki_models.Game(
					name = form.cleaned_data['name'],
					has_image = has_image,
					image = form.cleaned_data['image'],
					has_bg_image = has_bg_image,
					bg_image = form.cleaned_data['bg_image'],
					bg_color = bg_color,
					players_min = form.cleaned_data['players_min'],
					players_max = form.cleaned_data['players_max'],
					duration = form.cleaned_data['duration'],
					age_min = form.cleaned_data['age_min'],
					description = form.cleaned_data['description'],
					video_url = form.cleaned_data['video_url'],
					has_rules_pdf = has_rules_pdf,
					rules_pdf = form.cleaned_data['rules_pdf'],
					category = form.cleaned_data['category']
				)
				game.save()

				helpers.register_view(request, current_view, real_view)
				return redirect(f"{reverse('account:detail')}?id={request.user.id}")

	helpers.register_view(request, current_view, real_view)
	return render(request, 'account/game/form.html', {'form': form, 'errors': errors})
