from django.contrib import admin as django_admin
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from datetime import datetime

from account import models, admin
from account.forms import soiree as forms

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

		form = forms.SoireeForm(request, soiree)
		errors = {
			'errors_count': 0,
			'not_enough_places': [False, "Il ne peut pas y avoir moins de places que d'invités pour une soirée privée avec liste d'invités. Retirez des invités avant de réduire le nombre de places."],
		}

		if request.method == "POST" :

			form = forms.SoireeForm(request, soiree, request.POST)

			if form.is_valid() :

				if soiree.type_soiree == models.Soiree.TypeDeSoiree.PRIV_INVIT_CONFIRM and form.cleaned_data['nb_joueurs'] < len(soiree.invites.all())+1 :
					errors['not_enough_places'][0] = True
					errors['errors_count'] += 1

				if errors['errors_count'] == 0 :

					soiree.type_soiree = form.cleaned_data['type_soiree']
					soiree.nb_joueurs = form.cleaned_data['nb_joueurs']
					soiree.lieu = form.cleaned_data['lieu']
					soiree.date = form.cleaned_data['date']
					soiree.save()
		errors.pop('errors_count')
		return render(request, 'account/soiree/detail.html', {'form': form, 'soiree': soiree, 'types_soiree': models.Soiree.TypeDeSoiree.choices, 'types_soiree_desc': models.Soiree.TYPES_SOIREE_DESC, 'errors': errors})

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


