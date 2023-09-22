from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from account import models
from account.forms import lieu as forms
import re

@login_required
def create_lieu(request) :

	current_view = ['account:create_lieu', []]

	form = forms.LieuCreationForm()
	errors = {
		'errors_count': 0,
		'code_postal_error': [False, "Le code postal doit être composé de 5 chiffres"],
	}

	if request.method == "POST" :

		form = forms.LieuCreationForm(request.POST, request.FILES)

		if form.is_valid() :

			if not(re.match(r"[0-9]{5}", form.cleaned_data['code_postal'])) :
				errors['code_postal_error'][0] = True
				errors['errors_count'] += 1

			if errors['errors_count'] == 0 :

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

				request.user.lieus.add(lieu)
				request.user.save()

				last_view = request.session.get('last_views', [['welcome:index', []], ['welcome:index', []]])[-2]
				return redirect(last_view[0], *last_view[1])

	errors.pop('errors_count')
	helpers.register_view(request, current_view)
	return render(request, 'account/lieu/creation_form.html', {'form': form, 'errors': errors})