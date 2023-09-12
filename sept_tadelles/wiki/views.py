from django.contrib import admin as django_admin
from django.shortcuts import render, redirect
from django.http import HttpResponse

from account.views import helpers

from . import models

def index(request):

    current_view = ['wiki:index', []]
    real_view = True

    games = []
    prochainement = []

    if request.method == "POST" :

        for cat in models.Category.objects.all() :
            if cat.name in request.POST.dict() and "on" in request.POST.dict()[cat.name] :
                for game in models.Game.objects.all() :
                    if game.category.name == cat.name :
                        if game.prochainement :
                            prochainement.append(game)
                        else :
                            games.append(game)

    else :

        games = models.Game.objects.filter(prochainement=False)
        prochainement = models.Game.objects.filter(prochainement=True)

    helpers.register_view(request, current_view, real_view)
    return render(request, "wiki/index.html", {
        "games": games,
        "prochainement": prochainement,
        "categories": models.Category.objects.all(),
    })

def detail(request, game_id) :

    current_view = ['wiki:detail', []]
    real_view = True

    try :
        game = models.Game.objects.get(pk=game_id)
    except :
        game = None

    if admin.SoireeAdmin(models.Soiree, django_admin.site).has_view_permission(request, game) :
        helpers.register_view(request, current_view, real_view)
        return render(request, 'wiki/detail.html', {'game': game})
    else :
        helpers.register_view(request, current_view, real_view)
        return render(request, 'account/error.html', {'error_txt': "Vous n'avez pas la permission de voir ce jeu (ou alors aucun jeu n'a cet identifiant)."})