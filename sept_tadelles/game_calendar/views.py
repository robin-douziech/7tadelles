from django.shortcuts import render

from . import models

# Create your views here.

def index(request) :

	day_names = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
	month_names = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]

	soirees = models.Soiree.objects.all()

	for soiree in soirees :
		soiree.day_name = day_names[soiree.date.weekday()]
		soiree.month_name = month_names[soiree.date.month-1]

	return render(request, 'game_calendar/index.html', {'soirees': soirees})