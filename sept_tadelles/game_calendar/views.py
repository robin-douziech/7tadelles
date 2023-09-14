from django.contrib import admin as django_admin

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from account import admin as account_admin
from account import models as account_models

from account.views import helpers

@login_required
def index(request) :

	current_view = ['game_calendar:game_calendar_index', []]
	real_view = True

	if request.user.invitations.exists() :

		all_soirees = request.user.invitations.all()
		inscriptions = []
		invitations = []

		for soiree in all_soirees :
			if soiree in request.user.user_inscriptions.all() :
				inscriptions.append(soiree)
			else :
				invitations.append(soiree)

		helpers.register_view(request, current_view, real_view)
		return render(request, 'game_calendar/index.html', {'inscriptions': inscriptions, 'invitations': invitations})

	else :

		return redirect('welcome:index')