from django.contrib import admin as django_admin

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from account import admin as account_admin
from account import models as account_models

from account.views import helpers

@login_required
def index(request) :

	current_view = ['game_calendar:game_calendar_index', []]
	real_view = True

	all_soirees = account_models.Soiree.objects.all()
	soirees = []
	for soiree in all_soirees :
		if account_admin.SoireeAdmin(account_models.Soiree, django_admin.site).has_view_permission(request, soiree) :
			soirees.append(soiree)

	helpers.register_view(request, current_view, real_view)
	return render(request, 'game_calendar/index.html', {'soirees': soirees})