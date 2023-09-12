from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required

from account import admin as account_admin
from account import models as account_models

# Create your views here.

@login_required
@permission_required('account.view_soiree')
def index(request) :

	day_names = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
	month_names = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]

	soirees = account_models.Soiree.objects.all()

	for soiree in soirees :
		soiree.day_name = day_names[soiree.date.weekday()]
		soiree.month_name = month_names[soiree.date.month-1]

	return render(request, 'game_calendar/index.html', {'soirees': soirees})