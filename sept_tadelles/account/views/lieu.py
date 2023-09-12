from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from account import models
from account.forms import lieu as forms


@login_required
def create_lieu(request) :

	current_view = ['account:create_lieu', []]
	real_view = False

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

			helpers.register_view(request, current_view, real_view)
			return render(request, 'account/lieu/creation_success.html', {})

	helpers.register_view(request, current_view, real_view)
	return render(request, 'account/lieu/creation_form.html', {'form': form})