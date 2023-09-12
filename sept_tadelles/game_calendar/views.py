from django.contrib import admin as django_admin

from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required

from account import admin as account_admin
from account import models as account_models

@login_required
def index(request) :
	all_soirees = account_models.Soiree.objects.all()
	soirees = []
	for soiree in all_soirees :
		if account_admin.SoireeAdmin(account_models.Soiree, django_admin.site).has_view_permission(request, soiree) :
			soirees.append(soiree)
	return render(request, 'game_calendar/index.html', {'soirees': soirees})