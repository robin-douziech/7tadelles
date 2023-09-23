from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.urls import reverse

from account import models
from account.forms import parameters as forms
from . import helpers

import re

def get_menu_buttons() :
	menu_buttons = [
		('Mon profil', 'account:parameters_profile', '', ()),
		('Mon adresse', 'account:parameters_address', '', ()),
		('Types de soirées', 'account:parameters_type_soiree', '', ()),
		('Mails reçus', 'account:parameters_notif_mail', '', ())
	]
	return menu_buttons

@login_required
def base(request) :

	current_view = ['account:parameters_base', []]

	helpers.register_view(request, current_view)
	return render(request, 'account/parameters/base.html', {
		'menu_buttons': get_menu_buttons(),
		'actions': helpers.get_actions(request)
	})

@login_required
def profile(request) :
	
	current_view = ['account:parameters_profile', []]

	form = forms.ProfileForm(request)

	if request.method == "POST" :

		form = forms.ProfileForm(request, request.POST, request.FILES)

		if form.is_valid() :

			if form.cleaned_data['profile_photo'] is not None :
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

			if form.cleaned_data['cover_photo'] is not None :
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

		return render(request, 'account/parameters/profile.html', {
			'form': form,
			'menu_buttons': get_menu_buttons(),
			'actions': helpers.get_actions(request)
		})

	helpers.register_view(request, current_view)
	return render(request, 'account/parameters/profile.html', {
		'form': form,
		'menu_buttons': get_menu_buttons(),
		'actions': helpers.get_actions(request)
	})

@login_required
def delete_profile_photo(request) :
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
	last_view = request.session.get('last_views', [['welcome:index', []], ['welcome:index', []]])[-1]
	return redirect(last_view[0], *last_view[1])

@login_required
def delete_cover_photo(request) :
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
	last_view = request.session.get('last_views', [['welcome:index', []], ['welcome:index', []]])[-1]
	return redirect(last_view[0], *last_view[1])

@login_required
def address(request) :
	
	current_view = ['account:parameters_address', []]

	form = forms.AddressForm(request)
	errors = {
		'errors_count': 0,
		'code_postal_error': [False, "Le code postal doit être composé de 5 chiffres"]
	}

	if request.method == "POST" :

		form = forms.AddressForm(request, request.POST, request.FILES)

		if form.is_valid() :

			if not(re.match(r"[0-9]{5}", form.cleaned_data['code_postal'])) :
				errors['code_postal_error'][0] = True
				errors['errors_count'] += 1
			if errors['errors_count'] == 0 :
				if request.user.adresse is not None :
					request.user.adresse.delete()
					request.user.adresse = None
					request.user.save()
				adresse = models.Lieu(
					name=f"Chez {request.user.username}",
					adresse=form.cleaned_data['adresse'],
					complement=form.cleaned_data['complement'],
					code_postal=form.cleaned_data['code_postal'],
					ville=form.cleaned_data['ville'],
					pays=form.cleaned_data['pays'],
					has_image=form.cleaned_data['image'] is not None,
					image=form.cleaned_data['image']
				)
				adresse.save()
				request.user.adresse = adresse
				request.user.lieus.add(adresse)
				request.user.save()

		errors.pop('errors_count')
		return render(request, 'account/parameters/address.html', {
			'form': form,
			'errors': errors,
			'menu_buttons': get_menu_buttons(),
			'actions': helpers.get_actions(request)
		})

	errors.pop('errors_count')
	helpers.register_view(request, current_view)
	return render(request, 'account/parameters/address.html', {
		'form': form,
		'errors': errors,
		'menu_buttons': get_menu_buttons(),
		'actions': helpers.get_actions(request)
	})

@login_required
def delete_address(request) :
	if request.user.adresse is not None :
		request.user.adresse.delete()
		request.user.adresse = None
		request.user.save()
	last_view = request.session.get('last_views', [['welcome:index', []], ['welcome:index', []]])[-1]
	return redirect(last_view[0], *last_view[1])







@login_required
def type_soiree(request) :

	current_view = ['account:parameters_type_soiree', []]

	form = forms.TypeSoireeForm(request)

	if request.method == "POST" :

		form = forms.TypeSoireeForm(request, request.POST)

		if form.is_valid() :

			choices_view = form.fields['type_soiree_view'].choices[::-1]
			choices_notif = form.fields['type_soiree_notif'].choices[::-1]
			type_soiree_view = 0
			type_soiree_notif = 0
			for i,choice in enumerate(choices_view) :
				if choice[0] in form.cleaned_data['type_soiree_view'] :
					type_soiree_view += 2**i
			for i,choice in enumerate(choices_notif) :
				if choice[0] in form.cleaned_data['type_soiree_notif'] :
					type_soiree_notif += 2**i

			request.user.parameters['type_soiree_view'] = type_soiree_view
			request.user.parameters['type_soiree_notif'] = type_soiree_notif
			request.user.save()

		return render(request, 'account/parameters/type_soiree.html', {
			'form': form,
			'menu_buttons': get_menu_buttons(),
			'actions': helpers.get_actions(request)
		})

	helpers.register_view(request, current_view)
	return render(request, 'account/parameters/type_soiree.html', {
		'form': form,
		'menu_buttons': get_menu_buttons(),
		'actions': helpers.get_actions(request)
	})

@login_required
def notif_mail(request) :

	current_view = ['account:parameters_notif_mail', []]

	form = forms.NotifMailForm(request)

	if request.method == "POST" :

		form = forms.NotifMailForm(request, request.POST)

		if form.is_valid() :

			request.user.parameters['notif_mail'] = form.cleaned_data['notif_mail']
			request.user.save()

		return render(request, 'account/parameters/notif_mail.html', {
			'form': form,
			'menu_buttons': get_menu_buttons(),
			'actions': helpers.get_actions(request)
		})

	helpers.register_view(request, current_view)
	return render(request, 'account/parameters/notif_mail.html', {
		'form': form,
		'menu_buttons': get_menu_buttons(),
		'actions': helpers.get_actions(request)
	})
