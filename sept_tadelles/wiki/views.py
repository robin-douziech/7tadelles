from django.shortcuts import render
from django.http import HttpResponse

from wiki.models import Game, Category

def index(request):

    games = []
    prochainement = []

    if request.method == "POST" :

        for cat in Category.objects.all() :
            if cat.name in request.POST.dict() and "on" in request.POST.dict()[cat.name] :
                for game in Game.objects.all() :
                    if game.category.name == cat.name :
                        if game.prochainement :
                            prochainement.append(game)
                        else :
                            games.append(game)

    else :

        games = Game.objects.filter(prochainement=False)
        prochainement = Game.objects.filter(prochainement=True)

    return render(request, "wiki/index.html", {
        "games": games,
        "prochainement": prochainement,
        "categories": Category.objects.all(),
    })

def detail(request, game_id) :
    return render(request, "wiki/detail.html", {
        "game": Game.objects.get(pk=game_id)
        })