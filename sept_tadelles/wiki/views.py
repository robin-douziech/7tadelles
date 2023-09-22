from django.contrib import admin as django_admin
from django.shortcuts import render, redirect
from django.http import HttpResponse

from account.views import helpers

from . import models, admin

def index(request):

    current_view = ['wiki:index', []]

    games = models.Game.objects.all()

    helpers.register_view(request, current_view)
    return render(request, "wiki/index.html", {
        "games": games,
        "categories": models.Category.objects.all(),
    })

def detail(request, game_id) :

    current_view = ['wiki:detail', []]

    try :
        game = models.Game.objects.get(pk=game_id)
    except :
        game = None

    if admin.GameAdmin(models.Game, django_admin.site).has_view_permission(request, game) :
        helpers.register_view(request, current_view)
        return render(request, 'wiki/detail.html', {'game': game})
    else :
        return render(request, 'account/error.html', {'error_txt': "Vous n'avez pas la permission de voir ce jeu (ou alors aucun jeu n'a cet identifiant)."})