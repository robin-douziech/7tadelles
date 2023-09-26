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
				user.save()
				helpers.clean_user(user)
				return redirect('welcome:index')
			elif user is not None :
				errors['unverified_user'][0] = True
			else :
				errors['auth_error'][0] = True

	errors.pop('errors_count')
	#helpers.register_view(request, current_view)
	return render(request, 'account/registration/login.html', {'form': form, 'errors': errors})

@login_required
def logout_view(request) :
	logout(request)
	return render(request, 'account/registration/logout.html')

def create(request) :

	current_view = ['account:user_creation_form', []]

	form = forms.UserCreationForm()
	errors = {
		'errors_count': 0,
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
					errors['errors_count'] += 1
				if user.username == form.cleaned_data['username'] :
					errors['username_already_used'][0] = True
					errors['errors_count'] += 1

			# on vérifie que les mots de passe sont identiques
			if form.cleaned_data['password1'] != form.cleaned_data['password2'] :
				errors['passwords_dont_match'][0] = True
				errors['errors_count'] += 1

			if errors['errors_count'] == 0 :

				# aucune erreur : on crée l'utilisateur
				user = models.User.objects.create_user(form.cleaned_data['username'], form.cleaned_data['email'], form.cleaned_data['password1'])
				user.verification_token = helpers.generate_token(64)
				user.save()

				if settings.ENV == "PROD" :
					verification_link = f"https://7tadelles.com/account/verify-email/{user.id}/{user.verification_token}"
				else :
					verification_link = f"http://localhost:8000/account/verify-email/{user.id}/{user.verification_token}"
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

				return render(request, 'account/creation/activation_email_sent.html', {})

	errors.pop('errors_count')
	#helpers.register_view(request, current_view)
	return render(request, "account/creation/creation_form.html", {"form": form, 'errors': errors})

def verify_email(request, user_id, token):

	current_view = ['account:verify_email', [user_id, token]]

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

def password_reset_email_form(request) :

	current_view = ['account:password_reset_email', []]

	form = forms.PasswordResetEmailForm()
	errors = {
		'errors_count': 0,
		'unknown_email': [False, "Aucun compte n'a été trouvé avec cette adresse e-mail."]
	}

	if request.method == "POST" :

		form = forms.PasswordResetEmailForm(request.POST)

		if form.is_valid() :

			user = helpers.find_user_by_email(form.cleaned_data['email'])
			if user is None :
				errors['unknown_email'][0] = True
				errors['errors_count'] += 1

			email = user.email

	elif request.user.is_authenticated :

		user = request.user
		email = user.email

	if (request.method == "POST" and form.is_valid()) or request.user.is_authenticated :

		if errors['errors_count'] == 0 :

			user.password_reset_token = helpers.generate_token(64)
			user.save()

			if settings.ENV == "PROD" :
				verification_link = f"https://7tadelles.com/account/password-reset/{user.id}/{user.password_reset_token}/"
			else :
				verification_link = f"http://localhost:8000/account/password-reset/{user.id}/{user.password_reset_token}/"

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

	errors.pop('errors_count')
	#helpers.register_view(request, current_view)
	return render(request, 'account/password_reset/password_reset_email_form.html', {'form': form, 'errors': errors})

def password_reset_form(request, user_id, token) :

	current_view = ['account:password_reset', [user_id, token]]

	try :
		user = models.User.objects.get(pk=user_id)
	except :
		user = None

	if user is not None and user.password_reset_token == token :

		form = forms.PasswordResetForm()
		errors = {
			'errors_count': 0,
			'passwords_dont_match': [False, "Les mots de passe renseignés ne sont pas identiques"]
		}

		if request.method == "POST" :

			form = forms.PasswordResetForm(request.POST)

			if form.is_valid() :

				if form.cleaned_data['password1'] != form.cleaned_data['password2'] :
					errors['passwords_dont_match'][0] = True
					errors['errors_count'] += 1

				if errors['errors_count'] == 0 :

					user.set_password(form.cleaned_data['password1'])
					user.password_reset_token = ""
					user.save()

					return render(request, 'account/password_reset/password_reset_complete.html', {})

		errors.pop('errors_count')
		#helpers.register_view(request, current_view)
		return render(request, 'account/password_reset/password_reset_confirm.html', {'form': form, 'errors': errors})

	else :

		return render(request, 'account/password_reset/password_reset_bad_link.html')

def discord_verification_send_email(request, discord_name, discord_id, user_name, bot_token) :

	current_view = ['account:discord_verification_send_email', [discord_name, discord_id, user_name, bot_token]]

	if bot_token != settings.BOT_TOKEN :
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
				verification_link = f"https://7tadelles.com/account/discord-verification-link/{user.id}/{token}"
			else :
				verification_link = f"http://localhost:8000/account/discord-verification-link/{user.id}/{token}"

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

			return JsonResponse({'result': 'success'})

		else :

			return JsonResponse({'result': 'failure'})


def discord_verification_link(request, user_id, token) :

	current_view = ['account:discord_verification_link', [user_id, token]]

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

		return render(request, 'account/discord_verification/success.html', {})

	else :

		return render(request, 'account/discord_verification/bad_link.html', {})

@login_required
def add_game(request) :
	
	current_view = ['account:add_game', []]

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

				return redirect('account:retour1')

	#helpers.register_view(request, current_view)
	return render(request, 'account/game/form.html', {'form': form, 'errors': errors})

@login_required
def clean_session(request) :
	request.session.pop('last_views')
	return redirect("welcome:index")

@login_required
def retour1(request) :

	last_views = request.session.get('last_views', [['welcome:index', []], ['welcome:index', []]])
	view = last_views[-1]
	if len(last_views) > 1 :
		request.session['last_views'] = request.session['last_views'][:-1]
	return redirect(view[0], *view[1])

@login_required
def retour2(request) :

	last_views = request.session.get('last_views', [['welcome:index', []], ['welcome:index', []]])
	view = last_views[-2]
	if len(last_views) > 2 :
		request.session['last_views'] = request.session['last_views'][:-2]
	return redirect(view[0], *view[1])