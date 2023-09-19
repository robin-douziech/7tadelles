from django.contrib import admin as django_admin
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils import timezone

import datetime as dt

from account import models as account_models
from account import admin as account_admin
from account import forms as account_forms
from account.views import helpers

from . import models, forms, admin

@login_required
def list(request) :

	filtre = request.GET.get('filter', "all") # hote, invitations, inscriptions, all
	type_soiree = int(request.GET.get('type', 15))

	get_args = f"?filter={filtre}&type={type_soiree}"

	current_view = [f"{reverse('soiree:list')}?filter={filtre}&type={type_soiree}", []]
	real_view = True

	if filtre == "all" :
		filtre = "hote+inscriptions+invitations"

	TYPES_SOIREE = [
		models.Soiree.TypeDeSoiree.PUB,
		models.Soiree.TypeDeSoiree.PUB_INSC,
		models.Soiree.TypeDeSoiree.PRIV_LIST_INSC,
		models.Soiree.TypeDeSoiree.PRIV_INVIT_CONFIRM,
	]

	all_soirees = models.Soiree.objects.none()
	for i,elt in enumerate(TYPES_SOIREE) :
		if (type_soiree//(2**i))%2 == 1 :
			all_soirees = all_soirees.union(models.Soiree.objects.filter(type_soiree__exact=TYPES_SOIREE[i]))

	mes_soirees = models.Soiree.objects.none()
	inscriptions = models.Soiree.objects.none()
	invitations = models.Soiree.objects.none()
	if "hote" in filtre :
		mes_soirees = all_soirees.intersection(request.user.soirees_hote.all())
	if "inscriptions" in filtre :
		inscriptions = all_soirees.intersection(request.user.user_inscriptions.all())
	if "invitations" in filtre :
		invitations = all_soirees.intersection(request.user.invitations.difference(request.user.user_inscriptions.all()))

	helpers.register_view(request, current_view, real_view, get_args)
	return render(request, 'soiree/soiree/list.html', {
		'mes_soirees': mes_soirees,
		'inscriptions': inscriptions,
		'invitations': invitations,
		'get_args': get_args
	})

@login_required
def detail(request) :

	soiree_id = request.GET.get("id", False)

	current_view = [f"{reverse('soiree:detail')}{f'?id={soiree_id}' if soiree_id else ''}", []]
	real_view = True

	if soiree_id :

		get_args = f"?id={soiree_id}"
		
		try :
			soiree = models.Soiree.objects.get(pk=soiree_id)
		except :
			soiree = None

		if admin.SoireeAdmin(models.Soiree, django_admin.site).has_change_permission(request, soiree) :

			form = forms.SoireeForm(request, soiree)
			errors = {
				'errors_count': 0,
				'not_enough_places': [False, "Il ne peut pas y avoir moins de places que d'invités pour une soirée privée avec liste d'invités. Retirez des invités avant de réduire le nombre de places."],
				'passed_date': [False, "Vous ne pouvez pas renseigner une date passée"],
			}
			if request.method == "POST" :
				form = forms.SoireeForm(request, soiree, request.POST)
				if form.is_valid() :
					if soiree.type_soiree == models.Soiree.TypeDeSoiree.PRIV_INVIT_CONFIRM and form.cleaned_data['nb_joueurs'] < len(soiree.invites.all())+1 :
						errors['not_enough_places'][0] = True
						errors['errors_count'] += 1
					if form.cleaned_data['date'] < timezone.now() :
						errors['passed_date'][0] = True
						errors['errors_count'] += 1
					if errors['errors_count'] == 0 :
						soiree.type_soiree = form.cleaned_data['type_soiree']
						soiree.nb_joueurs = form.cleaned_data['nb_joueurs']
						soiree.lieu = form.cleaned_data['lieu']
						soiree.date = form.cleaned_data['date']
						soiree.save()
			errors.pop('errors_count')
			helpers.register_view(request, current_view, real_view, get_args)
			return render(request, 'soiree/soiree/detail_change.html', {
				'form': form,
				'errors': errors,
				'soiree': soiree,
				'types_soiree': models.Soiree.TypeDeSoiree.choices,
				'types_soiree_desc': models.Soiree.TYPES_SOIREE_DESC,
				'get_args': get_args
			})

		if admin.SoireeAdmin(models.Soiree, django_admin.site).has_view_permission(request, soiree) :

			helpers.register_view(request, current_view, real_view, get_args)
			return render(request, 'soiree/soiree/detail_view.html', {
				'soiree': soiree,
				'types_soiree': models.Soiree.TypeDeSoiree.choices,
				'types_soiree_desc': models.Soiree.TYPES_SOIREE_DESC,
				'get_args': get_args
			})

		else :

			return render(request, 'soiree/error.html', {"error_txt": "Vous n'avez pas la permission de voir ou de modifier cette soirée"})

	else :

		last_view = request.session.get('last_view', ['welcome:index', []])
		return redirect(last_view[0], *last_view[1])



@login_required
def creation_step_1(request) :

	current_view = ['soiree:creation_step_1', []]
	real_view = False

	if admin.SoireeAdmin(models.Soiree, django_admin.site).has_add_permission(request) :

		form = forms.CreationForm_step_1(request)
		if request.method == "POST" :
			form = forms.CreationForm_step_1(request, request.POST)
			if form.is_valid() :
				soiree = models.Soiree(
					type_soiree = form.cleaned_data['type_soiree'],
					nb_joueurs = models.Soiree()._meta.get_field('nb_joueurs').default,
					lieu = request.user.adresse,
					date = dt.datetime.now() + dt.timedelta(days=1),
					hote = request.user,
					has_image = False,
					image = None,
					created_at = dt.datetime.now(),
				)
				soiree.save()
				if form.cleaned_data['type_soiree'] in [models.Soiree.TypeDeSoiree.PUB_INSC, models.Soiree.TypeDeSoiree.PUB] :
					for user in account_models.User.objects.all() :
						soiree.invites.add(user)
				soiree.save()
				return redirect(f"{reverse('soiree:creation_step_2')}?id={soiree.id}")
		helpers.register_view(request, current_view, real_view)
		return render(request, 'soiree/soiree/creation_step_1.html', {'form': form})

	else :

		return render(request, 'soiree/error.html', {'error_txt': "Vous n'avez pas la permission de créer une nouvelle soirée"})

@login_required
def creation_step_2(request) :

	soiree_id = request.GET.get('id', False)

	current_view = [f"{reverse('soiree:creation_step_2')}{f'?id={soiree_id}' if soiree_id else ''}", []]
	real_view = False

	if soiree_id :

		get_args = f"?id={soiree_id}"

		try :
			soiree = models.Soiree.objects.get(pk=soiree_id)
		except :
			soiree = None

		if admin.SoireeAdmin(models.Soiree, django_admin.site).has_change_permission(request, soiree) :

			form = forms.CreationForm_step_2(request)
			if request.method == "POST" :
				form = forms.CreationForm_step_2(request, request.POST)
				if form.is_valid() :
					soiree.nb_joueurs = form.cleaned_data['nb_joueurs']
					soiree.save()
					return redirect(f"{reverse('soiree:creation_step_3')}?id={soiree.id}")
			helpers.register_view(request, current_view, real_view, get_args)
			return render(request, 'soiree/soiree/creation_step_2.html', {'form': form})

		else :
			return render(request, 'soiree/error.html', {'error_txt': "Vous n'avez pas la permission de modifier cette soirée"})

	else :
		last_view = request.session.get('last_view', ['welcome:index', []])
		return redirect(last_view[0], *last_view[1])

@login_required
def creation_step_3(request) :

	soiree_id = request.GET.get('id', False)

	current_view = [f"{reverse('soiree:creation_step_3')}{f'?id={soiree_id}' if soiree_id else ''}", []]
	real_view = False

	if soiree_id :

		get_args = f"?id={soiree_id}"

		try :
			soiree = models.Soiree.objects.get(pk=soiree_id)
		except :
			soiree = None

		if admin.SoireeAdmin(models.Soiree, django_admin.site).has_change_permission(request, soiree) :

			form = forms.CreationForm_step_3(request)
			if request.method == "POST" :
				form = forms.CreationForm_step_3(request, request.POST)
				if form.is_valid() :
					soiree.lieu = form.cleaned_data['lieu']
					soiree.save()
					return redirect(f"{reverse('soiree:creation_step_4')}?id={soiree.id}")
			helpers.register_view(request, current_view, real_view, get_args)
			return render(request, 'soiree/soiree/creation_step_3.html', {'form': form})

		else :
			return render(request, 'soiree/error.html', {'error_txt': "Vous n'avez pas la permission de modifier cette soirée"})

	else :
		last_view = request.session.get('last_view', ['welcome:index', []])
		return redirect(last_view[0], *last_view[1])

@login_required
def creation_step_4(request) :

	soiree_id = request.GET.get('id', False)

	current_view = [f"{reverse('soiree:creation_step_4')}{f'?id={soiree_id}' if soiree_id else ''}", []]
	real_view = False

	if soiree_id :

		get_args = f"?id={soiree_id}"

		try :
			soiree = models.Soiree.objects.get(pk=soiree_id)
		except :
			soiree = None

		if admin.SoireeAdmin(models.Soiree, django_admin.site).has_change_permission(request, soiree) :

			form = forms.CreationForm_step_4(request)
			errors = {
				'errors_count': 0,
				'passed_date': [False, "Vous ne pouvez pas renseigner une date passée"]
			}
			if request.method == "POST" :
				form = forms.CreationForm_step_4(request, request.POST)
				if form.is_valid() :
					if form.cleaned_data['date'] < timezone.now() :
						errors['passed_date'][0] = True
						errors['errors_count'] += 1
					if errors['errors_count'] == 0 :
						soiree.date = form.cleaned_data['date']
						soiree.save()
						return render(request, 'soiree/soiree/creation_success.html', {})
			errors.pop('errors_count')
			helpers.register_view(request, current_view, real_view, get_args)
			return render(request, 'soiree/soiree/creation_step_4.html', {'form': form, 'errors': errors})

		else :
			return render(request, 'soiree/error.html', {'error_txt': "Vous n'avez pas la permission de modifier cette soirée"})

	else :
		last_view = request.session.get('last_view', ['welcome:index', []])
		return redirect(last_view[0], *last_view[1])

@login_required
def change_invites(request) :

	soiree_id = request.GET.get('id', False)

	current_view = [f"{reverse('soiree:change_invites')}{f'?id={soiree_id}' if soiree_id else ''}", []]
	real_view = False

	if soiree_id :

		get_args = f"?id={get_args}"

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
						nb_joueurs = len(soiree.invites.all())+1 + len(form.cleaned_data['invites_to_add'])
						if nb_joueurs > soiree.nb_joueurs :
							errors['too_many_guests'][0] = True
							errors['errors_count'] += 1
					if errors['errors_count'] == 0 :
						notification = account_models.Notification(
							title="Nouvelle invitation à une soirée jeux",
							text=f"{request.user.username} vous invite à une soirée jeux le {helpers.week_day(soiree.date)} {soiree.date.day} {helpers.month_str(soiree.date)} {soiree.date.year}",
							link="game_calendar:game_calendar_index",
							args=None,
							created_at=dt.datetime.now()
						)
						notification.save()
						invite_to_notice = []
						for invite in form.cleaned_data['invites_to_add'] :
							soiree.invites.add(invite)
							if soiree not in invite.invitations_received.all() :
								invite_to_notice.append(invite)
						soiree.save()
						helpers.send_notification(notification, invite_to_notice)
						return redirect(f"{reverse('soiree:detail')}?id={soiree.id}")
			errors.pop('errors_count')
			helpers.register_view(request, current_view, real_view, get_args)
			return render(request, 'soiree/soiree/change_invites.html', {'form': form, 'errors': errors})

		else :
			return render(request, 'soiree/error.html', {'error_txt': "Vous n'avez pas la permission de modifier cette soirée"})

	else :
		last_view = request.session.get('last_view', ['welcome:index', []])
		return redirect(last_view[0], *last_view[1])

@login_required
def inscription(request) :

	soiree_id = request.GET.get('id', False)

	current_view = [f"{reverse('soiree:inscription')}{f'?id={soiree_id}' if soiree_id else ''}", []]
	real_view = False

	if soiree_id :

		get_args = f"?id={soiree_id}"

		try :
			soiree = models.Soiree.objects.get(pk=soiree_id)
		except :
			soiree = None

		if admin.SoireeAdmin(models.Soiree, django_admin.site).has_view_permission(request, soiree) :

			errors = {
				'errors_count': 0,
				'no_more_places': [False, "Il n'y a plus de place libre à cette soirée. Vous ne pouvez pas vous inscrire tant que quelqu'un d'autre ne s'est pas désinscrit."],
				'hote_error': [False, "Vous ne pouvez pas vous inscrire à cette soirée, vous ne faites pas partie des invités (l'hôte d'une soirée n'a pas besoin de s'y inscrire)."]
			}

			if request.user not in soiree.invites.all() :
				errors['hote_error'][0] = True
				errors['errors_count'] += 1
			if soiree.type_soiree in [models.Soiree.TypeDeSoiree.PRIV_LIST_INSC, models.Soiree.TypeDeSoiree.PUB_INSC] :
				if len(soiree.inscriptions.all())+1 >= soiree.nb_joueurs :
					errors['no_more_places'][0] = True
					errors['errors_count'] += 1
			if errors['errors_count'] == 0 :
				soiree.inscriptions.add(request.user)
				soiree.save()
			else :
				errors.pop('errors_count')
				return render(request, 'soiree/error.html', {'error_txt': "", 'errors': errors})

			last_view = request.session.get('last_view', ['welcome:index', []])
			return redirect(last_view[0], *last_view[1])

		else :
			return render(request, 'soiree/error.html', {'error_txt': "Vous n'avez pas la permission de voir cette soirée"})

	else :
		last_view = request.session.get('last_view', ['welcome:index', []])
		return redirect(last_view[0], *last_view[1])

@login_required
def desinscription(request) :

	soiree_id = request.GET.get('id', False)

	current_view = [f"{reverse('soiree:desinscription')}{f'?id={soiree_id}' if soiree_id else ''}", []]
	real_view = False

	if soiree_id :

		get_args = f"?id={soiree_id}"

		try :
			soiree = models.Soiree.objects.get(pk=soiree_id)
		except :
			soiree = None

		if admin.SoireeAdmin(models.Soiree, django_admin.site).has_view_permission(request, soiree) :

			errors = {
				'errors_count': 0,
				'hote_error': [False, "Vous ne pouvez pas vous désinscrire de cette soirée, vous ne faites pas partie des invités."]
			}

			if request.user not in soiree.invites.all() :
				errors['hote_error'][0] = True
				errors['errors_count'] += 1
			if errors['errors_count'] == 0 :
				soiree.inscriptions.remove(request.user)
				soiree.invites.remove(request.user)
				soiree.save()
			else :
				errors.pop('errors_count')
				return render(request, 'soiree/error.html', {'error_txt': "", 'errors': errors})

			last_view = request.session.get('last_view', ['welcome:index', []])
			return redirect(last_view[0], *last_view[1])

		else :
			return render(request, 'soiree/error.html', {'error_txt': "Vous n'avez pas la permission de voir cette soirée"})

	else :
		last_view = request.session.get('last_view', ['welcome:index', []])
		return redirect(last_view[0], *last_view[1])


@login_required
def delete_soiree(request) :

	soiree_id = request.GET.get('id', False)

	current_view = [f"{reverse('soiree:delete_soiree')}{f'?id={soiree_id}' if soiree_id else ''}", []]
	real_view = False

	if soiree_id :

		get_args = f"?id={soiree_id}"

		try :
			soiree = models.Soiree.objects.get(pk=soiree_id)
		except :
			soiree = None

		if admin.SoireeAdmin(models.Soiree, django_admin.site).has_del_permission(request, soiree) :

			soiree.delete()
			return redirect(f"{reverse('soiree:list')}")

		else :
			return render(request, 'soiree/error.html', {'error_txt': "Vous n'avez pas la permission de supprimer cette soirée"})

	else :
		last_view = request.session.get('last_view', ['welcome:index', []])
		return redirect(last_view[0], *last_view[1])
