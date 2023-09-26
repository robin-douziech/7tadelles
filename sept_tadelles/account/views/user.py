from django.contrib import admin as django_admin
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

import datetime as dt

from soiree import admin as soiree_admin
from soiree import models as soiree_models

from account import models, admin
from account.forms import user as forms
from . import helpers

@login_required
def detail(request) :

	user_id = request.GET.get('id', False)

	current_view = [f"{reverse('account:detail')}{f'?id={user_id}' if user_id else ''}", []]

	# notifications
	notifications = request.user.user_notifications.order_by("-created_at")
	no_notification = not(notifications.exists())

	if user_id :

		try :
			user = models.User.objects.get(pk=user_id)
			helpers.clean_user(user)
		except :
			user = None

		if user == request.user :

			helpers.register_view(request, current_view)
			return render(request, 'account/user/detail_change.html', {
				'user_view': user,
				'notifications': notifications,
				'actions': helpers.get_actions(request),
			})

		elif admin.UserAdmin(models.User, django_admin.site).has_view_permission(request, user) :

			helpers.register_view(request, current_view)
			return render(request, 'account/user/detail_view.html', {
				'user_view': user,
				'notifications': notifications,
				'actions': helpers.get_actions(request),
			})

		else :
			return render(request, 'account/error.html', {'error_txt': "Vous n'avez pas la permission de voir cet utilisateur"})

	else :
		return redirect('account:retour1')

@login_required
def list(request) :

	search = request.GET.get('search', False)

	current_view = [f"{reverse('account:list')}{f'?search={search}' if search else ''}", []]

	form = forms.UserSearchForm(request, request.GET)

	if form.is_valid() :

		results = models.User.objects.filter(username__contains=form.cleaned_data['search']).exclude(pk=request.user.id)

	helpers.register_view(request, current_view)
	return render(request, 'account/user/list.html', {
		'form': form,
		'results': results,
		'actions': helpers.get_actions(request)
	})

@login_required
def add_friend(request) :

	user_id = request.GET.get('id', False)

	current_view = [f"{reverse('account:add_friend')}{f'?id={user_id}' if user_id else ''}", []]

	if user_id :

		try :
			user = models.User.objects.get(pk=user_id)
		except :
			user = None

		if admin.UserAdmin(models.User, django_admin.site).has_view_permission(request, user) :

			request.user.demandes_envoyees.add(user)
			request.user.save()

			notification = models.Notification(
				title = "Nouvelle demande d'amitié",
				text = f"{request.user.username} veut être votre ami(e)",
				link = "account:detail",
				get_args = f"?id={request.user.id}",
				post_args = None,
				created_at = dt.datetime.now()
			)
			notification.save()

			helpers.send_notification(notification, [user])

			return redirect('account:retour1')

		else :
			return render(request, 'account/error.html', {'error_txt': "Vous n'avez pas la permission de voir cet utilisateur"})

	else :
		return redirect('account:retour1')

@login_required
def accept_friend(request) :
	
	user_id = request.GET.get('id', False)

	current_view = [f"{reverse('account:accept_friend')}{f'?id={user_id}' if user_id else ''}", []]

	if user_id :

		try :
			user = models.User.objects.get(pk=user_id)
		except :
			user = None

		if admin.UserAdmin(models.User, django_admin.site).has_view_permission(request, user) :

			request.user.amis.add(user)
			request.user.save()

			user.demandes_envoyees.remove(request.user)
			user.save()

			notification = models.Notification(
				title = "Demande d'amitié acceptée",
				text = f"{request.user.username} a accepté votre demande d'amitié",
				link = None,
				get_args = "",
				post_args = None,
				created_at = dt.datetime.now()
			)
			notification.save()

			helpers.send_notification(notification, [user])

			return redirect('account:retour1')

		else :
			return render(request, 'account/error.html', {'error_txt': "Vous n'avez pas la permission de voir cet utilisateur"})

	else :
		return redirect('account:retour1')

@login_required
def refuse_friend(request) :
	
	user_id = request.GET.get('id', False)

	current_view = [f"{reverse('account:refuse_friend')}{f'?id={user_id}' if user_id else ''}", []]

	if user_id :

		try :
			user = models.User.objects.get(pk=user_id)
		except :
			user = None

		if admin.UserAdmin(models.User, django_admin.site).has_view_permission(request, user) :

			user.demandes_envoyees.remove(request.user)
			user.save()

			return redirect('account:retour1')

		else :
			return render(request, 'account/error.html', {'error_txt': "Vous n'avez pas la permission de voir cet utilisateur"})

	else :
		return redirect('account:retour1')

@login_required
def message_friend(request) :
	
	user_id = request.GET.get('id', False)

	current_view = [f"{reverse('account:message_friend')}{f'?id={user_id}' if user_id else ''}", []]

	if user_id :

		try :
			user = models.User.objects.get(pk=user_id)
		except :
			user = None

		if admin.UserAdmin(models.User, django_admin.site).has_view_permission(request, user) :

			return render(request, 'account/error.html', {'error_txt': "Les messages avec les autres utilisateurs seront bientôt disponibles..."})

		else :
			return render(request, 'account/error.html', {'error_txt': "Vous n'avez pas la permission de voir cet utilisateur"})

	else :
		return redirect('account:retour1')
