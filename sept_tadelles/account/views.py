from django.contrib import admin as django_admin

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.core.mail import send_mail
from django.core.files.images import get_image_dimensions
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from django.conf import settings
from asgiref.sync import sync_to_async, async_to_sync

from PIL import Image
import os, random
from datetime import datetime

from . import forms, models, admin


'''
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
'''




### LOGIN/LOGOUT


'''
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
'''


### DETAIL ###

'''
@login_required
def detail(request) :

	profile_info = {
		'username': request.user.username,
		'e-mail'   : request.user.email
	}
	if request.user.discord_verified :
		profile_info['pseudo discord'] = request.user.discord_username

	actions = [
		('Modifier la photo de profil', 'account:update_profile_photo', ()),
		('Supprimer la photo de profil', 'account:delete_profile_photo', ()),
		('Modifier le mot de passe', 'account:password_reset_email', ()),
		('Mon adresse', 'account:change_address', ())
	]
	if not(request.user.discord_verified) :
		actions += [
			('Lier le compte discord', 'account:discord_verification_info', ())
		]
	if admin.SoireeAdmin(models.Soiree, django_admin.site).has_add_permission(request) :
		actions += [
			('Créer une soirée', 'account:create_soiree_step_1', ())
		]

	return render(request, "account/detail/detail.html", {
		'actions': actions,
		'profile_info': profile_info
	})

@login_required
def update_profile_photo(request) :

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
					if not(delete_media_file(f"{settings.MEDIA_ROOT}{old_profile_photo.url[1:].split('/',1)[1]}")) :
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

				return redirect('/account/')

	return render(request, 'account/detail/update_profile_photo.html', {'form': form, 'errors': errors})

@login_required
def delete_profile_photo(request) :

	if request.user.has_profile_photo :

		old_profile_photo = request.user.profile_photo
		if not(delete_media_file(f"{settings.MEDIA_ROOT}{old_profile_photo.url[1:].split('/',1)[1]}")) :
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

	return redirect('/account/')

'''


### ACCOUNT CREATION ###



'''

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





@login_required
def discord_verification_info(request) :

	if request.user.discord_verified :
		return redirect('/account/')
	else :
		return render(request, 'account/discord_verification/info.html', {})

def discord_verification_send_email(request, discord_name, discord_id, user_name, bot_token) :

	if bot_token != settings.BOT_TOKEN :
		return redirect('/')
	else :

		try :
			user = models.User.objects.get(username=user_name)
		except :
			user = None

		if user is not None and not(user.discord_verified) :

			token = generate_token(64)
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

			return JsonResponse({'result': 'success'})

		else :

			return JsonResponse({'result': 'failure'})


def discord_verification_link(request, user_id, token) :

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
def address_form(request) :

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

			return render(request, 'account/adresse/success.html', {})

	return render(request, 'account/adresse/form.html', {'form':form})



'''

'''
@login_required
def create_lieu(request) :

	form = forms.LieuCreationForm()

	if request.method == "POST" :

		form = forms.LieuCreationForm(request.POST, request.FILES)

		if form.is_valid() :

			lieu = models.Lieu(
				name=form.cleaned_data['name'],
				adresse=form.cleaned_data['adresse'],
				complement=form.cleaned_data['complement'],
				code_postal=form.cleaned_data['code_postal'],
				ville=form.cleaned_data['ville'],
				pays=form.cleaned_data['pays'],
				image=form.cleaned_data['image']
			)

			lieu.save()

			return render(request, 'account/lieu/creation_success.html', {})

	return render(request, 'account/lieu/creation_form.html', {'form': form})

'''








"""
@login_required
def create_soiree_step_1(request) :

	if admin.SoireeAdmin(models.Soiree, django_admin.site).has_add_permission(request) :

		form = forms.SoireeCreationForm_step_1()

		if request.method == "POST" :

			form = forms.SoireeCreationForm_step_1(request.POST)

			if form.is_valid() :

				soiree = models.Soiree(
					type_soiree=form.cleaned_data['type_soiree'],
					nb_joueurs=models.Soiree()._meta.get_field('nb_joueurs').default,
					lieu=request.user.adresse,
					date=datetime.now(),
					hote=request.user,
					has_image=False,
					image=None
					)
				soiree.save()

				return redirect('account:create_soiree_step_2', soiree_id=soiree.id)

		return render(request, 'account/soiree/creation_form_step_1.html', {'form': form})

	else :

		return render(request, 'account/error.html', {'error_txt': "Vous n'avez pas la permission de créer une nouvelle soirée."})

@login_required
def create_soiree_step_2(request, soiree_id) :

	form = forms.SoireeCreationForm_step_2()

	try :
		soiree = models.Soiree.objects.get(pk=soiree_id)
	except :
		soiree = None

	if admin.SoireeAdmin(models.Soiree, django_admin.site).has_change_permission(request, soiree) :

		if request.method == "POST" :

			form = forms.SoireeCreationForm_step_2(request.POST)

			if form.is_valid() :

				soiree.nb_joueurs = form.cleaned_data['nb_joueurs']
				soiree.save()

				return redirect('account:create_soiree_step_3', soiree_id=soiree.id)

		return render(request, 'account/soiree/creation_form_step_2.html', {'form': form})

	else :

		return render(request, 'account/error.html', {'error_txt': "Vous essayez de modifier une soirée qui n'existe pas ou dont vous n'êtes pas l'hôte"})

@login_required
def create_soiree_step_3(request, soiree_id) :

	form = forms.SoireeCreationForm_step_3(initial={'lieu':request.user.adresse})

	try :
		soiree = models.Soiree.objects.get(pk=soiree_id)
	except :
		soiree = None

	if admin.SoireeAdmin(models.Soiree, django_admin.site).has_change_permission(request, soiree) :

		if request.method == "POST" :

			form = forms.SoireeCreationForm_step_3(request.POST)

			if form.is_valid() :

				soiree.lieu = form.cleaned_data['lieu']
				soiree.save()

				return redirect('account:create_soiree_step_4', soiree_id=soiree.id)

		return render(request, 'account/soiree/creation_form_step_3.html', {'form': form})

	else :

		return render(request, 'account/error.html', {'error_txt': "Vous essayez de modifier une soirée qui n'existe pas ou dont vous n'êtes pas l'hôte"})

@login_required
def create_soiree_step_4(request, soiree_id) :

	form = forms.SoireeCreationForm_step_4()

	try :
		soiree = models.Soiree.objects.get(pk=soiree_id)
	except :
		soiree = None

	if admin.SoireeAdmin(models.Soiree, django_admin.site).has_change_permission(request, soiree) :

		if request.method == "POST" :

			form = forms.SoireeCreationForm_step_4(request.POST)

			if form.is_valid() :

				soiree.date = form.cleaned_data['date']
				soiree.save()

				return render(request, 'account/soiree/creation_success.html', {})

		return render(request, 'account/soiree/creation_form_step_4.html', {'form': form})

	else :

		return render(request, 'account/error.html', {'error_txt': "Vous essayez de modifier une soirée qui n'existe pas ou dont vous n'êtes pas l'hôte"})


@login_required
@permission_required('account.view_soiree')
def my_events(request) :
	all_soirees = models.Soiree.objects.all()
	soirees = []
	for soiree in all_soirees :
		if admin.SoireeAdmin(models.Soiree, django_admin.site).has_change_permission(request, soiree) :
			soirees.append(soiree)
	return render(request, 'account/soiree/list.html', {'soirees': soirees})


@login_required
@permission_required('account.view_soiree')
def event_detail(request, soiree_id) :

	try :
		soiree = models.Soiree.objects.get(pk=soiree_id)
	except :
		soiree = None

	if admin.SoireeAdmin(models.Soiree, django_admin.site).has_change_permission(request, soiree) :
		return render(request, 'account/soiree/detail.html', {'soiree': soiree, 'types_soiree': models.Soiree.TypeDeSoiree.choices, 'types_soiree_desc': models.Soiree.TYPES_SOIREE_DESC})
	else :
		return render(request, 'account/error.html', {'error_txt': "Vous n'avez pas la permission de modifier cette soirée."})



@login_required
@permission_required('account.view_soiree')
def change_invites(request, soiree_id) :

	try :
		soiree = models.Soiree.objects.get(pk=soiree_id)
	except :
		soiree = None

	if admin.SoireeAdmin(models.Soiree, django_admin.site).has_change_permission(request, soiree) :

		form = forms.InvitesForm(request, soiree)
		errors = {
			'errors_count': 0,
			'too_many_guests': [False, "Vous ne pouvez pas inviter autant de monde"],
		}


		if request.method == "POST" :

			form = forms.InvitesForm(request, soiree, request.POST)

			if form.is_valid() :

				if soiree.type_soiree == models.Soiree.TypeDeSoiree.PRIV_INVIT_CONFIRM :
					nb_joueurs = len(soiree.invites.all())+1 - len(form.cleaned_data['invites_to_del']) + len(form.cleaned_data['invites_to_add'])
					if nb_joueurs > soiree.nb_joueurs :
						errors['too_many_guests'][0] = True
						errors['errors_count'] += 1

				if errors['errors_count'] == 0 :

					for invite in form.cleaned_data['invites_to_del'] :
						soiree.invites.remove(invite)
					for invite in form.cleaned_data['invites_to_add'] :
						soiree.invites.add(invite)
					soiree.save()

					return redirect(f'/account/event/{soiree_id}')

		return render(request, 'account/soiree/invites_form.html', {'form': form, 'errors': errors.pop('errors_count')})

	else :

		return render(request, 'account/error.html', {'error_txt': "Vous n'avez pas la permission de modifier cette soirée."})


"""