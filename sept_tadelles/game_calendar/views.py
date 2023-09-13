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

	if request.user.soirees_invite.exists() :

		all_soirees = account_models.Soiree.objects.all()
		soirees = []
		for soiree in all_soirees :
			if request.user in soirees.invites.all() :
				soirees.append(soiree)

		helpers.register_view(request, current_view, real_view)
		return render(request, 'game_calendar/index.html', {'soirees': soirees})

	else :

		return redirect('welcome:index')