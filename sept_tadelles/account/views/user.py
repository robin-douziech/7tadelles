from django.contrib import admin as django_admin
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.core.mail import send_mail
from django.core.files.images import get_image_dimensions
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import Permission
from django.conf import settings
from django.urls import reverse

import datetime as dt

from account import models, admin
from account.forms import user as forms
from . import helpers

def login_view(request) :

	current_view = ['account:login', []]
	real_view = False

	form = forms.LoginForm()
	auth_error = False
	unverified_user = False

	if request.method == "POST" :

		form = forms.LoginForm(request.POST)

		if form.is_valid() :

			user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])

			if user is not None and user.verified :
				login(request, user)
				helpers.register_view(request, current_view, real_view)
				return redirect('/')
			elif user is not None :
				unverified_user = True
			else :
				auth_error = True

	helpers.register_view(request, current_view, real_view)
	return render(request, 'account/registration/login.html', {'form': form, 'auth_error': auth_error, 'unverified_user': unverified_user})


def logout_view(request) :
	current_view = ['account:logout', []]
	real_view = False
	logout(request)
	helpers.register_view(request, current_view, real_view)
	return render(request, 'account/registration/logout.html')




@login_required
def detail(request) :

	current_view = ['account:detail', []]
	real_view = True

	profile_info = {
		'username': request.user.username,
		'e-mail'   : request.user.email
	}
	if request.user.discord_verified :
		profile_info['pseudo discord'] = request.user.discord_username

	left_actions = [('Modifier la photo de profil', 'account:update_profile_photo', ())]

	if request.user.has_profile_photo :
		left_actions += [('Supprimer la photo de profil', 'account:delete_profile_photo', ())]

	left_actions += [
		('Modifier le mot de passe', 'account:password_reset_email', ()),
		('Mon adresse', 'account:change_address', ())
	]

	if request.user.adresse is not None :
		left_actions += [('Supprimer mon adresse', 'account:delete_address', ())]
	if not(request.user.discord_verified) :
		left_actions += [('Lier le compte discord', 'account:discord_verification_info', ())]
	if admin.SoireeAdmin(models.Soiree, django_admin.site).has_add_permission(request) :
		left_actions += [('Créer une soirée', 'account:create_soiree_step_1', ())]
	if request.user.soirees_hote.exists() :
		left_actions += [('Mes soirées', 'account:my_events', ())]
	if request.user.invitations.exists() :
		left_actions += [('Mes invitations', 'game_calendar:game_calendar_index', ())]
	left_actions += [('Rechercher utilisateur', 'account:search_user_form', ())]

	right_actions = [('Retour', 'welcome:index', ())]

	notifications = request.user.user_notifications.filter(created_at__gt=dt.datetime.now()-dt.timedelta(days=7)).order_by("-created_at")
	notification_to_del = request.user.user_notifications.filter(created_at__lte=dt.datetime.now()-dt.timedelta(days=7))
	for notification in notification_to_del:
		notification.delete()
	no_notifications = False
	if not(notifications.exists()) :
		no_notifications = True

	helpers.register_view(request, current_view, real_view)
	return render(request, "account/detail/detail.html", {
		'left_actions': left_actions,
		'right_actions': right_actions,
		'profile_info': profile_info,
		'notifications': notifications,
		'no_notifications' : no_notifications
	})

@login_required
def update_profile_photo(request) :

	current_view = ['account:update_profile_photo', []]
	real_view = False

	form = forms.UpdateProfilePhotoForm()
	errors = {
		'photo_too_big': [False, "Vous ne pouvez pas utiliser cette image car au moins un de ses dimensions est trop grande"]
	}

	if request.method == "POST" :

		form = forms.UpdateProfilePhotoForm(request.POST, request.FILES)

		if form.is_valid() :

			width, height = get_image_dimensions(form.cleaned_data['profile_photo'])
			if width >= 1000 or height >=1000 :
				errors['photo_too_big'][0] = True

			else :

				# si l'utilisateur avait déjà une photo de profil, on la supprime du serveur
				# (et on envoie un mail au propriétaire du serveur en cas d'erreur lors de la suppression)
				if request.user.has_profile_photo :

					old_profile_photo = request.user.profile_photo
					if not(helpers.delete_media_file(f"{settings.MEDIA_ROOT}{old_profile_photo.url[1:].split('/',1)[1]}")) :
						send_mail(
							subject="Fichier mal supprimé sur le serveur",
							message=f"Une erreur est survenue lors de la suppression d'un fichier sur le serveur.\n\nChemin vers le fichier : {settings.MEDIA_ROOT}{old_profile_photo.url[1:].split('/',1)[1]}",
							from_email="info@7tadelles.com",
							recipient_list=["robin.douziech27@gmail.com"],
							fail_silently=False
						)		

				request.user.profile_photo = form.cleaned_data['profile_photo']
				request.user.has_profile_photo = True
				request.user.save()

				helpers.register_view(request, current_view, real_view)
				return redirect('/account/')

	helpers.register_view(request, current_view, real_view)
	return render(request, 'account/detail/update_profile_photo.html', {'form': form, 'errors': errors})

@login_required
def delete_profile_photo(request) :

	current_view = ['account:delete_profile_photo', []]
	real_view = False

	if request.user.has_profile_photo :

		old_profile_photo = request.user.profile_photo
		if not(helpers.delete_media_file(f"{settings.MEDIA_ROOT}{old_profile_photo.url[1:].split('/',1)[1]}")) :
			send_mail(
				subject="Fichier mal supprimé sur le serveur",
				message=f"Une erreur est survenue lors de la suppression d'un fichier sur le serveur.\n\nChemin vers le fichier : {settings.MEDIA_ROOT}{old_profile_photo.url[1:].split('/',1)[1]}",
				from_email="info@7tadelles.com",
				recipient_list=["robin.douziech27@gmail.com"],
				fail_silently=False
			)

		request.user.profile_photo = None
		request.user.has_profile_photo = False
		request.user.save()

	helpers.register_view(request, current_view, real_view)
	return redirect('/account/')




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
		permission = Permission.objects.get(codename='view_soiree')
		print(f"permission : {permission}")
		user.user_permissions.set([permission])
		user.save()
		helpers.register_view(request, current_view, real_view)
		return render(request, 'account/creation/activation_success.html', {})
	else:
		helpers.register_view(request, current_view, real_view)
		return render(request, 'account/creation/activation_error.html', {})



### PASSWORD RESET ###

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
		return redirect('/account/')
	else :
		helpers.register_view(request, current_view, real_view)
		return render(request, 'account/discord_verification/info.html', {})

def discord_verification_send_email(request, discord_name, discord_id, user_name, bot_token) :

	current_view = ['account:discord_verification_send_email', [discord_name, discord_id, user_name, bot_token]]
	real_view = False

	if bot_token != settings.BOT_TOKEN :
		helpers.register_view(request, current_view, real_view)
		return redirect('/')
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

	if request.method == "POST" :

		form = forms.AddressForm(request.POST, request.FILES)

		if form.is_valid() :

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
			request.user.save()

			helpers.register_view(request, current_view, real_view)
			return render(request, 'account/adresse/success.html', {})

	helpers.register_view(request, current_view, real_view)
	return render(request, 'account/adresse/form.html', {'form':form})

@login_required
def address_delete(request) :
	current_view = ['account:delete_address', []]
	real_view = False
	request.user.adresse.delete()
	request.user.adresse = None
	request.user.save()
	helpers.register_view(request, current_view, real_view)
	return redirect('account:detail')

@login_required
def clear_session(request) :
	last_view = request.session.get("last_view", ["welcome:index", []])
	request.session['last_view'] = ['account:clear_session', []]
	request.session['last_real_view'] = []
	if request.session.get('form', False) :
		request.session.pop('form')
	return redirect(last_view[0], *last_view[1])

def retour(request) :
	request.session['last_real_view'] = request.session.get("last_real_view", [])
	if len(request.session['last_real_view']) > 0 :
		redirect_view = request.session['last_real_view'][-1]
		request.session['last_real_view'] = request.session['last_real_view'][:-1]
	else :
		redirect_view = ['welcome:index', []]
	return redirect(redirect_view[0], *redirect_view[1])



@login_required
def search_user_form(request) :

	current_view = ['account:search_user_form', []]
	real_view = False

	results = []
	form = forms.FriendSearchForm(request.GET)

	right_actions = [('Retour', 'account:detail', ())]

	if form.is_valid() :

		request.session['form'] = {field: form.cleaned_data[field] for field in form.cleaned_data}
		results = models.User.objects.filter(username__contains=form.cleaned_data['search']).exclude(pk=request.user.id)

	elif request.session.get("form", False) :

		results = models.User.objects.filter(username__contains=request.session['form']['search']).exclude(pk=request.user.id)
		request.session.pop("form")

	helpers.register_view(request, current_view, real_view)
	return render(request, 'account/user/list.html', {'form': form, 'results': results, 'right_actions': right_actions})



	


@login_required
def user_detail(request, username) :

	current_view = ['account:user_detail', [username]]
	real_view = False

	try :
		user = models.User.objects.get(username=username)
	except :
		user = None

	if admin.UserAdmin(models.User, django_admin.site).has_view_permission(request, user) :

		helpers.register_view(request, current_view, real_view)
		return render(request, 'account/user/detail.html', {'user_detail': user})

	else :
		helpers.register_view(request, current_view, real_view)
		return render(request, 'account/error.html', {'error_txt': "Vous n'avez pas la permission de voir cet utilisateur."})



@login_required
def demande_ami(request, user_id) :

	#current_view = ['account:demande_ami', [user_id]]
	#real_view = False

	try :
		user = models.User.objects.get(pk=user_id)
	except :
		user=None

	if admin.UserAdmin(models.User, django_admin.site).has_view_permission(request, user) :

		request.user.demandes_envoyees.add(user)
		request.user.save()

		notification = models.Notification(
			#users=None,
			title="Nouvelle demande d'amitié",
			text=f"{request.user.username} veut être votre ami(e)",
			link="account:search_user_form",
			args=None,
			created_at=dt.datetime.now()
		)
		notification.save()
		helpers.send_notification(notification, [user])

		last_view = request.session['last_view']
		return redirect(last_view[0], *last_view[1])

	else :
		return render(request, 'account/error.html', {'error_txt': "Vous n'avez pas la permission de voir cet utilisateur."})

@login_required
def accepter_ami(request, user_id) :

	#current_view = ['account:accepter_ami', [user_id]]
	#real_view = False

	try :
		user = models.User.objects.get(pk=user_id)
	except :
		user = None

	if admin.UserAdmin(models.User, django_admin.site).has_view_permission(request, user) and user in request.user.demandes_recues.all() :

		request.user.amis.add(user)
		request.user.save()

		user.demandes_envoyees.remove(request.user)
		user.save()

		notification = models.Notification(
			title="Demande d'amitié acceptée",
			text=f"{request.user.username} a acceptée votre demande d'amitié",
			link=None,
			args=None,
			created_at=dt.datetime.now()
		)
		notification.save()
		helpers.send_notification(notification, [user])

		last_view = request.session['last_view']
		return redirect(last_view[0], *last_view[1])

	else :
		return render(request, 'account/error.html', {'error_txt': "Vous n'avez pas la permission de voir cet utilisateur."})


@login_required
def refuser_ami(request, user_id) :

	#current_view = ['account:refuser_ami', [user_id]]
	#real_view = False

	try :
		user = models.User.objects.get(pk=user_id)
	except :
		user = None

	if admin.UserAdmin(models.User, django_admin.site).has_view_permission(request, user) and user in request.user.demandes_recues.all() :

		user.demandes_envoyees.remove(request.user)
		user.save()

		last_view = request.session['last_view']
		return redirect(last_view[0], *last_view[1])

	else :
		return render(request, 'account/error.html', {'error_txt': "Vous n'avez pas la permission de voir cet utilisateur."})



